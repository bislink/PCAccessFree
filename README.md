# PCAccessFree (Windows Version)

Convert your personal computer (Windows 7, 8, 10, 11) into a file server, Windows File Manager,
Content Management System, et cetera.

Created using Perl/Mojolicious, Bootstrap, JavaScript, and SQL programming languages.

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
cpan CPAN CGI DateTime DBI DBIx::Class Cpanel::JSON::XS EV IO::Socket::Socks Net::DNS::Native Role::Tiny Future::AsyncAwait Mojolicious
```

### After the completion of the above command test with

```
mojo version
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

## Git

### Download/Install Git for Windows

https://github.com/git-for-windows/git/releases/download/v2.35.1.windows.2/Git-2.35.1.2-64-bit.exe

## PC Access free

### Download/install app from any of the following public repositories

#### In PowerShell, with administrative privileges, run one of the following commands

* cd C:/inetpub/wwwroot

* git clone https://github.com/bislink/PCAccessFree.git

* git clone https://bislinks.visualstudio.com/PCAccessFree

* git clone https://gitlab.com/bislink/pc-access-free.git


## Test/Run App

### Open your favorite browser and open the following URL in a new tab:

http://localhost/PCAccessFree/admin.cgi/nologin

#### Set/enable features

##### Alternatively, you can save the following lines as they are in 'C:/inetpub/wwwroot/lib' as 'system_functions.txt'

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

### After saving the changes,

#### Open File Explorer and create directory

```
C:/inetpub/PCAF22
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

#### Loging with the credentials you just created.

## Have fun using PCAccessFree!
