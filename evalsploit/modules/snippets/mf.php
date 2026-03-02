$cat = $_LOCAL;
if(file_exists($cat)){echo 'EXISTS';}
elseif(!@file_put_contents($cat,'')){
    if(!@touch($cat)){echo 'X';}
}
