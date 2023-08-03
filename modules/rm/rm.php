$delete = $_LOCAL;
@unlink($delete);
echo file_exists($delete);