$directory = __DIR__;
$stat = stat($directory);
$sizes = log($stat['size'], 1024);
echo "Last access:       ".gmdate("Y-m-d h:i:s",$stat['atime'])."\n";
echo "Last modification: ".gmdate("Y-m-d h:i:s",$stat['mtime'])."\n";
echo "Size:              ".str_pad(round(pow(1024, $sizes - floor($sizes)), $precision=0) . array('B', 'K', 'M', 'G', 'T')[floor($sizes)], 5, " "). " = " . $stat['size'] ." bytes" ."\n";
echo "Links count:       ".$stat['nlink'];