<?php 
include_once('Crypt/RSA.php');

#
# This is only used as an example on how Votifier-mk2 might check votes
# This is not meant to be used by you.
# 
# This uses the pear library 'phpseclib' - There is a bug in the pear version
# You should use the version of RSA.php from github
#

function split_payload($payload) {
	$payload = explode('\xa7', $payload);
	return $payload;
}

function rsa_verify_sign($key, $signature, $message) {
	$rsa = new Crypt_RSA();
	$rsa->setHash("sha256"); 
	$rsa->setSignatureMode(CRYPT_RSA_SIGNATURE_PKCS1);
	$rsa->loadKey($key); 
	$signature = base64_decode($signature);
	$verify = $rsa->verify($message, $signature) ? True : False; 
	return $verify;
}

function parse_vote($payload) {
	$epoch = date('U');
	$payload = split_payload($payload);
	$message = $payload[0];
	$signature = $payload[1];
	$key = file_get_contents('id_servlist'.'.pub');
	$result = rsa_verify_sign($key, $signature, $message);
	if ($result) {
		$message = json_decode($message, True);
		return "Vote recieved from ".$message['serviceName']." created by ".$message['username']." from the IP ".$message['address']."\n";
	} else {
		return "False vote";
	}
}

$payload = '{"Type":"VOTE","serviceName":"","username":"KsaRedFx","address":"192.168.0.1","timestamp":"1378620737","uuid":"f0a1563c09c549f1917f7c1c58e0919737c5226e"}\xa7dIa8Bd2/iWBQDWU4rhLQOwuUYqRB8b2hOq0ajB7WHmeLQ32k786bus1Ir5W3ms0PKFUGEP89s3Wd9IAe9bjw+3sutL5JJtNZY9h9lI/tSswt6jqcAvcVhoRAzoF5SwxNd086CQ1YgIci+JwPdQ5ww1r8zvFZAzrnqkmcROQRLWXgqWT7JTtJ9NLVU/xIMqdhhid2iI0ak9mnaZqC21AWJwbniTpHwzTiQ9yCR/oHboprm/hP0JmDIq+py25q/Xd64RVuKKAZFM4K6ggjY8Sm3dxgNiHNdl2faiAKG63Vrk7y3LDB3cBryv2I7PQi4IGnmAMXsGBgihtViutcOqrL+WsqSNqKhuzxlkT+Z0JDvabKQQ636DmPCalp7jmxLj12N0AKMQeYzB+IwbqT7M1J0tXJlolcihACCEEaKVpJ4zTOAAm8Sli05Uyw0mFmiB5p23xp/fYnHiFNstMuauy2QZF8oRFjqFj0HHjaa0Ve+/hjndkO9WM9mJKo691JPzMyYyaFTOqlTsl/9kWD6IzokJ7fbz9tu6yZgTYZu423sNxhqlMYmo68kkIuDj4CUIKu7nLUbPICnJqfHraLUD9weZlzzjERdQ3bcfJgSwNdSoR5YT04QyCW9bqs8KaDsjm9wqTE2u9LXlJx8OL2OEw9jIG9eFeiAenGTO8mQA+Vy+g=';
print parse_vote($payload);

?>