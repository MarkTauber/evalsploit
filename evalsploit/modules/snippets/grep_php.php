$_GREP_PATH = __PATH_PLACEHOLDER__;
$_GREP_RE   = __REGEX_PLACEHOLDER__;
$_it = new RecursiveIteratorIterator(
    new RecursiveDirectoryIterator($_GREP_PATH, FilesystemIterator::SKIP_DOTS),
    RecursiveIteratorIterator::SELF_FIRST
);
foreach($_it as $_f){
    if(!$_f->isFile() || !$_f->isReadable()) continue;
    $_lines = @file($_f->getPathname(), FILE_IGNORE_NEW_LINES);
    if($_lines === false) continue;
    foreach($_lines as $_n => $_line){
        if(@preg_match($_GREP_RE, $_line)){
            echo $_f->getPathname().':'.($_n+1).':'.$_line."\n";
        }
    }
}
