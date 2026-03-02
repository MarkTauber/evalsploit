$_FIND_PATH = __PATH_PLACEHOLDER__;
$_FIND_PAT  = __PATTERN_PLACEHOLDER__;
$_it = new RecursiveIteratorIterator(
    new RecursiveDirectoryIterator($_FIND_PATH, FilesystemIterator::SKIP_DOTS),
    RecursiveIteratorIterator::SELF_FIRST
);
foreach($_it as $_f){
    if(@preg_match('/'.$_FIND_PAT.'/i', $_f->getFilename())){
        echo ($_f->isDir() ? '[D]' : '[F]').' '.$_f->getPathname()."\n";
    }
}
