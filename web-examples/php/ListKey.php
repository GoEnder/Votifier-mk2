<?php 
/* 
Example PHP Script for a Server List website to push their key to a central listing
Only should be run after GenerateKey type operations

'List Key' sends a request that your Public Key is listed in the Central Key Database, and made avaliable to Minecraft Servers

This is a operation that requires multiple payloads of data sent between the Server List website and the Central Key Database to make sure the keys are 100% valid

*/

/* Important Variable to be set correctly */
$domain = '';

/* Optional Variables for you to set */
/* These are best left as-is */
$keyname = 'servlist';

if ($domain == '' || preg_match('/\//i', $domain) || !preg_match('/\./i', $domain)) {
	die("
      Please include just your domain name in the default configuration of this script, do not include http or trailing slashes
      Good: domain.com
      Bad: http://domain.com/
	\n");
}


?>