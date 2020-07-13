## NMAP
Continuing with another box on TryHackMe, as the name suggests this time it is [Nmap](https://nmap.org/). In my last writeup ([Vulnversity](https://github.com/n00b-0x31/TryHackMe-Writeups/blob/master/Vulnversity/vulnversity_writeup.md)), there was a part where nmap was used but it had a brief role over there. With this room ([Nmap](https://tryhackme.com/room/rpnmap)) on THM we can develop our nmap skill further.

#### What is nmap?
As per Wikipedia (https://en.wikipedia.org/wiki/Nmap), it a free open-source network scanner which can be used to discover hosts and services on a computer network by sending packets and analyzing responses. But once we start using nmap to it's fullest, we can see that it can be used for many more things like OS detection, encryptions being used, testing scripts and many more things. Basically, it is one of the most used tools to perfrom reconnaissance on any given target/s.

So, let's begin with the room now!

### [Task 1] Deploy
We need to deploy the machine in order to gain access to it and nothing more is required in this task.

### [Task 2] Quiz
In this task there are a number of questions that arranged in a way that we can get a better grip on the mostly used nmap switches. Remember for any help `man nmap` is always there.
As this room is pretty straightforward and there is not much to discuss about, we can look into each switch's meaning at somewhat detailed level.

1. Accessing the Help Menu: `-h`
  * With `nmap -h`, we can see all the various switches and their brief description. This can come in handly when we don't feel like going through the manual and just want to check the switch that we want.
  
2. Stealth Scan: `-sS`
	```
	nmap -sS <target_ip>
	```
	* It is the default and most popular type of scan. As the name suggest it can perform the scan in a stealth mode as it never opens a full TCP connection.

3. UDP Scan: `-sU`
	```
	nmap -sU <target_ip>
	```
	* With this switch we can perform scan on the target machine's UDP port. This scan works by simply sending a UDP packet to every port on the target machine and analyzing the response.
	
4. Operating System Detection: `-O`
	```
	nmap -O <target_ip>
	```
	* With this switch, we can directly detect the OS that the target machine is running. Sometimes, nmap is not able to detect the exact OS but it might provide some suspected OS's that might be running on the target.

5. Service Version Detection: `-sV`
	```
	nmap -sV <target_ip>
	```
	* With this switch, we can detect the version of the service running on the open ports. Also, with the help of this information we can diffrentiate between truly open ports and filtered ports.

6. Being Talky (Verbose): `-v`
	```
	nmap -v <target_ip>
	```
	* Sometimes we want to know what is going on in the backgound of the running scan and in such cases the verbose switch turns out to be really helpful.

7. Very Verbose: `-vv`
	```
	nmap -vv <target_ip>
	```
	* This switch provides even greater verbosity and much more detailed insights into the processes running in the background of a scan.
	
8. Saving Output in XML File: `-oX`
	```
	nmap -oX <target_ip>
	```
	* When performing the scan it can be handy to save the output of the scan so that it can used in future to check some major or minor details of the scan.

9. Aggressive Scan: `-A`
	```
	nmap -A <target_ip>
	```
	* When want in depth details of a scan we can use this switch as it is capable of performing OS detection, version detection, script scanning and traceroute all together.
	
10. Max Scan Speed: `-T5`
	```
	nmap -T<0-5> <target_ip>
	```
	* We can adjust the speed of the scan using the speed template. These range from 0 to 5 with 0 T4 being the slowest and T5 being the fastest. One thing to keep in mind here is that faster the scan, more are the chances that we can miss on some details in the scan.
	
11. Specific Port: `-p`
	```
	nmap -p<single port number or range> <target_ip>
	```
	* With this switch we can perform scan on a single port like `-p80` or over a range of ports like `-p100-2000`.

12. Scanning All Ports: `-p-`
	```
	nmap -p- <target_ip>
	```
	* While running a scan to detect all the open ports, we need to perform a check on all the ports. And in such a case we can use the switch `-p-` to run the scan over all the ports.
	
13. Script Scan: `--script`
	```
	nmap --script <scrip_name> <target_ip>
	```
	* Nmap has a large variety of scripts that can check for various vulnerabilites and perform various detections.

14. Running Vulnerability Scripts: `--script vuln`
	```
	nmap --script vuln <target_ip>
	```
	* There are many categories of scripts in nmap that are seggregated in various categories like auth, broadcast, exploit, fuzzer, vuln and many other.

15. Scan Without Ping: `-Pn`
	```
	nmap -Pn <target_ip>
	```
	* With this switch nmap skips the discovery stage which is used to determine active machines for heavier scanning. When this switch is specified, nmap is forced to perform scan against every target IP address specified.
	
### [Task 3] Nmap Scanning
This section consists of various tasks that are needed to be performed on the actual deployed machine. I've explained the switch that are used:

