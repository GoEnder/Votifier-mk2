<?php
/* 
Example PHP Script for a Server List website to generate a Private key and Public Key pair in PHP

Only should be run once, or when a Server List comprimization happens

*/


/* Important Variable to be set correctly */
$domain = '';

/* Optional Variables for you to set */
/* These are best left as-is */
$keyname = 'servlist';
$keysize = 4096;


/* Generation of Private and Public Keys */
if ($domain == '' || preg_match('/\//i', $domain) || !preg_match('/\./i', $domain)) {
	die("
      Please include just your domain name in the default configuration of this script, do not include http or trailing slashes
      Good: domain.com
      Bad: http://domain.com/
	\n");
} 
if ($keysize < 2048) {
  $keysize = 4096;
} 
if ($keyname = '') {
  $keyname = 'servlist';
}

$rsaKey = openssl_pkey_new(array( 
              'private_key_bits' => $keysize, 
              'private_key_type' => OPENSSL_KEYTYPE_RSA));

$privKey = openssl_pkey_get_private($rsaKey); 
openssl_pkey_export($privKey, $pem); // Your Private Key
$pubKey = sshEncPub($rsaKey); // Your Public Key

$umask = umask(0066); 
file_put_contents('id_'.$keyname, $pem); // Saving the Private Key
file_put_contents('id_'.$keyname.'.pub', $pubKey); // Saving the Public Key

function sshEncPub($privKey) {
    $keyInfo = openssl_pkey_get_details($privKey);
    $buffer  = pack("N", 7)."ssh-rsa".sshEncBuffer($keyInfo['rsa']['e']).sshEncBuffer($keyInfo['rsa']['n']);
    return "ssh-rsa ".base64_encode($buffer)." ".$domain;
}

function sshEncBuffer($buffer) {
    $len = strlen($buffer);
    if (ord($buffer[0]) & 0x80) {
        $len++;
        $buffer = "\x00" . $buffer;
    }
    return pack("Na*", $len, $buffer);
}

?>