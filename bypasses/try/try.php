if (function_exists('exec') && is_callable('exec')) { echo "exec,";} 
if (function_exists('system') && is_callable('system')) { echo "system,";} 
if (function_exists('shell_exec') && is_callable('shell_exec')) { echo "shell_exec,";}
if (function_exists('passthru') && is_callable('passthru')) { echo "passthru,";}  
if (function_exists('popen') && is_callable('popen')) { echo "popen,";} 
if (function_exists('expect_popen') && is_callable('expect_popen')) { echo "expect_popen,";} 
if (function_exists('proc_open') && is_callable('proc_open')) { echo "proc_open,";} 
if (function_exists('pcntl_exec') && is_callable('pcntl_exec')) { echo "pcntl_exec,";}
if($r=@`echo 1`){echo"do,";}