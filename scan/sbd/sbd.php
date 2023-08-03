$directory = __DIR__;
$it = new RecursiveIteratorIterator(new RecursiveDirectoryIterator($directory), 
        RecursiveIteratorIterator::CHILD_FIRST, 
        RecursiveIteratorIterator::CATCH_GET_CHILD);
while($it->valid()) {

    if (!$it->isDot()) {
        try{
            if($it->isLink()){$il = "L";}else{$il = " ";}
            if($it->isreadable()){$ir = "R";}else{$ir = "-";}
            if($it->iswritable()){$iw = "W";}else{$iw = "-";}
            echo $ir. $iw. $il . " | " .$it->getsize() . " | " . $it->key() . "\n";
        }
        catch(Exception $e){echo " | " . $it->key() . "\n";}
    }                   
    $it->next();
}
