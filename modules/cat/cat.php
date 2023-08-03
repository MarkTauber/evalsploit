$cat = $_LOCAL;
if(is_readable($cat)){
    if($data = fread(fopen($cat, "r"),filesize($cat))){
        echo htmlentities($data);
    }else{echo "0";}

}

