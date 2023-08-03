$cat = $_LOCAL;

if (!@fopen($cat)){
    if(!@file_put_contents($cat)){
        if(!@touch($cat)){echo"X";}
    }
}