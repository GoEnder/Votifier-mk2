Votifier-mk2 Website Examples
==============
Tips and examples on how to impliment Votifier-mk2 on your website
  
  


How to send a vote
-------------
To send a vote, You must create a Json Serialized object with the following peramiters  

| Name        | Value           | Format    | Description                      | Example        |
|:----------- |:---------------:|:---------:|:-------------------------------- |:--------------:|
| Type        | "VOTE"          | String    | Literally "VOTE"                 | 'VOTE'         |
| serviceName | Your Domain     | String    | Domain name matching your pubkey | 'domain.com'   |
| username    | Voters Username | String    | Username of the voter            | 'Herobrine'    |
| address     | Voters IP       | String    | IP Address of the voter          | '192.168.0.1'  |
| timestamp   | Unix Timestamp  | Int/Float | Seconds since Epoch              | 1378620756     |
| uuid        | Random data     | String    | A different UUID each time       |                |

You must then sign the vote using the RSA Private key and the Sha256 algorytm  
Finally, You append the signature to the end of the json object with a `\xa7` delimiter  

`Vote` + `'\xa7'` + `signature`
  
_Note: Extra peramiters are just ignored with no error, plugins **can** hook into the extra data_


Votifier-mk2 Central Repository  
-------------
Votifier-mk2 will have a "Central Repository" that helps keep security to a maximum for everyone.  
Because of how the Repository works, it will require manually enabling before use.  
  

**For Server List Owners**  
The Central Repository will keep your keys in a easily seen location  
It will also keep your keys up to date with Server Owners and greatly reduce vote spoofing even further  
This requires sending a request to us with your key every time you change it. This should not be often.  

Why you should use it:
 * Your keys are avaliable to anyone looking to add your website to their vote list  
 * Your keys are checked for integrity and if any comprimization has happened  
 * Free listing in our Repo for your site  
  

**For Minecraft Server Owners**  
The Central Repository will allow you to reach out and access keys in a easy to find place
  
Why you should use it:
 * Keys can be automatically checked for comprimization every startup  
 * Keys can easily be added or removed on the fly with a command in-game  
 * Automatic updates for keys if they are out of date or comprimized  
 * Easy, or Automatic Generation of Config Files  
  

**What is Comprimization**  
Comprimization is when a Server List website's Private Key is comprimized (made public or abused)  