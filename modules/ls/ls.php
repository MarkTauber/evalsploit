$directory = __DIR__;

if(file_exists($directory)  && is_readable($directory) ){
foreach (new DirectoryIterator($directory) as $fileInfo) {
    if($fileInfo->isDot()) continue;
    $base = log($fileInfo->getsize(), 1024);
    if($fileInfo->isreadable()){$ir = "1";}else{$ir = "0";}
    if($fileInfo->iswritable()){$iw = "1";}else{$iw = "0";}
    if(!$fileInfo->isdir()){$if="[F]";$size = str_pad(round(pow(1024, $base - floor($base)), $precision=0) . array('b', 'kb', 'mb', 'gb', 'tb')[floor($base)], 5, " ");}else{$if="[D]"; $size = "     ";}
    echo  gmdate("[Y-m-d h:i:s]", $fileInfo->getCTime()) . " ". $if. " |" . $ir .":".  $iw .  "| " . $size . " | ". $fileInfo->getFilename() . "\n";
}
}else{
    echo "Cant access " . $directory;
}