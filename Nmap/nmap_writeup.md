## NMAP
Continuing with another box on TryHackMe, as the name suggests this time it is [Nmap](https://nmap.org/). In my last writeup ([Vulnversity](https://github.com/n00b-0x31/TryHackMe-Writeups/blob/master/Vulnversity/vulnversity_writeup.md)), there was a part where nmap was used but it had a brief role over there. With this room ([Nmap](https://tryhackme.com/room/rpnmap)) on THM we can develop our nmap skill further.

#### What is nmap?
As per Wikipedia (https://en.wikipedia.org/wiki/Nmap), it a free open-source network scanner which can be used to discover hosts and services on a computer network by sending packets and analyzing responses. But once we start using nmap to it's fullest, we can see that it can be used for many more things like OS detection, encryptions being used, testing scripts and many more things.

So, let's begin with the room now!

### [Task 1] Deploy
We need to deploy the machine in order to gain access to it and nothing more is required in this task.

### [Task 2] Quiz
In this task there are a number of questions that arranged in a way that we can get a better grip on the mostly used nmap flags. Remember for any help `man nmap` is always there.
As this room is pretty straightforward and there is not much to discuss about, we can look into each flags meaning at somewhat detailed level.

1. Accessing the help menu: `-h`
