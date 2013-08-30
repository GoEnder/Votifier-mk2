Votifier-mk2
============
A Minecraft Plugin to replace Votifier, due to the very backwards implementation of RSA
  
  
What is Votifier-mk2
-----------------
Votifier-mk2 is a replacement for the "Votifer" plugin for Minecraft.  
Due to how Votifier implimented RSA, it has a lot of very large security holes that almost render it's security as none.  
  
  
  
How is it different?
-----------------
**In Votifier**  
the RSA Private and Public keys are generated by the Minecraft Server,  
_The Public key is then given to the server listing website_, like Planet Minecraft.  
There is a large flaw here, where if your Public key is leaked, anyone can spoof votes to your server.  
You must make a new set of keys, making you have to update all the websites with your new key.  
_**This is inherently wrong, and defeats the purpose of RSA**_
  
  
  
**In Votifier-mk2**  
The RSA Private and Public keys are generated by the website,  
_The Public key is given to the Minecraft Server._  
If you happen to put a bad public key in your Minecraft Server, you just remove it.  
You no longer have to regenerate your keys, or any keys, or update any websites.  
_**This is how RSA keys are meant to be used**_  
  
  
**Basically**
in Votifier if the website gets comrpimised, you have to start over and give every website a new key
in Votifier-mk2 if the website gets comprimised, you just remove that websites bad key
  
  
  
  
How does RSA work?
------------------
RSA works by generating two keys, The **Private** key, and the **Public** key.  
The **Private** key is mean to never, ever be shared. It is meant to be **Private**.  
The **Public** key is meant to be shared, givien out, and it is meant to be **Public**.  
**The Private key basically is the _end-all-be-all_ that says _"I am, who i say i am"_**  

The keys are used to "Scramble" messages,  
The private key scrambles it in a way that only the public key can read.  
If the private key sends out a message, anyone can read it.  
  
   
The public key scrambles it in a way that only the private key can read.  
If the public key sends out a message, only the private key can read it.  
  
  
  
How is this relevant? 
-------------------
In **Votifier-mk2**   
All messages are sent from the website using the private key, anyone can read them.  
Nobody can pretend to be that website.  
_**This, is secure**_  
  
In **Votifier**  
All messages are sent from the website using the public key, nobody but the server can read them.  
Anyone with the public key can send them to the server.  
_**This, is not secure**_  




Central Key Repository?
-------------------
Votifier-mk2 will have a central location where we track and store all Server List Websites possible.

**For the Website Owner**   
We will only track the keys for the websites who request tracking, but it is highly reccomended.  
This requires sending a request to us with your key every time you change it.  
This allows server owners to always have the right key.  
This also allows you to be alerted when you have a possible server comprimization  

**For the Server Owner**  
Our "Central Key Repository" will be an _Opt-In_ feature that allows you to:
 * Add allowed keys on the fly
 * Remove allowed keys on the fly
 * Report bad keys
 * Automatically be alerted if you have a bad key
 * Automatically have bad keys updated to good ones