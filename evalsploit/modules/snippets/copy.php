$what = __WHAT__;
$where = __WHERE__;
if(!@copy($what, $where)){
    $error=error_get_last();
    echo "Error: ".$error['type']."\n".$error['message'];
}else{
    echo "+";
}
