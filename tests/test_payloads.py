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


def test_mutation_php():
    php = mutation_php("if(1){}", "Z")
    assert "base64_decode" in php
    assert "isset($_POST[" in php
    assert "getcwd" in php or "PHP_SELF" in php


def test_substitute():
    t = "hello $_LOCAL world"
    assert substitute(t, {"$_LOCAL": "x"}) == "hello x world"
    t2 = "$directory = __DIR__;"
    assert substitute(t2, {"$directory = __DIR__;": "$directory = '/tmp';"}) == "$directory = '/tmp';"
