# Gotta Catch'em All

[This](https://tryhackme.com/room/pokemon) room on TryHackMe is really a good one and can be considered as majorly designed in a CTF style. The main target is to find different flags that are related to various pokemons and submit them to complete the questions. So, let's begin!

### Initial Foothold

The first thing that we need to do is to deploy the machine and then we can start our basic enumeration.

1. ##### Find the Grass-Type Pokemon

Once deployed, we can visit the IP address where we can see the default apache page. With time I've observed that many a times some important information is usually hidden in these default pages that is not directly visible but can be found in it's source code.

We can open the source-code by right-clicking on the page and selecting 'view source-code'. At the end of the code we can find a pair of credenitals:

![default_hidden_creds](./.images/default_hidden_creds.png)



Now, we have a pair of username and password but we don't know where we can use them. So, we can run a nmap scan to see what other services are open where we can try to use these credentials.

```
tester@kali:~$ nmap -A -T4 10.10.28.204
Starting Nmap 7.80 ( https://nmap.org ) at 2020-08-30 12:19 IST
Nmap scan report for 10.10.28.204
Host is up (0.16s latency).
Not shown: 998 closed ports
PORT   STATE SERVICE VERSION
22/tcp open  ssh     OpenSSH 7.2p2 Ubuntu 4ubuntu2.8 (Ubuntu Linux; protocol 2.0)
| ssh-hostkey: 
|   2048 58:14:75:69:1e:a9:59:5f:b2:3a:69:1c:6c:78:5c:27 (RSA)
|   256 23:f5:fb:e7:57:c2:a5:3e:c2:26:29:0e:74:db:37:c2 (ECDSA)
|_  256 f1:9b:b5:8a:b9:29:aa:b6:aa:a2:52:4a:6e:65:95:c5 (ED25519)
80/tcp open  http    Apache httpd 2.4.18 ((Ubuntu))
|_http-server-header: Apache/2.4.18 (Ubuntu)
|_http-title: Can You Find Them All?
Service Info: OS: Linux; CPE: cpe:/o:linux:linux_kernel

Service detection performed. Please report any incorrect results at https://nmap.org/submit/ .
Nmap done: 1 IP address (1 host up) scanned in 38.93 seconds
```

From the nmap scan result we can see that other than port 80 port 22 which is used for SSH is also open. Hence, we can try to access the machine via SSH using the discovered credentials:

```
tester@kali:~$ ssh xxxxxxx@10.10.28.204
The authenticity of host '10.10.28.204 (10.10.28.204)' can't be established.
ECDSA key fingerprint is SHA256:mXXTCQORSu35gV+cSi+nCjY/W0oabQFNjxuXUDrsUHI.
Are you sure you want to continue connecting (yes/no/[fingerprint])? yes
Warning: Permanently added '10.10.28.204' (ECDSA) to the list of known hosts.
xxxxxxx@10.10.28.204's password: 
Welcome to Ubuntu 16.04.6 LTS (GNU/Linux 4.15.0-112-generic x86_64)

 * Documentation:  https://help.ubuntu.com
 * Management:     https://landscape.canonical.com
 * Support:        https://ubuntu.com/advantage

84 packages can be updated.
0 updates are security updates.


The programs included with the Ubuntu system are free software;
the exact distribution terms for each program are described in the
individual files in /usr/share/doc/*/copyright.

Ubuntu comes with ABSOLUTELY NO WARRANTY, to the extent permitted by
applicable law.

xxxxxxx@root:~$ 
```

And we do get into the machine. Now, we can start solving the question. The first question asks us to find a 'grass-type pokemon' for which we can run a `find ` command as:

```
pokemon@root:~$ find / -name grass* 2> /dev/null
/var/lib/app-info/icons/ubuntu-xenial-universe/64x64/grass-core_grass70.png
^C
```

With this we can't find any useful file so, the next thing we can do is manually look for the file just in case if it is named something like gr4ss or something else.

On the Desktop, we can see a zip file which we can try to unzip and extract it's content. 

```
pokemon@root:~/Desktop$ ls
P0kEmOn.zip
pokemon@root:~/Desktop$ unzip P0kEmOn.zip 
Archive:  P0kEmOn.zip
   creating: P0kEmOn/
  inflating: P0kEmOn/grass-type.txt  
pokemon@root:~/Desktop$ ls
P0kEmOn  P0kEmOn.zip
pokemon@root:~/Desktop$ cd P0kEmOn/
pokemon@root:~/Desktop/P0kEmOn$ ls
grass-type.txt
pokemon@root:~/Desktop/P0kEmOn$ cat grass-type.txt
```

In the extracted files we can find the file `grass-type.txt`. On viewing the content of the file, we can determine that is not the exact file but encoded in hex. So, we can use the [CyberChef](https://gchq.github.io/CyberChef/) website to decode it and submit the obtained value as the answer to the first question.

2. ##### Find the Water-Type Pokemon

Again we can use the `find` command and see if something related to water comes up.

```
pokemon@root:~/Desktop/P0kEmOn$ find / -name water* 2> /dev/null
/var/www/html/water-type.txt
^C
pokemon@root:~/Desktop/P0kEmOn$ cat /var/www/html/water-type.txt 
```

It can be seen that we found a file named `water-type.txt` but the value that it contains appears to be decoded using ROT13. So, we can again go to CyberChef and decode it using the ROT13 function.

But if we look properly, we don't get any proper result. So, the next thing that can be done is try different rotation values. And while doing so, if we just go one step up i.e. `ROT14`, we get our deisired flag that can be submitted as the answer to second question.

3. ##### Find the Fire-Type Pokemon

This time also, we can find a file named `fire-type.txt` using the `find` command as:

```
pokemon@root:~/Desktop/P0kEmOn$ find / -name fire-type* 2> /dev/null
/etc/why_am_i_here?/fire-type.txt
^C
pokemon@root:~/Desktop/P0kEmOn$ cat /etc/why_am_i_here\?/fire-type.txt 
```

Again the content of the file is decoded. At the end of the string we can see `==`, which suggests that the string is `base64` encode. So, we can decode this value and submit it as the answer to the third question.



### Privilege Escalation

4. ##### Who is Root's Favorite Pokemon?

In the `/home` directory, we can see a file named `roots-pokemon.txt` that can't be accessed as `pokemon` user. Also, we can see there is another user named `ash`. From the permissions for the file `roots-pokemon.txt`, it can be concluded that it is accessible only by the users that have root level privileges.

```
pokemon@root:/home$ ls -la roots-pokemon.txt 
-rwx------ 1 ash root 8 Jun 22 23:21 roots-pokemon.txt
```

We can see what privileges we have by using the command `sudo -l`:

```
pokemon@root:/home$ sudo -l
[sudo] password for pokemon: 
Sorry, user pokemon may not run sudo on root.
```

Sadly, we are not allowed to run any commands as root on the machine. We can look for some other files in the system such as some shell script through which we can escalate our privileges to root level. 

On browsing through the various folders, we can find a bit strange sub-folder chain in `~/Videos` folder. 

```
pokemon@root:~$ cd ~/Videos/Gotta/Catch/Them/ALL\!/
pokemon@root:~/Videos/Gotta/Catch/Them/ALL!$ ls
Could_this_be_what_Im_looking_for?.cplusplus
```

Just by pressing the `tab` key again and again we can get the entire path. At the end we can find a file `Could_this_be_what_Im_looking_for?.cplusplus`. 

```
pokemon@root:~/Videos/Gotta/Catch/Them/ALL!$ cat Could_this_be_what_Im_looking_for\?.cplusplus 
# include <iostream>

int main() {
	std::cout << "ash : xxxxxxxx"
	return 0;
```

 The file contain a pair of credentials havind username as `ash`. So, we can use these credentials and switch user as `ash`.

```
}pokemon@root:~/Videos/Gotta/Catch/Them/ALL!$ su ash
Password: 
To run a command as administrator (user "root"), use "sudo <command>".
See "man sudo_root" for details.

bash: /home/ash/.bashrc: Permission denied
ash@root:/home/pokemon/Videos/Gotta/Catch/Them/ALL!$ 
```

Now we can again try to access the `roots-pokemon.txt` file. 

```
ash@root:/home/pokemon/Videos/Gotta/Catch/Them/ALL!$ cd /home
ash@root:/home$ cat roots-pokemon.txt 
XXXXXXXXash@root:/home$ 
```

And we got the final flag as well!

With this we completed this room!



## Some Key Points to Take Away

1. When you suspect presence of something use the `find` command.
2. Always enumerate different folders.
3. If vertical privilege escalation is not possible try to perform horizontal privilege escalation.