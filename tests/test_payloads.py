"""Minimal tests for payload generation and substitution."""

from evalsploit.transport.payloads import generate_backdoor, generate_polymorphic_backdoor, mutation_php
from evalsploit.modules.base import substitute


def test_generate_backdoor_classic():
    payloads = generate_backdoor("classic", "Z", "V")
    assert len(payloads) >= 1
    assert "Z" in payloads[0] and "V" in payloads[0]
    assert "isset($_POST[" in payloads[0]
    assert "die();" in payloads[0]


def test_generate_backdoor_bypass():
    payloads = generate_backdoor("bypass", "z1", "v1")
    assert len(payloads) >= 1
    assert "z1" in payloads[0] or "z1" in payloads[-1]


def test_generate_polymorphic():
    code = generate_polymorphic_backdoor("Zt", "Vt")
    assert "Zt" in code and "Vt" in code
    assert "isset" in code or "POST" in code


def test_mutation_php_structure():
    php = mutation_php("if(1){}", "abc123")
    assert "base64_decode" in php
    assert "abc123" in php
    assert "SCRIPT_FILENAME" in php
    assert "Mutated successfully" in php
    assert "ERR:marker line not found" in php
    assert "htmlentities" not in php


def test_mutation_php_finds_correct_marker():
    """The findme string must match what generate_backdoor/polymorphic actually produces."""
    from evalsploit.transport.payloads import generate_polymorphic_backdoor, generate_php8_backdoor
    for Z, V in [("myZ", "myV"), ("ab", "cd")]:
        for gen in (generate_polymorphic_backdoor, generate_php8_backdoor):
            backdoor = gen(Z, V)
            assert f"isset($_POST['{Z}'])" in backdoor, \
                f"{gen.__name__} output missing expected marker for Z={Z!r}"


def test_mutation_php_no_htmlentities_roundtrip():
    """Single quotes in findme must not be HTML-encoded — would break strpos on PHP 8.1+."""
    php = mutation_php("NEW_BACKDOOR", "myKey")
    findme_line = next(l for l in php.splitlines() if "$findme" in l)
    assert "&#039;" not in findme_line
    assert "myKey" in findme_line


def test_substitute():
    t = "hello $_LOCAL world"
    assert substitute(t, {"$_LOCAL": "x"}) == "hello x world"
    t2 = "$directory = __DIR__;"
    assert substitute(t2, {"$directory = __DIR__;": "$directory = '/tmp';"}) == "$directory = '/tmp';"
