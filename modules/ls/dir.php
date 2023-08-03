$directory = __DIR__;
$files2 = array_diff(scandir($directory, SCANDIR_SORT_DESCENDING), array('..', '.'));
foreach ($files2 as $item) {
    $path = $directory."/".$item;
    $stat = stat($path);
    if(is_dir($path)){$type = "[D]";$size = "     ";}else{$type = "[F]";
        $sizes = log($stat['size'], 1024);
        $size = str_pad(round(pow(1024, $sizes - floor($sizes)), $precision=0) . array('b', 'kb', 'mb', 'gb', 'tb')[floor($sizes)], 5, " ");
    }
    if(is_readable($path)){$ir = "1";}else{$ir = "0";}
    if(is_writable($path)){$iw = "1";}else{$iw = "0";}
    echo gmdate("[Y-m-d h:i:s]",$stat['mtime']) . " " . $type . " |" . $ir . ":" . $iw . "| " . $size . " | ". $item . "\n";
}