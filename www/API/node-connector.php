<?php
// $msg contains a real encrypted message. Let's see if we can decrypt it in PHP
$msg = "empty";

$password = "pre-Shared secret abcdefghijklmn";
$key = mb_convert_encoding($password, "UTF-8");

$data = mcrypt_decrypt(MCRYPT_RIJNDAEL_128, $key, $msg, MCRYPT_MODE_CBC [, string $iv ]

//key = bytes(secret, 'utf-8')
//iv = Random.new().read(AES.block_size)
//cipher = AES.new(key, AES.MODE_CFB, iv)
//msg = iv + cipher.encrypt(bytes(json_data, 'utf-8'))

?>