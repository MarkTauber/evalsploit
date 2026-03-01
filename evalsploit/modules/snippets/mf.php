$cat = $_LOCAL;
if (!file_exists($cat)) {
    if (!@file_put_contents($cat, '')) {
        if (!@touch($cat)) { echo "X"; }
    }
}
