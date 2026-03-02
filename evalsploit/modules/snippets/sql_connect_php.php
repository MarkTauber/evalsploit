$_SQL_DSN  = __DSN_PLACEHOLDER__;
$_SQL_USER = __USER_PLACEHOLDER__;
$_SQL_PASS = __PASS_PLACEHOLDER__;
try {
    $_pdo = new PDO($_SQL_DSN, $_SQL_USER, $_SQL_PASS, [PDO::ATTR_ERRMODE=>PDO::ERRMODE_EXCEPTION, PDO::ATTR_TIMEOUT=>5]);
    $_v = $_pdo->query('SELECT VERSION()')->fetchColumn();
    echo 'OK '.$_v;
} catch(Exception $_e) {
    echo 'ERR '.$_e->getMessage();
}
