$directory = __DIR_PLACEHOLDER__;
$stat = @stat($directory);
if($stat === false){echo "ERR: cannot stat";}
else{
    $sz = (int)$stat['size'];
    if($sz > 0){$sizes=log($sz,1024);$size=str_pad(round(pow(1024,$sizes-floor($sizes)),0).array('B','K','M','G','T')[floor($sizes)],5," ")." = ".$sz." bytes";}else{$size="0 bytes";}
    echo "Last access:       ".gmdate("Y-m-d h:i:s",$stat['atime'])."\n";
    echo "Last modification: ".gmdate("Y-m-d h:i:s",$stat['mtime'])."\n";
    echo "Size:              ".$size."\n";
    echo "Links count:       ".$stat['nlink'];
}
