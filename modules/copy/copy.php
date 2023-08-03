$what = __DIR__;
$where  = __DIR__;
if(!@copy($what, $where)){
    $error=error_get_last();
    echo "Error: ".$error['type']."\n".$error['message'];
}else{
    echo "+";
}