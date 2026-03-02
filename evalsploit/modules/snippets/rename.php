$cat = $_LOCAL;
$ren = $_REMOTE;
if(@rename($cat,$ren)){echo 'OK';}else{echo 'ERR';}
