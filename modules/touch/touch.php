$cat = $_LOCAL;
$date = $_DATE;
if (!@touch($cat, $date)) {
    echo "X";
}
