$cat = $_LOCAL;
$size = @filesize($cat);
if(is_readable($cat)){
    if($data = fread(fopen($cat, "r"),filesize($cat))){
    echo base64_encode($data);
    } 
}