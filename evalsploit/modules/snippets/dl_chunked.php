$_DL_f=$_LOCAL;
$_DL_off=(int)$_OFFSET;
$_DL_len=(int)$_LENGTH;
if(!is_readable($_DL_f)){echo 'ERR:not readable';}
elseif($_DL_off===0&&$_DL_len===0){echo 'SIZE:'.filesize($_DL_f);}
else{
    $_DL_fh=fopen($_DL_f,'rb');
    if(!$_DL_fh){echo 'ERR:cannot open';}
    else{
        fseek($_DL_fh,$_DL_off);
        $_DL_data=fread($_DL_fh,$_DL_len);
        fclose($_DL_fh);
        if($_DL_data===false){echo 'ERR:read failed';}
        else{echo base64_encode($_DL_data);}
    }
}
