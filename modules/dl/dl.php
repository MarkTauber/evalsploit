$cat = $_LOCAL;
if(is_readable($cat)){
    if($data = fread(fopen($cat, "r"),filesize($cat))){
        echo base64_encode($data);
    }else{echo "0";}

}else{ echo "X";}

