$directory = __DIR_PLACEHOLDER__;
$files2 = array_diff(scandir($directory, SCANDIR_SORT_DESCENDING), array('..', '.'));
foreach ($files2 as $item) {
    $path = $directory."/".$item;
    $stat = stat($path);
    if(is_dir($path)){$type = "[D]";$size = "     ";}else{$type = "[F]";
        $sz=$stat['size'];if($sz>0){$sizes=log($sz,1024);$_u=array('b','kb','mb','gb','tb');$size=str_pad(round(pow(1024,$sizes-floor($sizes))).$_u[min(4,(int)floor($sizes))],5," ");}else{$size="0b   ";}
    }
    if(is_readable($path)){$ir = "1";}else{$ir = "0";}
    if(is_writable($path)){$iw = "1";}else{$iw = "0";}
    echo gmdate("[Y-m-d h:i:s]",$stat['mtime']) . " " . $type . " |" . $ir . ":" . $iw . "| " . $size . " | ". $item . "\n";
}
