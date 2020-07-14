## OWASP Top 10 
This writeup is going to be based on the [OWASP Top 10](https://tryhackme.com/room/owasptop10) room on TryHackMe. The challenges to this room are going to be released on daily basis, so that for 10 days one can focus on one of the Top 10 vulnerabilities whichever has been released for that day. I will try to add every vulnerability task to this article as soon as I complete it.

### What is OWASP and what are the Top 10???
Open Web Application Security Project or better known as [OWASP](https://owasp.org/) is an online community that produces tools, documentations, technologies and many other things related to web security which can be accessed by anyone and at cost-free rate. Some of the major OWASP projects that I know are [ZAP](https://www.zaproxy.org/), [Juice Shop](https://github.com/bkimminich/juice-shop), obviously the [Top 10](https://owasp.org/www-project-top-ten/) and many other.

Coming to OWASP Top 10
OWASP releases this document called as OWASP Top 10 which consists of most critical security risks to web applications. There are many versions of this document released in the past well. Going through this document would help any individual to develop a better insight regarding some of the major vulnuerabilities on the web and not only how to exploit them but also how to protect yourself from those vulnerabilites.

Coming to this room, it does not require any prerequisite knowledge related to these vulnerabilites but one can easily develop some knowledge regarding them. Moving on let's get started with the `OWASP Top 10` room!

### [Task 1] Introduction
This task just provides a list of all the vulnerabilites that are going to be covered in this room.

1. Injection
2. Broken Authentication
3. Sensitive Data Exposure
4. XML External Entity
5. Broken Access Control
6. Security Misconfiguration
7. Cross-Site Scripting
8. Insecure Deserialization
9. Components With Known Vulnerabilities
10. Insufficient Logging and Monitoring

#### Task 2 and 3 are just related to VPN access and daily prize. So, nothing important here.

### [Task 4] Injection
This is the point from where all the interesting stuff begins. In this task, they have briefed about what is Injection, how it can be performed and how to defend youself from such attacks. Folowing are some major points from the decription they have provided:

* There are broadly two types of injection attacks:
	* SQL Injection: When you exploit some weakness in SQL or database implementation in a web application.
	* Command Injection: When you exploit the web app implementation at system level and run system level command.
* Once such injection attacks are successfully performed, an attacker can easily access, modify or delete important data and sometimes even confidential data as well.
* Considering the protection from such attacks, the best way is to sanitize all the data from every possible entry-point before it gets processed or executed.

### [Task 5] Command Injection
This task provides brief introduction to command injection. One important point described over here is that once an attacker gets access to the system it is not necessary that he/she will perform some simple malicious tasks like `whoami` or some other system level commands but he/she can also try to pop a shell for themselves and virtual own all the data stored on that server which can be pretty dangerous in sevel ways.

### [Task 6] Command Injection Practical
This task is all about the practical implementation of Command Injection. Though one important thing to be noted here is that you will never find such an easy way to perform command injection out in the real world, this is just for basic practice and develop a simple mindset for such attack.

The task talks about a simple code snippet that is running behind the URL through which we will be performing command inection. Also, a few windows and linux commands are provided which can be tested while perform command injection. Now, the most interesting part THE PRACTICAL IMPLEMENTATION!!!!

First of all, deploy the machine and browse to the URL: http://<machine_ip>/evilshell.php which would look something like:

![EvilCorp]()
1. This question asks about an odd file present in the web root directory. Keep in mind it is asking about the `WEB ROOT` directory and not the `ROOT` directory. With the command `pwd` we get the result as `/var/www/html` which is the `WEB ROOT` directory. All that needs to be done here is just to run the `ls` command to get a list of all the files present in this diretory and and find the odd file out.

2. 
