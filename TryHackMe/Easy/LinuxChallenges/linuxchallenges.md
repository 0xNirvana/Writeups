# Linux Challenges
The [Linux Challenges](https://tryhackme.com/room/linuxctf) room on TryHackMe is one such room based on learning Linux. One really good feature of this room is that it is designed in a CTF fashion. So, it pretty much gives a feeling of solving some CTF challenge along with learning new things related to Linux.

This room has more than 30 hidden flags associated with different questions. As an answer to each question, we need to submit the relevant flag. To begin we are provided credentials of one of the users:

```
Username: garry
Password: letmein
```

With this, let's deploy the machine and get started with the challenge!

### [Task 1] Linux Challenges Introduction 
1. How many visible files can you see in garrys home directory?

We can log in as garry through SSH using the command `ssh garry@machine_ip` and entering the password when prompted. Once logged in as garry, we can simply check the number of visible files using the command:
```
ls
```

### [Task 2] The Basics 
1. What is flag 1?

In the previous question when we ran the command `ls`, we saw the file `flag1`. Now, we just need to read the content of that file and find our flag.

2. Log into bob's account using the credentials shown in flag 1. What is flag 2?

For this question, first of all, we need to switch the user as 'bob' using the command `su bob` and then entering the value of password obtained from `flag1.txt`. Next, the question asks to check bob's files which means we need to check files `/home/bob` directory.

```
garry@ip-10-10-238-167:~$ su bob
Password: 
bob@ip-10-10-238-167:/home/garry$ cd /home/bob
bob@ip-10-10-238-167:~$ ls
Desktop  Documents  Downloads  flag13  flag21.php  flag2.txt  flag8.tar.gz  Music  Pictures  Public  Templates  Videos
bob@ip-10-10-238-167:~$ 
```

Here, we can see that there is file named `flag2.txt` which contains our flag. We can simple print that file and get our flag.

3. Flag 3 is located where bob's bash history gets stored.

Details related to bash history are stored in a file named `~/.bash_history` in each user's directory. As we are currently in bob's directory itself we can access the file easily. 

As the file begins with '.', it is hidden and hence was not visible when we listed the files in the last question.

```
bob@ip-10-10-238-167:~$ cat .bash_history 
```

4. Flag 4 is located where cron jobs are created.

All the cron jobs can be accessed through the command `crontab -l` and the flag can be found in that command's output itself.
```
bob@ip-10-10-238-167:~$ crontab -l
```

5. Find and retrieve flag 5.

We are not provided any information regarding where can we find the file in which the flag would be present. So, we can use the `find` command and look throughout the system for any file named `flag5.txt`:
```
bob@ip-10-10-238-167:~$ find / -name flag5* 2> /dev/null
/lib/terminfo/E/flag5.txt
bob@ip-10-10-238-167:~$ cat /lib/terminfo/E/flag5.txt
```

With the switch `-name` we can specify the filename we are looking for and the '\*' in the filename is actually a wildcard so that we can find any file whose name begins with 'flag5' regardless of the file extension it has. The value `2> /dev/null` is used so that all the error values are not displayed to us.

6. "Grep" through flag 6 and find the flag. The first 2 characters of the flag is c9.

First, we need to find the file named 'flag6', which can be done using the command `find / -name flag6* 2> /dev/null`. And once, the file is found we can use `grep` command to find any string that begins with 'c9'.
```
bob@ip-10-10-238-167:~$ find / -name flag6* 2> /dev/null
/home/flag6.txt
bob@ip-10-10-238-167:~$ grep -E c9.* /home/flag6.txt
```

In the grep command `-E` switch is used to specify that we are using regex to find the string.

7. Look at the systems processes. What is flag 7.

System processes can be checked using `ps aux` command. In the output, we need to look for the value that either starts with 'flag7' or looks like a long string similar to what our flags usually look like.
```
bob@ip-10-10-238-167:~$ ps aux
```

8. De-compress and get flag 8.

First, we must find where flag 8 is located using the `find` command. We can then see a file that is compressed as the extension is `tar.gz`. Any such `gzip` file can be decompressed using the command `tar -zxvf filname`, so we can use the same over here to decompress the file. Once, decompressed, we get `flag8.txt` in which our required flag is present.
```
bob@ip-10-10-9-65:~$ tar -vxf flag8.tar.gz 
flag8.txt
bob@ip-10-10-9-65:~$ cat flag8.t
flag8.tar.gz  flag8.txt     
bob@ip-10-10-9-65:~$ cat flag8.txt
```

9. By look in your hosts file, locate and retrieve flag 9.

This question is talking about the `/etc/hosts` file which is used for mapping the hostnames to IP addresses usually on localhost but can be configured for other addresses as well. So, we just need to read the `/etc/hosts` file in order to get or flag.
```
bob@ip-10-10-9-65:~$ cat /etc/hosts
```

10. Find all other users on the system. What is flag 10.

We can find all the users present on the system in the `/etc/passwd` file as it's main purpose is to keep a track of all the users present on the system. In that file, we can find one user with our flag as it's username. 
```
bob@ip-10-10-9-65:~$ cat /etc/passwd

```

### [Task 3] Linux Functionality
1. Run the command flag11. Locate where your command alias are stored and get flag 11.

This question makes it very clear that `flag11` is not some file but a command that we can run on our shell. On running that command, we get a hint related to `aliases`. And details related to the alias of an user are stored in `~/.bashrc` file.

2. Flag12 is located were MOTD's are usually found on an Ubuntu OS. What is flag12?

MOTD stands for Message of the Day. It is a banner that usually appears on the login screen. All the files related to MOTD are stored at `/etc/update-motd.d`. But from all the files present in this directory only one file `00-header` is useful to us as it contains the actual banner and in the same file we can find our flag.
```
bob@ip-10-10-9-65:~$ cd /etc/update-motd.d/
bob@ip-10-10-9-65:/etc/update-motd.d$ ls
00-header     51-cloudguest         91-release-upgrade  98-fsck-at-reboot   99-esm
10-help-text  90-updates-available  97-overlayroot      98-reboot-required  logo.txt
bob@ip-10-10-9-65:/etc/update-motd.d$ cat 00-header 
```

3. Find the difference between two script files to find flag 13.

Linux has a command called `diff` which is used to determine the difference between two given files. We can use the same command here to see the difference between the two files which must be the flag that we are looking for.
```
bob@ip-10-10-9-65:~/flag13$ ls 
script1  script2
bob@ip-10-10-9-65:~/flag13$ diff script1 script2
```	

4. Where on the file system are logs typically stored? Find flag 14.

All the logs on a Linux machine are stored in `/var/log` directory. Hence, all that we need to do is just go to that directory and there we can find a file named `flagfourteen.txt`. We can find our flag at the end of this file.

```
bob@ip-10-10-73-24:/$ cd var
bob@ip-10-10-73-24:/var$ ls
backups  cache  crash  lib  local  lock  log  mail  metrics  opt  run  snap  spool  tmp  www
bob@ip-10-10-73-24:/var$ cd log
bob@ip-10-10-73-24:/var/log$ ls
alternatives.log    auth.log.1             dist-upgrade      gdm3             lxd                unattended-upgrades
alternatives.log.1  btmp                   dpkg.log          gpu-manager.log  mysql              wtmp
amazon              btmp.1                 dpkg.log.1        hp               speech-dispatcher  wtmp.1
apache2             cloud-init.log         flagtourteen.txt  kern.log         syslog             Xorg.0.log
apt                 cloud-init-output.log  fontconfig.log    kern.log.1       syslog.1           Xorg.0.log.old
auth.log            cups                   fsck              lastlog          syslog.2.gz        xrdp-sesman.log
bob@ip-10-10-73-24:/var/log$ cat flagtourteen.txt 
```

5. Can you find information about the system, such as the kernel version etc.
Find flag 15.

Personally speaking, I found this question a bit challenging as we can use the command `uname -a` to get the details related to kernel but it wasn't the answer to this question. Another way to check the kernel version that I found was through the file `/proc/version` but again this file also didn't contain the flag. Then I found out that depending on the OS, we can find the kernel version in `/etc` directory. For linux, it is stored in `/etc/lsb-release`.
```
bob@ip-10-10-73-24:~$ cat /etc/lsb-release
```

6. Flag 16 lies within another system mount.

Usually, when we mount on linux, it is done from the `/media` directory. We can explore the media directory to find the flag. And this time the flag has been stored in a really creative way. In the /media directory there is another directory named 'f' which further contains another directory named 'l'. We can see that this might lead to the word `flag`, so we can use `tab completion` and quickly browse till we get to the end of this directory tree.
```
bob@ip-10-10-73-24:/$ cd media/
bob@ip-10-10-73-24:/media$ ls
f
bob@ip-10-10-73-24:/media$ cd f
bob@ip-10-10-73-24:/media/f$ ls
l
bob@ip-10-10-73-24:/media/f$ cd l/a/g/1/6/is/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/
```
At the end of this directory chain we can find our required flag.

7. Login to alice's account and get flag 17. Her password is TryHackMe123

This question was really simple as all that was required to be done for this question was to switch the user to 'alice' and read the flag17.
```
bob@ip-10-10-73-24:/media/f$ su alice
Password: 
alice@ip-10-10-73-24:/media/f$ cd /home/alice/
alice@ip-10-10-73-24:~$ ls
flag17  flag19  flag20  flag22  flag23  flag32.mp3
alice@ip-10-10-73-24:~$ cat flag17
```

8. Find the hidden flag 18.

This question was again really easy. We know that all the hidden files start with '.'(fullstop) in Linux. And hidden files can be viewed using the command `ls -la`. So, in alice's directory we can check for hidden files and find the flag over there.
```
alice@ip-10-10-73-24:~$ cat .flag18 
```

9. Read the 2345th line of the file that contains flag 19.

To read a particular line in a file we can use the `sed` command and pass on the line number as a parameter to that command to read the specific line.
```
alice@ip-10-10-73-24:~$ sed -n 2345p flag19
```

### [Task 4] Data Representation, Strings and Permissions 

1. Find and retrieve flag 20.

We can see flag20 in alice's home directory. So, we can use `cat` to view it's content:
```
alice@ip-10-10-73-24:~$ cat flag20
MDJiOWFhYjhhMjk5NzBkYjA4ZWM3N2FlNDI1ZjZlNjg=
```
This appears to `base64` encoded. Hence, we need to decode it in order to obtain the flag. This can be done as:
```
alice@ip-10-10-73-24:~$ base64 -d flag20
```
The `-d` switch is used to decode the data in the file.

2. Inspect the flag21.php file. Find the flag.

First, we need to find the file as it is not present is alice's directory. 
```
alice@ip-10-10-73-24:~$ find / -name flag21.php 2> /dev/null
/home/bob/flag21.php
alice@ip-10-10-73-24:~$ cd /home/bob/
```
We can find the file in bob's directory. So, now we can `cat` the content of the file:
```
alice@ip-10-10-73-24:/home/bob$ cat flag21.php 
<?='MoreToThisFileThanYouThink';?>
```
But the content does not appear to be the flag but it does give a hint that there is something more related to this file in order to obtain the flag. So, we can use an editor like `nano` and check the content.
```
alice@ip-10-10-73-24:/home/bob$ nano flag21.php 
```
When we open the file in `nano` we can see the flag over there!


3. 	Locate and read flag 22. Its represented as hex.

First we need to find the file using the `find` command:
```
alice@ip-10-10-73-24:/home/bob$ find / -name flag22* 2> /dev/null
/home/alice/flag22
```
We can now print the content of the file but keep in mind the question has already mentioned that the data is in hex. Hence, we need to convert it to ASCII, which can be done by using `xxd`.
```
alice@ip-10-10-73-24:~$ cat flag22 
39 64 31 61 65 38 64 35 36 39 63 38 33 65 30 33 64 38 61 38 66 36 31 35 36 38 61 30 66 61 37 64
alice@ip-10-10-73-24:~$ xxd -r flag22
```
The `-r` switch is used to reverse from hex to ASCII

4. Locate, read and reverse flag 23.

We can find this flag in alice's directory itself. And when we print the content of this file we get a string that seems to be our flag but in the question it has been mentioned that we need to reverse the flag first before submitting. This can be done using the `rev` command:
```
alice@ip-10-10-73-24:~$ rev flag23
```

5. Analyse the flag 24 compiled C program. Find a command that might reveal human readable strings when looking in the source code.

First we need to locate the flag using the `find` command, which turns out to be in garry's directory. Now, as the question says the file is a C compiled program, there is no meaning in printing the content of the file. Rather we can use the `strings` command which is used to see the text inside a binary or data file.
```
alice@ip-10-10-73-24:/home/garry$ strings flag24
```
The output would contain a large number of lines, hence we need to look carefully for the flag in this output.

6. Flag 25 does not exist.

7. Find flag 26 by searching the all files for a string that begins with 4bceb and is 32 characters long. 

For this task, I was not able to make a proper command but found one on the internet which is:
```
find / -xdev -type f -print0 2>/dev/null | xargs -0 grep -E '^[a-z0-9]{32}$' 2>/dev/null
```

8. Locate and retrieve flag 27, which is owned by the root user.

For this question, we need to use the `find` command along with two switches `-name` and `-user` to pass the name of the file and the owner of the file. 
```
alice@ip-10-10-112-180:~$ find / -name flag27* -user root 2> /dev/null
/home/flag27
alice@ip-10-10-112-180:~$ cat /home/flag27
cat: /home/flag27: Permission denied
```
We don't have the access as alice to this file. So, we can check what all commands do we have access to with root privileges using the command `sudo -l`. 
```
alice@ip-10-10-112-180:~$ sudo -l
Matching Defaults entries for alice on ip-10-10-112-180.eu-west-1.compute.internal:
    env_reset, mail_badpass, secure_path=/usr/local/sbin\:/usr/local/bin\:/usr/sbin\:/usr/bin\:/sbin\:/bin\:/snap/bin

User alice may run the following commands on ip-10-10-112-180.eu-west-1.compute.internal:
    (ALL) NOPASSWD: /bin/cat /home/flag27
```
From this, we can see that we have root level access to read `flag27`, so if not as alice we can read it as root.
```
alice@ip-10-10-112-180:~$ sudo cat /home/flag27
```

9. Whats the linux kernel version?

The answer to this question can be easily found out by the command `uname -a`.
```
alice@ip-10-10-112-180:~$ uname -a
```

10. Find the file called flag 29 and do the following operations on it:

    Remove all spaces in file.
    Remove all new line spaces.
    Split by comma and get the last element in the split.

As usual, we will first locate the file using `find` command. But after that we need to perform some operations on the file. We can use `tr` command to remove spaces and new lines along with that `cut` command can be used to split by comma and get the last element.
```
alice@ip-10-10-112-180:~$ find / -name flag29* 2> /dev/null
/home/garry/flag29
alice@ip-10-10-112-180:~$ cat /home/garry/flag29 | tr -d " \n" | cut -d "," -f1
```

With the '|' the output of the former command is passed on as input to the later one. Now, the `tr` command is used for truncation and the `-d` switch is used to remove certain characters from the input, here we have mention " \n" (don't forget the blankspace before \n as we are asked to remove all spaces). The cut command is used to split the input based on certain delimiter characters that we pass to the command along with switch `-d`. The last value `-f1` finds and returns the first value from the end.

### [Task 5] SQL, FTP, Groups and RDP
1. Use curl to find flag 30.

This question is pretty straight forward, we just need to curl the IP address of the machine to get the flag.
```
alice@ip-10-10-112-180:~$ curl http://10.10.112.180
```

2. Flag 31 is a MySQL database name.

	MySQL username: root
	MySQL password: hello

For this question, we need to access MySQL and from there we can check the databases present on the system and the name of one of those would be our flag. The following commands show how to access it:
```
alice@ip-10-10-77-115:~$ mysql --user=root --password=hello
mysql: [Warning] Using a password on the command line interface can be insecure.
Welcome to the MySQL monitor.  Commands end with ; or \g.
Your MySQL connection id is 4
Server version: 5.7.25-0ubuntu0.16.04.2 (Ubuntu)

Copyright (c) 2000, 2019, Oracle and/or its affiliates. All rights reserved.

Oracle is a registered trademark of Oracle Corporation and/or its
affiliates. Other names may be trademarks of their respective
owners.

Type 'help;' or '\h' for help. Type '\c' to clear the current input statement.

mysql> show databases;
```
This will return a list of databases from which we can get our flag.

3. Bonus flag question, get data out of the table from the database you found above!

We need to first get into the database that we found in last question.
```
mysql> use database_xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx;
Reading table information for completion of table and column names
You can turn off this feature to get a quicker startup with -A

Database changed
```
Now the next task is to see the tables present in the database.
```
mysql> show tables;
+-----------------------------------------------------+
| Tables_in_database_xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx |
+-----------------------------------------------------+
| flags                                               |
+-----------------------------------------------------+
1 row in set (0.00 sec)
```
Here we can see that a table named `flags` is present in this database. To print the content of this table we can use a simple MySQL query.
```
mysql> select * from flags;
+----+----------------------------------+
| id | flag                             |
+----+----------------------------------+
|  1 | zzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzz |
+----+----------------------------------+
1 row in set (0.00 sec)

```
And we get the flag for this question.

4. Using SCP, FileZilla or another FTP client download flag32.mp3 to reveal flag 32.

For this question, we can use SCP through which we can download the file on our local system and listen to the .mp3 file.
```
tester@kali:~/Downloads/ctf$ scp alice@10.10.77.115:/home/alice/flag32.mp3 ~/Downloads
alice@10.10.77.115's password: 
flag32.mp3                                                           100%   10KB  63.6KB/s   00:00  
```
Here, we have downloaded the file by using the credentials of alice. The first path belongs to the file that we want to download from the local system whereas the sencond is the path where we want to store the file on our local system.

Once downloaded, we can listen to the file and get our flag.

5. Flag 33 is located where your personal $PATH's are stored.

All the personal $PATH's are stored in `~/.profile`, so we can check this file for every user and find the flag.
In this case, the flag was present in bob's .profile file.
```
alice@ip-10-10-77-115:/home/bob$ cat .profile 
```

6. Switch your account back to bob. Using system variables, what is flag34?

All the system variables are declare in `/etc/environment`. So, we can directly print that file and get our flag.
```
bob@ip-10-10-77-115:~$ cat /etc/environment 
```

7. Look at all groups created on the system. What is flag 35?

We know that all the groups on a system are stored in `/etc/group`. So, we can print that file and get our flag.
```
bob@ip-10-10-77-115:~$ cat /etc/group

```
In the output, we can a see a group whose name appears like a flag but that is not the answer. So, look proper at each group in the file.

8. Find the user which is apart of the "hacker" group and read flag 36.

We can use the `find` command and search for file to which 'hacker' group is given the access.
```
bob@ip-10-10-77-115:~$ find / -name flag36 -group hacker 2> /dev/null 
/etc/flag36
bob@ip-10-10-77-115:~$ cat /etc/flag36
```

And with this we have completed all the questions in Linux Challenge.

## Some Important Points to Take Away
1. `.bash_history` is a file that stores all the commands the user has run recently.
2. Cron jobs that are created can be found using `crontab -l` and a list of cron jobs can be found in `/etc/crontab`
3. All the system processes can be seen using the command `ps aux`.
4. Hostname resolutions can be created and/or edited in `/etc/hosts` file.
5. Alias can be found in `~/.bashrc`.
6. Files related to MOTD are stored in `/etc/update-motd.d` and the header is stored in `00-header`
7. All the logs in linux are stored in `/var/log` directory.
8. Different methods to check kernel version are:
	uname -a
	cat /proc/version
	cat /etc/lsb-release
9. Personal $PATH variables are stored in `~/.profile`.
10. All the system variables are stored in `/etc/environment`.
11. All groups on the system can be found in `/etc/group`