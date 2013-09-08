<?php
include_once('Crypt/RSA.php');

$domain = '';

#
# This is example code on how to send a vote to Votifier-mk2
# Votes cosist of a json encoded hash with the values
# Type, serviceName, username, address, timestamp, uuid
# All extra values will be ignored by Votifier-mk2
#
# The Json encoded hash (Our vote) is then signed
# The signature is then appended to the end of the vote string with '\xa7' as a delimiter
# vote + '\xa7' + signature
# And finally sent to the server
#

function load_keys($ident, $type) {
	if ($type == 'public') {
		$key = file_get_contents($ident.'.pub');
	} elseif ($type == 'private') {
		$key = file_get_contents($ident);
	}
	return $key;
}

function rsa_sign($key, $message) {
	$rsa = new Crypt_RSA(); 
	$rsa->setHash("sha256"); 
	$rsa->setSignatureMode(CRYPT_RSA_SIGNATURE_PKCS1); 
	$rsa->loadKey($key); 
	$signature = $rsa->sign($message);
	$signature = base64_encode($signature);
	return $signature;
}

function build_vote($user, $addr, $domain) {
	$epoch = date('U');
	$uuid = hash('sha1', $epoch.$domain.$user.$addr);
	$vote = json_encode(array("Type"=>"VOTE", "serviceName"=>$domain, "username"=>$user, "address"=>$addr, "timestamp"=>$epoch, "uuid"=>$uuid));
	return $vote;
}

function build_payload($user, $addr, $domain) {
	$vote = build_vote($user, $addr, $domain);
	$sign = rsa_sign(load_keys('id_servlist', 'private'), $vote);
	$payload = $vote . '\xa7' . $sign;
	return $payload;
}

function send_vote($server, $port, $user, $addr, $domain) {
	$payload = build_payload($user, $addr, $domain);
	$socket = socket_create(AF_INET, SOCK_STREAM, SOL_TCP);
	if ($socket === false) {
		return "socket_create() failed: reason: " . socket_strerror(socket_last_error()) . "\n";
	}
	$result = socket_connect($socket, $addr, (int) $port);
	if ($result === false) {
		return "socket_connect() failed.\nReason: ($result) " . socket_strerror(socket_last_error($socket)) . "\n";
	}
	socket_write($socket, $payload);
	socket_read($socket, 2048);
	socket_close($socket);
}

$output = send_vote('127.0.0.1', '35566', 'KsaRedFx', '192.168.0.1', $domain);
print $output;


?>