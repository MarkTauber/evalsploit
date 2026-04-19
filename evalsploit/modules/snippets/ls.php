$directory = __DIR_PLACEHOLDER__;
if(file_exists($directory)  && is_readable($directory) ){
foreach (new DirectoryIterator($directory) as $fileInfo) {
    if($fileInfo->isDot()) continue;
    if($fileInfo->isreadable()){$ir = "1";}else{$ir = "0";}
    if($fileInfo->iswritable()){$iw = "1";}else{$iw = "0";}
    if(!$fileInfo->isdir()){$if="[F]";$sz=$fileInfo->getSize();if($sz>0){$base=log($sz,1024);$_u=array('b','kb','mb','gb','tb');$size=str_pad(round(pow(1024,$base-floor($base))).$_u[min(4,(int)floor($base))],5," ");}else{$size="0b   ";}}else{$if="[D]"; $size = "     ";}
    echo  gmdate("[Y-m-d h:i:s]", $fileInfo->getCTime()) . " ". $if. " |" . $ir .":".  $iw .  "| " . $size . " | ". $fileInfo->getFilename() . "\n";
}
}else{
    echo "Cant access " . $directory;
}
