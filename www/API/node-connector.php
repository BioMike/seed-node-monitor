<?php
// $msg contains a real encrypted message. $iv is the IV that belongs with it. Let's see if we can decrypt it in PHP
$iv = "vCCgcZvaTguiMdq0SVVa4w==";
$msg = "eFxHUokk2GXosM2pgEcb0ng0TXafEdxRouN5t8e3vWwCuLpwJ1A13qoIgC0uJU6j1qYrLRT3MYpi1KxI7PoxXy7oNWxUlWyvwe8QK5AhEoIkztIShbuBC3OUwtCknIo0/+xc77kM7WFvDX4iFwnP3w==";

$password = "pre-Shared secret abcdefghijklmn";
$key = mb_convert_encoding($password, "UTF-8");

// MCRYPT_RIJNDAEL_128, we use a 16 bit key.
$json_data = mcrypt_decrypt(MCRYPT_RIJNDAEL_128, $key, base64_decode($msg), MCRYPT_MODE_CBC, base64_decode($iv));

$data = json_decode(ltrim($json_data));

echo "\n";
print_r($data);
echo "\n";

?>