# Necessary Software Installation Instructions

## Iinternet Information Services

See README.md

## Git For Windows
Download and install

https://github.com/git-for-windows/git/releases/download/v2.35.1.windows.2/Git-2.35.1.2-64-bit.exe

Restart PowerShell and/or PC after installation is complete

## Run install.ps1 for the following msi packages

cd C:/inetpub/wwwroot/PCAccessFree
./install.ps1

and follow instructions

## Strawberry Perl MSI package

Included in install.ps1

## Node.js MSI package

included in install.ps1

## MariaDB MSI package

Included in install.ps1

### Suggested parameters for MariaDB Server Setup

Select/check 'use utf-8 as default character set for server'
Service Name: MariaDB106
Port: 3308
Password: draryapyolrajcob

### After installation of MariaDB Server

Search for MariaDB
Run MySQL Client (MariaDB 10.6 x64 )
enter password you provided during installation

#### Database Setup

#### Suggested Paramaters for database, username, and password

```
Enter password: ****************
Welcome to the MariaDB monitor.  Commands end with ; or \g.
Your MariaDB connection id is 4
Server version: 10.6.7-MariaDB mariadb.org binary distribution
Copyright (c) 2000, 2018, Oracle, MariaDB Corporation Ab and others.

Type 'help;' or '\h' for help. Type '\c' to clear the current input statement.

MariaDB [(none)]> create database mojocms;
Query OK, 1 row affected (0.002 sec)

MariaDB [(none)]> create user mojocms identified by 'Mojo4Cms,22032';
Query OK, 0 rows affected (0.005 sec)

MariaDB [(none)]> grant all on mojocms.* to mojocms;
Query OK, 0 rows affected (0.008 sec)

MariaDB [(none)]>

```

#### settings.txt

Open C:/inetpub/wwwroot/PCAccessFree/lib/Database/settings.txt
and make sure the parameters set in this file match above settings

#### Open admin.cgi

Now access 'http://localhost/PCAccessFree/admin.cgi' in your favorite browser.

This page will show error if Database is not installed and/or `settings.txt` is not setup properly 
