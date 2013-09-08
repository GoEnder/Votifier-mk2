Votifier-mk2 Website Examples - PHP
==============
In this folder you'll find examples on how to create, sign, and send the vote  

The file that you need is `sendVote.php`  
This file is all you need to send a vote to a server.  
  
The file `verifyVote.php` is provided as a example of how Votifier-mk2 will read votes  
and can be used to check if your own signature program is working properly  


Libraries
--------------
These examples use the PHP library `phpseclib`  
They are avaliable through PEAR  
**Warning:** the current version of `phpseclib` in PHP-PEAR is slightly broken  
It is unable to properly verify signatures. If you wish to use it, pull RSA.php [From Github](https://github.com/phpseclib/phpseclib/blob/master/phpseclib/Crypt/RSA.php)