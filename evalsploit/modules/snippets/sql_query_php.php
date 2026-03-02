$_SQL_DSN  = __DSN_PLACEHOLDER__;
$_SQL_USER = __USER_PLACEHOLDER__;
$_SQL_PASS = __PASS_PLACEHOLDER__;
$_SQL_Q    = __QUERY_PLACEHOLDER__;
try {
    $_pdo = new PDO($_SQL_DSN, $_SQL_USER, $_SQL_PASS, [PDO::ATTR_ERRMODE=>PDO::ERRMODE_EXCEPTION, PDO::ATTR_TIMEOUT=>5]);
    $_stmt = $_pdo->query($_SQL_Q);
    $_rows = $_stmt->fetchAll(PDO::FETCH_ASSOC);
    if (empty($_rows)) {
        echo "OK (".$_stmt->rowCount()." rows affected)\n";
    } else {
        $_cols = array_keys($_rows[0]);
        $_w = array();
        foreach ($_cols as $_c) $_w[$_c] = strlen($_c);
        foreach ($_rows as $_row) {
            foreach ($_cols as $_c) {
                $_l = strlen((string)$_row[$_c]);
                if ($_l > $_w[$_c]) $_w[$_c] = $_l;
            }
        }
        $_sep = '+';
        foreach ($_cols as $_c) $_sep .= str_repeat('-', $_w[$_c]+2).'+';
        echo $_sep."\n";
        $_h = '';
        foreach ($_cols as $_c) $_h .= '| '.str_pad($_c, $_w[$_c]).' ';
        echo $_h."|\n".$_sep."\n";
        foreach ($_rows as $_row) {
            $_r = '';
            foreach ($_cols as $_c) $_r .= '| '.str_pad((string)$_row[$_c], $_w[$_c]).' ';
            echo $_r."|\n";
        }
        echo $_sep."\n".count($_rows)." row(s)\n";
    }
} catch(Exception $_e) {
    echo 'ERR '.$_e->getMessage()."\n";
}
