$cat = $_LOCAL;

if (!file_exists("$cat")) {
    if(!mkdir($cat,0777,true)){echo "X";}else{if(!file_exists("$cat")){echo "X1";}}
}else{
    echo "X2";
}