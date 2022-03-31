# PCAccessFree (Windows Version)

Convert your personal computer (Windows 7, 8, 10, 11) into a file server, Windows File Manager,
Content Management System, et cetera.

Created using Perl (CGI, Mojolicious, DBI), Bootstrap, JavaScript, and SQL programming languages.

## Internet Information Services

### Search/open 'Turn Windows features on or off'

```
Select all .NET frameworks
Select all features in Internet Information Services
Select Internet Information Services Hostable Web Core
Click OK
Wait for installation to complete, restart your PC if asked to
```

## Perl

### Download/install Perl from Strawberry Perl

https://strawberryperl.com/download/5.32.1.1/strawberry-perl-5.32.1.1-64bit.msi

### Open PowerShell as Administrator and run the following command.

```
cpan CPAN CGI DateTime DBI DBIx::Class Cpanel::JSON::XS EV IO::Socket::Socks Role::Tiny Future::AsyncAwait Log::Log4perl Mojolicious  Mojolicious::Plugin::RemoteAddr
```

### After the completion of the above command, test with

```
mojo version
```

which should produce an output similar to the following

```
PS C:\inetpub\wwwroot\PCAccessFree> mojo version
CORE
  Perl        (v5.32.1, MSWin32)
  Mojolicious (9.22, Waffle)

OPTIONAL
  Cpanel::JSON::XS 4.09+   (4.25)
  EV 4.32+                 (4.33)
  IO::Socket::Socks 0.64+  (0.74)
  IO::Socket::SSL 2.009+   (2.069)
  Net::DNS::Native 0.15+   (n/a)
  Role::Tiny 2.000001+     (2.002004)
  Future::AsyncAwait 0.52+ (0.54)

You might want to update your Mojolicious to 9.23!
PS C:\inetpub\wwwroot\PCAccessFree>
```

## Setup Perl handler mapping in IIS

```
Search/open IIS as Administrator
Expand Sites
Select Default Web Site
Double click Handler Mappings on the right side
Edit feature permissions
Select Execute
click OK
Click Add Script Map
Request Path: *.cgi
Executable: C:\Strawberry\perl\bin\perl.exe "%s" %s
Name: Perl For PCAccessFree
Click Request Restrictions
Mapping Tab: Invoke handler only if request is mapped to: File
Verbs Tab: All verbs
Access Tab: Execute
click OK multiple times - Yes to all
```

### Video

https://youtu.be/hsmAqw08-aQ

## Set User for IIS

### Fixes `permission denied` error when saving settings via `nologin.cgi`:

```
Open IIS as Administrator
Under 'connections,' select 'default web site' under 'Sites'
Under 'actions,' click 'basic settings'
Click 'connect as'
select 'specific user'
Click 'set' and provide a valid username/password for your first windows user account
Click OK to Save
OK Again to exit
```

### Now, go back to 'nologin.cgi' and edit/save 'system_functions' again.

This time, you should not see 'permission denied' if you followed above instructions correctly.



## Install Git

### Download/Install Git for Windows

https://github.com/git-for-windows/git/releases/download/v2.35.1.windows.2/Git-2.35.1.2-64-bit.exe



## Get/install PC Access free on your computer

### Download/install app from any of the following public repositories

#### In PowerShell, with administrative privileges, run one of the following commands

* cd C:/inetpub/wwwroot

* git clone https://github.com/bislink/PCAccessFree.git

* git clone https://bislinks.visualstudio.com/PCAccessFree

* git clone https://gitlab.com/bislink/pc-access-free.git


## Install nodejs

Please download/install https://nodejs.org/dist/v16.14.2/node-v16.14.2-x64.msi



## Install jQuery, Bootstrap via `npm`


### On a PowerShell with administrative privileges, run

```
cd C:/inetpub/wwwroot/PCAccessFree/public
npm install @popperjs/core jquery bootstrap
```


## Test/Run PC Access Free App

### PC Access Free runs on your browser

### Open your favorite browser and open the following URL in a new tab:

http://localhost/PCAccessFree/nologin.cgi

#### Set/enable features

##### Alternatively, you can save the following lines `as they are` in `C:/inetpub/wwwroot/PCAccessFree/lib` as `system_functions.txt`

```
cookie_domain=localhost
cookie_expiry=+3M
css_js_url=//localhost/
enable_browser_info=1
enable_cookie_secure=1
enable_date_folder=1
enable_server_info=1
language=en-us
password_dir=C:/inetpub/PCAF22
script_web_dir=C:/inetpub/wwwroot/PCAccessFree
server_port=80
user_pref_home_dir=C:/inetpub/wwwroot/PCAccessFree
web_root=C:/inetpub/wwwroot
web_root_url=//localhost
```

### After saving the changes, in case the default `username.t` file is not created:

See permission denied section above.

#### Open File Explorer and create directory `PCAF22` in `C:/inetpub`

```
cd C:/inetpub;
mkdir PCAF22
```
OR

```
New-Item -Path "C:/inetpub/PCAF22" -ItemType "directory" -Force`
```

#### create a file named `username.t` in `C:/inetpub/PCAF22`

##### Add a single line in the following format and save it:

```
username|pas2W0rd|C:/inetpub/wwwroot|http://localhost
```

###### Make sure you do not save file with `.txt` extension but with `.t` extension.

### open the following url in a new tab in your favorite browser:

```
http://localhost/PCAccessFree/index.cgi
```

#### Log in with the credentials you just created.

### Have fun using PC Access Free on your laptop/pc


## How to update to latest version?

```
Open PowerShell as Administrator
cd C:/inetpub/wwwroot
git pull
```





# PC Access Free optional customizations

## Import SSL Certificate

### Assuming, you have downloaded `YOURNAME.bislinks.com.pfx` file to your computer, e.g., to `C:/Users/USER/Documents` from https://pca.bislinks.com/download-pfx.html

```
Open IIS as Administrator
Under Connections, Click on your main IIS Server Connection, usually your computer name
In the middle pane, double click "Server Certificates"
Under Actions, click 'import'
In the 'import certificate' dialogue, under 'certificate file .pfx,' select location `c:/Users/USERNAME/Documents`
and select .pfx file you just downloaded
```

### Video

https://youtu.be/QMqcQB_aGDg



## Add HTTPS

```
Open IIS as Administrator
Under connections, selet your site
Under Actions, click bindings
Under Actions, click bindings
Under Site Bindings, click add
Under Type, select https
Under IP Address, Select "All Unassigned"
Under Port, leave it as 443 or assign a custom port above 10000, e.g., 21202 or 20443 or 30443 or 40443
Under SSL Certificates, Select free.pca.bislinks.com
Check "Disalbe HTTP/2" in order to disable http2
Clcik OK to save
Click close to close Site Bindings.

```


## Disable http2 in IIS

### For SSL sites only

```
Open IIS as Administrator
Under connections, selet your site
Under Actions, click bindings
Under Site Bindings, Select https and click edit
Check/enable the "Disable HTTP/2" option
```

### Video

https://www.youtube.com/watch?v=EwIRbf-9emY
