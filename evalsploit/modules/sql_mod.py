"""sql: interactive SQL console via PDO (MySQL/PostgreSQL)."""

from __future__ import annotations

import re
from typing import TYPE_CHECKING, Optional

from evalsploit.modules.base import Module, load_snippet, substitute, php_quote
from evalsploit.modules.registry import register

if TYPE_CHECKING:
    from evalsploit.context import SessionContext


def _parse_dsn(raw: str) -> tuple[str, str, str]:
    """Parse [driver://]user:pass@host[:port][/db] → (pdo_dsn, user, pass)."""
    m = re.match(
        r'^(?:(mysql|pgsql)://)?([^:@]+):([^@]*)@([^:/]+)(?::(\d+))?(?:/(.*))?$',
        raw.strip(),
    )
    if not m:
        raise ValueError(
            f"Cannot parse: {raw!r}. Expected: [mysql://]user:pass@host[:port][/db]"
        )
    driver, user, passwd, host, port, db = m.groups()
    driver = driver or "mysql"
    if driver == "mysql":
        pdo = f"mysql:host={host};connect_timeout=5"
        if port:
            pdo += f";port={port}"
        if db:
            pdo += f";dbname={db}"
        pdo += ";charset=utf8"
    else:  # pgsql
        pdo = f"pgsql:host={host};connect_timeout=5"
        if port:
            pdo += f";port={port}"
        if db:
            pdo += f";dbname={db}"
    return pdo, user, passwd


def _switch_db(pdo_dsn: str, db: str) -> str:
    """Replace or insert dbname in PDO DSN string."""
    if "dbname=" in pdo_dsn:
        return re.sub(r'dbname=[^;]*', f'dbname={db}', pdo_dsn)
    if ";charset=" in pdo_dsn:
        return pdo_dsn.replace(";charset=", f";dbname={db};charset=")
    return pdo_dsn + f";dbname={db}"


def _run_query(ctx: "SessionContext", pdo_dsn: str, user: str, passwd: str, query: str) -> str:
    snip = load_snippet("php", "sql_query")
    if not snip:
        return "Snippet not found"
    php = substitute(snip, {
        "__DSN_PLACEHOLDER__": php_quote(pdo_dsn),
        "__USER_PLACEHOLDER__": php_quote(user),
        "__PASS_PLACEHOLDER__": php_quote(passwd),
        "__QUERY_PLACEHOLDER__": php_quote(query),
    })
    return ctx.send(php).strip()


@register(
    "sql",
    description="Interactive SQL console (PDO/MySQL/PostgreSQL)",
    usage="sql [user:pass@host[:port][/db]]",
)
class SqlModule(Module):
    def run(self, ctx: "SessionContext", args: str) -> Optional[str]:
        raw = args.strip() or getattr(ctx.config, "sql_dsn", "")
        if not raw:
            print("Usage: sql user:pass@host[:port][/db]")
            print("  Or:  set sql mysql://user:pass@host/db  (save DSN)")
            return None

        try:
            pdo_dsn, user, passwd = _parse_dsn(raw)
        except ValueError as e:
            print(f"Error: {e}")
            return None

        conn_snip = load_snippet("php", "sql_connect")
        if not conn_snip:
            print("Snippet not found")
            return None

        php = substitute(conn_snip, {
            "__DSN_PLACEHOLDER__": php_quote(pdo_dsn),
            "__USER_PLACEHOLDER__": php_quote(user),
            "__PASS_PLACEHOLDER__": php_quote(passwd),
        })
        result = ctx.send(php).strip()
        if result.startswith("ERR"):
            print(f"Connection failed: {result[4:]}")
            return None

        ctx.config.sql_dsn = raw
        ctx.config.save_global()
        print(result)

        label = raw.rsplit("/", 1)[-1] if "/" in raw else raw.rsplit("@", 1)[-1]
        while True:
            try:
                query = input(f"sql:{label}> ").strip()
            except (EOFError, KeyboardInterrupt):
                print()
                break
            if not query or query.lower() == "exit":
                break

            use_m = re.match(r'use\s+(\w+);?$', query, re.IGNORECASE)
            if use_m:
                new_db = use_m.group(1)
                pdo_dsn = _switch_db(pdo_dsn, new_db)
                label = new_db
                print(f"Database changed to {new_db}")
                continue

            out = _run_query(ctx, pdo_dsn, user, passwd, query)
            if out:
                print(out)

        return None
