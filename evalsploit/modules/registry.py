"""Command registry: name -> Module class and optional help."""

from __future__ import annotations

from typing import TYPE_CHECKING, Dict, Optional, Tuple, Type

if TYPE_CHECKING:
    from evalsploit.modules.base import Module

COMMANDS: Dict[str, Type["Module"]] = {}
COMMAND_HELP: Dict[str, Tuple[str, str]] = {}  # cmd -> (description, usage)


def register(
    name: str,
    description: Optional[str] = None,
    usage: Optional[str] = None,
):
    """Decorator: register a Module class under command name. Optional description and usage for help."""

    def deco(cls: Type["Module"]) -> Type["Module"]:
        COMMANDS[name] = cls
        if description is not None or usage is not None:
            COMMAND_HELP[name] = (description or "-", usage or name)
        return cls

    return deco


def get(name: str):
    """Get module class by command name."""
    return COMMANDS.get(name)
