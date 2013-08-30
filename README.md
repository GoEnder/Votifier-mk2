Votifier-mk2
============
A Minecraft Plugin to replace Votifier, due to the very backwards implementation of RSA


## What is Votifier-mk2
-----------------
Votifier-mk2 is a replacement for the "Votifer" plugin for Minecraft.  
Due to how Votifier implimented RSA, it has a lot of very large security holes that almost render it's security as none.  
  
  
  
## How is it different?
-----------------
In Votifier, the RSA Private and Public keys are generated by the Minecraft Server, and then the Public key is given to the server listing website.  
There is a large flaw here, where if your Public key is leaked, anyone can spoof votes to your server.... And then you have to make a new set of keys, making you have to update all the websites with your new key.  
_**This is inherently wrong, and defeats the purpose of RSA**_
  
In Votifier-mk2, The RSA Private and Public keys are generated by the website, and the Public key is given to the Minecraft Server.
If you happen to put a bad public key in your Minecraft Server, you can just remove it for that one site, instead of having to regenerate a new key and update all the websites.  
_**This is how RSA keys are meant to be used**_  
  
  

## How does RSA work?
------------------
RSA works by generating two keys, The **Private** key, and the **Public** key.  
The **Private** key is mean to never, ever be shared. It is meant to be **Private**.  
The **Public** key is meant to be shared, givien out, and it is meant to be **Public**.  
  
The private key basically is the end-all-be-all that says "I am, who i say i am"  

Theys keys are used to "Scramble" messages,  
The private key scrambles it in a way that only the public key can read, so if the private key sends out a message, anyone can read it.  
The public key scrambles it in a way that only the private key can read, so if the public key sends out a message, only the private key can read it.  



## How is this relevant? 
-------------------
In Votifier-mk2, all messages are sent from the website using the private key, anyone can read them, but nobody can pretend to be that website. _**This, is secure**_  
In Votifier, all messages are sent from the website using the public key, nobody but the server can read them, but anyone with the public key can send them to the server. _**This, is not secure**_  
