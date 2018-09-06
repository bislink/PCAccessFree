#!/usr/bin/perl 
#C:/Users/user03/public/OneFile/index.cgi 

use strict; 
use CGI qw/:standard/; 
use CGI::Cookie;
use Cwd qw();
use File::Basename qw();

#use warnings;
use CGI::Carp qw/fatalsToBrowser/; 

my $cwd = Cwd::abs_path();

my ($name, $path, $suffix) = File::Basename::fileparse($0);
$path =~ s!\\!\/!g;

my $users_userpass_dir = '';
my @path = ''; @path = split(/\//, $path);
$users_userpass_dir = "$path[0]/$path[1]/$path[2]/PCAccessFree2018";		# This is mostly C:/Users OR C:/inetpub. Either way, it is not publicly accessible to store user/pass files, temporarily.

my %sys;

%sys = (

# system URLS 

	script_url => "//$ENV{'SERVER_NAME'}:$ENV{SERVER_PORT}/$ENV{'SCRIPT_NAME'}",
	PCAccessMainUrl => "//$ENV{'SERVER_NAME'}$ENV{'SCRIPT_NAME'}",
	PCAccessAdminUrl => "admin.cgi",
	PCAccessSetupUrl => "setup.cgi",
	
# system related 

	script_name => "PC Access Free",	
	script_powershell => "C:\\Windows\\System32\\WindowsPowerShell\\v1.0\\powershell.exe",	
	script_users_folder => "$users_userpass_dir",
	script_dir => "$path",
	
	author => "hosting\@a1z.us",
	website => "https://www.a1z.us",
	bugs_url => "https://www.a1z.us/bugzilla/describecomponents.cgi?product=AccessYourPC",	
	
	dir_error => qq``,

# cookies 
	
	cookie_name => 'user',
	cookie_value => 'AccessYourPC',
    cookie_expiry => "+1h",
    cookie_domain => "user03.ns51.a1z.us",	          # CHANGE 
    cookie_path => "/",                               # MODIFY/UPDATE
    cookie_secure => 1                                # MODIFY/UPDATE

);

# include functions in %sys 
if ( -e -f "$path/lib/system_functions.txt" ) 
{
	open(SysFun, "$path/lib/system_functions.txt") or die $!;
	my @sf = <SysFun>;
	close SysFun;
	
	while ( my $function = <@sf> ) 
	{
		chomp $function;
		my ( $left, $right ) = split(/\=/, $function, 2);
		$sys{"$left"} = "$right";
	}
}

#Date 
my $date = '';
if ( $sys{enable_date_folder} )
{
	$date = `"$sys{script_powershell}" Get-Date -UFormat "%Y-%m-%d-%a-%H-%M-%S%Z"`; 
}
else 
{
	$date = "new-folder-$$";
}
chomp $date;


# Language 

my %lang;

my $default_language = '';

if ( -e -f "$sys{script_dir}/lang/default-language.txt" ) 
{
	open( LANG, "$sys{script_dir}/lang/default-language.txt") or die $!;
	$default_language = <LANG>;
	close LANG;
	chomp $default_language; 
}
else
{
	$default_language = 'en-us';
}

$default_language =~ s!\s+!!g;

if ( -e -f "$sys{script_dir}/lang/$default_language.txt" )
{
	open(DL, "$sys{script_dir}/lang/$default_language.txt" ) or die $!;
	my @dl = <DL>;
	close DL;
	
	##while ( my $item = <@dl> )                # gets only first word!!
	foreach my $item (@dl)                   
	{
		chomp $item;
		my ( $left_item, $right_value ) = split(/\=/, $item, 2);

		$lang{"$left_item"} = qq{$right_value};
	}
}
else
{
	$sys{lang_file_error} = "Could not open language file $default_language";
}

my $q = new CGI; 

#print $q->header( -charset => "utf-8");

# get cookie
my %cookies = (''); %cookies = fetch CGI::Cookie;
my $getUserCookie = ''; 
if ( %cookies ) 
{ 
	#$getUserCookie = $cookies{user}->value; 
	if ( $cookies{user} ) { $getUserCookie = $cookies{user}->value; }
} 
else { 
#&header1( cookie_status => 'set'); 
$getUserCookie = ''; 
}


use vars qw($a $b $c $d $e $f $g $h $i $f1 $action $path $j @j $title $url @url $total $i $folders $files @folders 
	@files @file $file $editfile @t $t @file2rename $file2rename $onebefore $firstOne $fileDate $con %fDate 
	$fa_temp1 $fa_temp2 $img @H $oneLess $prevDir $imgUrl $myURL @prevDir
	$safeChars $upDir $upFile $upHandle $url1 @G $f2nFile $f2nExt 
	$user $pass $u $p $curDir $file2create $folder2create @curDir $lastItem
	$Key $Cipher $ENCR $DECR
	@Last $last %u);

sub sys_vars 
{

#common for any server	
	$a = "C:/inetpub/wwwroot";

#other servers
	$f = "C:\\inetpub\\wwwroot";

# important vars used everywhere
	$myURL = "//$ENV{'SERVER_NAME'}$ENV{'SCRIPT_NAME'}";		#
	
# probably the most imp var; used in any
	$f1 = $q->param('f1');
	
# used in else, auth, authform

	$user = "$sys{script_user}"; 
	$pass = "$sys{script_password}";
	$u = $q->param('user');	#68
	$p = $q->param('pass');
	$g = "C:\\inetpub\\wwwroot";
}

$action = $q->param('action');		# this has to be here, otherwise first will not show results.  so $action has to be outside in order for subs to show results.

if ($q->param) 
{ 

	&sys_vars; 

	if ( $getUserCookie or ($u ne '' and $p ne '') ) #
	{ 
		if 	  ($action eq "first")          { &first; }           # nope. # if ($u eq $user && $p eq $pass){ else { &authForm; } }
		elsif ($action eq "list")           { &list; }
		elsif ($action eq "edit")           { &edit; }
		elsif ($action eq "write")	        { &write; }
		elsif ($action eq "rename") 	    { &rename; }
		elsif ($action eq "upload") 	    { &upload; } 		   # &upload_form is used to add upload form
		elsif ($action eq "doRename") 	    { &doRename; }
		elsif ($action eq "auth")           { &auth( cookie_status => "set"); }
		elsif ($action eq "createFile")     { &createFile; }
		elsif ($action eq "createFolder")	{ &createFolder; }
		elsif ($action eq "loginForm")	    { &authForm; }
		elsif ($action eq "registerForm")	{ \&registerForm; }		# '&reg' in &register is considered utf-8 code when transfered from pc to pc  
		elsif ($action eq "login")          { &auth; }
		elsif ($action eq "register")       { \&register; }	
		elsif ($action eq "CHMOD")          { &CMform; }		
		elsif ($action eq "doCM")           { &doCM; }			    # done 4:19 PM 9/11/2009
		elsif ($action eq "duplicate")      { &duplicateForm; }
		elsif ($action eq "doDuplicate")    { &doDuplicate; }	    # done 4:56 PM 9/11/2009
		elsif ($action eq "delete")         { &deleteForm; }
		elsif ($action eq "doDelete")       { &doDelete; }			# Done 5:12 PM 9/11/2009
		elsif ($action eq "logout")         { &logout(); }
	}
	else 
	{ 
		&authForm( title => "$lang{'session_expired'}", cookie_status => "get", body_cont => "$lang{too_many_session_expired} '$ENV{SERVER_NAME}'" ); 
	} 
	
}	#end if param
else 
{ 
	&authForm( cookie_status => "get" ); 
}							
#end if/else

# FORM 

sub form 
{
	&sys_vars;
	
	&header1("CMS by Bislinks");

	print "
<a href=$ENV{'SCRIPT_NAME'}?action=first&f=$a>$a</a>

<a href=$ENV{'SCRIPT_NAME'}?action=first&f=$f>$f</a>

	<form action='$ENV{'SCRIPT_NAME'}' method=post  accept-charset='utf-8' enctype='multipart/form-data'>
	<input type=hidden name=action value=first>
<input type=hidden name=user value=$u>
	<select name=\"f\">
	<option value=\"$a\">$a</option>
	<option value=\"$f\">$f</option>
	</select>
	<input type=submit value=OPEN>
	</form>
	";			#<input type=text value=\"$f\">
}

sub first 
{
	# this is necessary to get the script started with primary/root folder as provided by user.  For now, it gets it from sub form
	&sys_vars;

	$g = $q->param('f');
	&header1("First");

# if ($u eq $user && $p eq $pass){ # nope
	&any("$g");
#} #else { &authForm; } #nope
	&footer;
} 						#sub first

sub list 
{
	&sys_vars; 
	&header1( title => "Online File/Folder CMS by Bislinks");	

	&any("$f1");
	&footer;
} 						#sub list



# MAIN SUB 

sub any 
{	
	&sys_vars; 					#
	
	$g = qq~$_[0]~;			#  
	
	# change name according to where in the dir tree the use is in 
	$sys{NameOrViewInBrowser} = '';
	if ( $g =~ /inetpub\/wwwroot/ ) { $sys{NameOrViewInBrowser} = "View In Browser"; }
	else { $sys{NameOrViewInBrowser} = "Name"; }

	$url1 = &url("$g");

	if ( opendir(DIR, "$g") ) 
	{
		@G = readdir(DIR); 		# @G is used extensively in this sub for showing files and folders # does not work if moved to vars
		close DIR;
	}
	else 
	{
		print &dir_error("188");		# yes output 188
	}

	$total = scalar(@G); $total = $total - 2; # reduce . and .. #Symlinks are not shown in $total but are of course counted into it

	for (@G) #
	{ 
		push(@folders, $_) if (-d "$g/$_"); $folders = scalar(@folders);
		push(@files, $_) if (-f "$g/$_"); $files = scalar(@files);
	}

	$folders = &numFolders("$g");
	$folders = $folders - 3;		# -3 instead of -2 makes the count correct!!
	$files = &numFiles("$g");		        #$files = $files + 2;

	@H = (split/\//, $g, $#H);
	$oneLess = $#H - 1; 				    #print "oneLess=$oneLess"; #test ok
	$prevDir = join('/', @H[0..$oneLess]);	#

	
	# FOLDERS
	
	
	my $upDir = ''; $upDir = "$prevDir";
	if ( $upDir !~ /\// ) { $upDir .= qq`/`; }
	
	print qq{
<script async src="//pagead2.googlesyndication.com/pagead/js/adsbygoogle.js"></script>
<!-- pc browser free -->
<ins class="adsbygoogle"
     style="display:block"
     data-ad-client="ca-pub-8434162582137179"
     data-ad-slot="3296453589"
     data-ad-format="auto"
     data-full-width-responsive="true"></ins>
<script>
(adsbygoogle = window.adsbygoogle || []).push({});
</script>
	};
	
	print "<table id='A'>";
	
	# header/welcome/ad
	print qq`
	<tr>
		<td colspan="8"> 
			<table class="header-welcome">
				<tr>
					<td class="welcome-back">
						<button type="button" class="btn btn-primary btn-sm">$getUserCookie</button>
					</td>
					<td class="ads-or-message">

					</td>
					<td>
						<a href="$ENV{SCRIPT_NAME}?action=logout" title="Logout">$lang{logout}</a>
					</td>
				</tr>
			</table>
		</td>
	</tr>
	`; 
	
	print "<tr> <td width='10'>"; 

#UP DOWN A1

#colspan 1

	print qq{</td> <td colspan='7'>

		<table id='A1'>
			<tr>
			
				<td>					
					<form action='$ENV{'SCRIPT_NAME'}' method='post' accept-charset='utf-8' enctype='multipart/form-data'>
						<input type='hidden' value='list' name='action'>
						<input name='f1' value='C:/Users/user03' type='hidden'>
						<input type='hidden' name='user' value='$u'>
						<input type='submit' value='HomeDir'>
					</form>
				</td>
				<td>
						<form action='$ENV{'SCRIPT_NAME'}' method='post' accept-charset='utf-8' enctype='multipart/form-data'>
							<input type='hidden' value='list' name='action'>
							<input type='hidden' name='user' value='$u'>
							<input name='g' type='hidden' value='$g'>
						};
							print qq{<input name="f1" value="$upDir" type="hidden">} if (-d "$prevDir") && ($prevDir =~ /[a-zA-Z0-9]/);
							print qq{<input type='submit' value=\"UP: $upDir\">
						</form>
				</td>
				<td> 
						<button type="button" class="btn btn-secondary btn-sm cur-folder">$H[$#H]
							<span class="badge badge-pill badge-primary">$total</span> <span class="sr-only">Total including folders and files</span>
						</button>
				</td>
				<td>
					<form action='$ENV{'SCRIPT_NAME'}' method='post' accept-charset='utf-8' enctype='multipart/form-data'>
						<input type='hidden' value='list' name='action'>
						<input type='hidden' name='user' value='$u'>
						<input name='g' type='hidden' value='$g'>
						<input type='submit' value=\"Down:\">
						<select name='f1'>
					}; 												# 
						foreach (sort @G) 						#
						{ 
							print qq{<option value="$g/$_">$_</option>\n} if (-d "$g/$_") && ($_ =~ /[a-zA-Z0-9]/); 
						} 											#   
						print "</select>
					</form>
				</td>
			</tr>
		</table>	
	";
		
#colspan 2
	
	print "</td></tr><tr> <td width='10'>";  print "</td> <td colspan=7>"; 

# TOP FORMS 

		print "<table id='A2_fileForms'>
		<tr>";
			print "<td>"; &fileForm("$g");
			print "</td>  <td>"; &folderForm("$g");
			print "</td>  <td> "; &upload_form("$g"); 						# top upload form
			print "</td>
		</tr>
		</table>";

	print "</td></tr>
	<tr> <td width='10'>";  
	
# FOLDERS current folder 

#colspan 3

	print qq{<span class="badge badge-secondary">$folders</span> 
	</td> 
	<td colspan='7'> 
	}; # 
	
	#  	
	
		print "<table id='A3_foldersOperation'>";
		
			# Folders Header
		print qq{
		<tr> <td class="td-spacer" colspan="8"> <span class='cur-folder'>$H[$#H]</span> </td> </tr>
		
		<tr>
			<th>$sys{NameOrViewInBrowser}</th>
			<th>Change To</th>
			<th>Ren</th>
			<th>Copy</th>
			<th>Del</th>
		</tr>	
		};

		foreach (sort @G)	# display folders and operations on them <i class="fas fa-folder-open"></i>
		{

			$url1 = &url("$g");	# files/folders are accessible only when they are in server's web directory; otherwise you will see not found error!

			print qq{
			<tr>
				<td class='links'> 
					<a href=\"http://$ENV{'SERVER_NAME'}/$url1/$_\" title=\"$_\">$_</a> 
				</td> 
				<td> 
					<form action='$ENV{'SCRIPT_NAME'}' method='post' accept-charset='utf-8' enctype='multipart/form-data'>
						<input type=hidden value=list name=action>
						<input type=hidden name=user value='$u'>
						<input name=g type=hidden value='$g'>
						<input name=f1 type=hidden value="$g/$_">
						<button type="submit" class="badge badge-pill badge-secondary">Go</button>
					</form>
				</td> 
				<td> 
					<a href='$ENV{'SCRIPT_NAME'}?action=rename&f=$g/$_&user=$u'><span class="badge badge-pill badge-secondary">Ren</span></a> 
				</td> 
				<td> 
					<a href='$ENV{'SCRIPT_NAME'}?action=duplicate&f=$g/$_&user=$u'><span class="badge badge-pill badge-secondary">Copy</span></a> 
				</td> 
				<td> 
					<a href='$ENV{'SCRIPT_NAME'}?action=delete&f=$g/$_&user=$u'><span class="badge badge-pill badge-secondary">Del</span></a> 
				</td> 
			</tr>} if (-d "$g/$_") && ($_ =~ /[a-zA-Z0-9]/); 
		}

	print "</table></td></tr><tr> <td width='10'>";   
	
#colspan 4

	print qq{<span class="badge badge-secondary">$files</span> </td> <td colspan=7>};

		print "<table id='foldersOperation'>";
		
		# Files Header
		print qq{
		
		<tr> <td class="td-spacer" colspan="8"><span class='cur-folder'>$H[$#H]</span></td> </tr>
		
		<tr>
			<th>$sys{NameOrViewInBrowser}</th>
			<th>Size</th>
			<th>Edit</th>
			<th>Ren</th>
			<th>dup</th>
			<th>Del</th>
		</tr>	
		};

		foreach (sort @G) 								# list files
		{ 
			#file creation and modification date
			$con = (-C "$g/$_"); 
			$fDate{'sec'} = $con * 86400; 
			$fDate{'min'} = $con * 1440; 
			$fDate{'hr'}  = $con * 24; 
			$fDate{'day'} = $con; 
			$fDate{'wk'}  = $con / 7; 
			$fDate{'yr'}  = $con / 365; 
			$fa_temp1 = $^T - int((-M "$g/$_") * 86400);
			$fa_temp2 = $^T - int((-C "$g/$_") * 86400);
			$fDate{'mod'}  = localtime($fa_temp1);
			$fDate{'date'} = localtime($fa_temp2);
			$fDate{'size'} = -s "$g/$_";
			#$fDate{'size'} = ($fDate{'size'});

			$files = scalar(@G);

		# FILES
		
			print qq{
				<tr>
					<td class='links'> <a href=\"http://$ENV{'SERVER_NAME'}/$url1/$_\"> $_</a> </td> 
					<td><span class="badge badge-pill badge-info">$fDate{'size'}</span></td> 
					<td><a href='$ENV{'SCRIPT_NAME'}?action=edit&file=$g/$_&user=$u'><span class="badge badge-pill badge-secondary">Edit</span></a> </td> 
					<td><a href='$ENV{'SCRIPT_NAME'}?action=rename&f=$g/$_&user=$u'><span class="badge badge-pill badge-secondary">Ren</span></a> </td> 				
					<td> <a href='$ENV{'SCRIPT_NAME'}?action=duplicate&f=$g/$_&user=$u'><span class="badge badge-pill badge-secondary">Copy</span></a> </td> 
					<td> <a href='$ENV{'SCRIPT_NAME'}?action=delete&f=$g/$_&user=$u'><span class="badge badge-pill badge-secondary">Del</span></a> </td> 
				</tr>
			} if (-f "$g/$_"); 
		}	
		#
		
#colspan 5

	print "</table> </td> </tr> <tr> <td width='10'>";  
		print "</td> <td colspan=7>"; 
		print "<table id='bottomFileForms'>
			<tr>";
		print "<td>"; &fileForm("$g");
		print "</td> <td> "; &folderForm("$g");
		print "</td> <td> "; &upload_form("$g"); # bottom upload form
		print "</td></tr></table>";
	print "</td> </tr> <tr> <td width='10'>";  #

#colspan 6

	print "</td><td colspan=7>";

		print qq{
		<table id='ComingSoonPro'>
			<tr>
				<td> 
					Logged in as $getUserCookie. <a href='$ENV{SCRIPT_NAME}?action=logout' title='Logout'>Logout</a> \|
					<a href='$ENV{'SCRIPT_NAME'}'>$sys{script_name}</a> 
					<!--
					<a href=$ENV{'SCRIPT_NAME'}?action=getURL&curDir=$g>Get File from a URL</a>
					Create Multiple: <a href=$ENV{'SCRIPT_NAME'}?action=multipleFile&curDir=$g>Files</a>
					<a href=$ENV{'SCRIPT_NAME'}?action=multipleFolders&curDir=$g>Folders</a>
					<a href=$ENV{'SCRIPT_NAME'}?action=multipleUpload&curDir=$g>Upload</a>
					<a href=$ENV{'SCRIPT_NAME'}?action=download&curDir=$g>Download Folder</a>
					<a href=$ENV{'SCRIPT_NAME'}?action=backup&curDir=$g>Backup Folder</a>
					-->
				</td>
			</tr>
		</table>
		}; 						#add more links here

	print "</td></tr></table>";			
	#End Main Table
}								
# end any



sub edit 
{

	&header1( title => "EDIT");

	$curDir = $q->param('curDir');
	$file = $q->param('file');

	# create current dir by removing the last item in $file which also contains the dir path
	@curDir = (split/\//, $file, $#curDir);
	$oneLess = $#curDir - 1;
	$curDir = join('/', @curDir[0..$oneLess]); 

	$url1 = &url("$file");

	open (FILE, "$file") or print qq{<div class="alert alert-danger">Unable to open file. Error#577. $!</div>};
	@file = <FILE>;	
	close FILE; 

	print qq{
		<form action="$ENV{'SCRIPT_NAME'}" accept-charset=utf-8 enctype='multipart/form-data'> 
			<input type=hidden name=action value=write>
			<input type=hidden name=file value=$file>
			<input type=hidden name=user value=$u>
			<div class="form-group">
				<label for="editfile">Editing : $curDir[$#curDir]</label>
				<textarea class="form-control" name=editfile id="editfile">};   # do not move } down 
				foreach (@file) { $_ =~ s/\</\</g; $_ =~ s/\>/\>/g; print "$_"; }	# escape all '<' and '>'
				print qq{</textarea>
			</div>
			<div><button type="submit" class="btn btn-primary">MODIFY/UPDATE</button></div>
		</form>
	};
	
	&any("$curDir");
	
	&footer;

}

sub write 
{
&sys_vars;

my $error = '';

&header1( title => "write"); 
#&form;
$curDir = $q->param('curDir');
$file = $q->param('file');

# create current dir by eliminating the last item in $file which also contains the dir path
@curDir = (split/\//, $file, $#curDir); 
$oneLess = $#curDir - 1; 
$curDir = join('/', @curDir[0..$oneLess]); 

$editfile = $q->param('editfile');
chomp($editfile); 
my @editfile = split(/\n/, $editfile); 

open (FILE, ">$file") or $error = "$!";
#print FILE "$editfile"; 
for (@editfile) { print FILE qq~$_~; } 				# Sat Feb 21 10:43:47 2015
close FILE;									#Sat Feb 21 10:42:26 2015 
#unless (-x $file) { system `chmod 0755 $file`; }
if ( $error ) { print qq{<div class="alert alert-danger" role="alert">Error editing $file. Error#544. $error</div>}; }
else { print qq{<div class="alert alert-success" role="alert">Successfully wrote to $file</div>}; }
#&list; nope
#&edit; # ok but not necessarily needed
&any("$curDir");
&footer;
}

sub rename
{
&sys_vars;

&header1( title => "RENAME");
$file = $q->param('f');
@file2rename = (split/\//, $file, $#file2rename);
$onebefore = $#file2rename - 1;
$firstOne = join('/', @file2rename[0..$onebefore]);
print "<center> You have chosen to rename \"$file.\"  <br> 
	<form action=\"$ENV{'SCRIPT_NAME'}\" method=post accept-charset=utf-8 enctype='multipart/form-data'>
<input type=hidden name=user value=$u>

	<input type=hidden name=file value=$file>
	<input type=hidden name=action value=doRename>
	<input type=text name=f2nFile value=\"$firstOne/\">
	<input type=text name=f2nExt value=\"$file2rename[$#file2rename]\">
	<input type=submit value=RENAME>
	</form>
	</center>
	";											## $file2rename[$#file2rename - 1] # good idea

&footer;
}

sub doRename
{
&sys_vars;


&header1( title => "Done");

$f2nFile = $q->param('f2nFile');
$f2nExt = $q->param('f2nExt');
$file = $q->param('file');

`"$sys{script_powershell}" Rename-Item "$f2nExt" -Path "$file"`;

$last = &lastItem("$file");

print "<center> $last was renamed to $f2nExt successfully";
&any("$f2nFile");
&footer;

}

sub lastItem
{
@Last = (split/\//, "$_[0]", $#Last); 	# struggled for an hour for omitting one / in split by mistake
$last = $Last[$#Last];
return($last);
}


sub upload_form 						# upload_form is used in both top and bottom of sub any
{
print <<"END";
<form action="$ENV{'SCRIPT_NAME'}" method=post enctype="multipart/form-data">
<table valign=top align=center><tr><td>
<input type=hidden name=upDir value=\"$_[0]\">
<input type=hidden name=user value=$u>
<input type=file name=\"upFile\">
</td><td>
<input type=hidden name=action value=\"upload\">
<input type=submit value=Upload>
</td></tr></table>
</form>
END
}

sub upload
{
&sys_vars;

&header1( title => "Upload");

$CGI::POST_MAX = 1024 * 5000; 
$safeChars = "a-zA-Z0-9_.-"; 
$upDir = $q->param('upDir'); 
$upFile = $q->param('upFile');
$upFile =~ tr/ /_/; #had added an extra my here and it was not uploading at all spent two hours to figure this out
$upFile =~ s/[^$safeChars]//g; 
if ( $upFile =~ /^([$safeChars]+)$/ ) { $upFile = $1; } else { print "$upFile contains invalid characters"; } 
$upHandle = $q->upload("upFile"); 
open ( UPLOADFILE, ">$upDir/$upFile" ) or print "Error#4_$0_478_$$"; 
binmode UPLOADFILE; 
while ( <$upHandle> ) {  print UPLOADFILE; } 
print UPLOADFILE;
#close UPLOADFILE; 

# create thumbnail of uploaded file if it is an image. 
if ("$upDir/$upFile" =~ /.jpg|.JPG|.gif|.GIF/) 
	{ 
	#unless (-e "$upDir/$upFile" or "$upDir/t.$upFile") { print "$upFile already exists";} #still overwriting
	$url1 = &url("$upDir"); 
	system ('convert', '-geometry', "100 x 100", "$upDir/$upFile", "$upDir/t.$upFile"); 
	print "<center> $upFile uploaded successfully <br> <a href=\"http://$ENV{'SERVER_NAME'}$url1/$upFile\"> <img src=\"http://$ENV{'SERVER_NAME'}$url1/t.$upFile\" border=0 alt=\"Click to see Big\"> </a>" if (-e "$upDir/$upFile"); 
	}
elsif (-T "$upDir/$upFile")
	{
	$url1 = &url("$upDir"); 
	print "<center> $upFile uploaded successfully.  <a href=\"http://$ENV{'SERVER_NAME'}$url1/$upFile\">$upFile</a> ";
	}
elsif (-e "$upDir/$upFile")
	{
	$url1 = &url("$upDir"); 
	print "<center> $upFile uploaded successfully.  <a href=\"http://$ENV{'SERVER_NAME'}$url1/$upFile\">$upFile</a> ";
	}
else { print "Upload failed"; }

&any("$upDir"); # Perfect 
}

sub url
{
	$url = "$_[0]";

	# windows 7-3-18-1133
	$url =~ s!C:!!g; 
	if ($url ne '' and  $ENV{OS} =~ /Windows/i ) 
	{ 
		$url =~ s!/inetpub/wwwroot!!i; 		# OK
		$url =~ s!\\inetpub\\wwwroot!!i; 
	}
	
	return($url);
}


sub numFolders					# Get total number of folders only under the current folder displayed
{
	if ( opendir(DIR, "$_[0]") )
	{
		@G = readdir(DIR);
		close DIR;
		
		for (@G) 
			{ 
				push(@folders, "$_[0]/$_") if (-d "$_[0]/$_") and ("$_[0]/$_" =~ /[a-zA-Z0-9]/);
				$folders = scalar(@folders);
				return $folders;
			}
	}
	else 
	{
		# no output 668
	}
}

sub numFiles				# total number of files under current folder displayed
{
	if ( opendir(DIR, "$_[0]") ) 
	{
		@G = readdir(DIR);
		for (@G) 
		{ 
			push(@files, "$_[0]/$_") if (-f "$_[0]/$_") and ("$_[0]/$_" =~ /[a-zA-Z0-9]/);
			$files = scalar(@files);
			return($files);
		}
	}
	else 
	{
		# no output 687 
	}
}


sub fileForm
{

print <<"END";
<form action=\"$sys{script_url}\" method='post' accept-charset='utf-8' enctype='multipart/form-data'>
<table valign=top align=center><tr><td>
<input type=hidden name=user value=$u>
<input type=hidden name='curDir' value="$_[0]">
<input type=text name=\"file2create\" value=\"index.html\">
</td><td>
<input type=hidden name=action value=\"createFile\">
<input type=submit value=\"Create File\">
</td></tr></table>
</form>
</center>
END
}

# Create a folder form 
sub folderForm
{

print <<"END";
<form action=\"$sys{script_url}\" method='post' enctype=\"multipart/form-data\" >
	<table valign=top align=center>
		<tr>
			<td>
			<input type=hidden name=user value=$u>
			<input type=hidden name='curDir' value="$_[0]">
			<input type=text name=\"folder2create\" value=\"$date\">
			</td>
			<td>
			<input type=hidden name=action value=\"createFolder\">
			<input type=submit value=\"Create Folder\">
			</td>
		</tr>
	</table>
</form>

END

}

sub authForm
{
	# mostly common for every sub 
	my %in = (
		title => "$sys{script_name}",               # default title 
		cookie_status => "get",
		cookie_value => "",
		#cookie_get => $cookies{'user'}->value,      #
		@_,
	);
	
	#
	&sys_vars;
	
	# header1 includes cgi_header	
	# html : until </head><body>
	
	if ( $in{get_cookie} ) 
	{
		chomp $in{get_cookie};
		
		# open user.t and load/open user's default folder
		my $u = '';
		my @u = '';
		if ( -e -f "$sys{script_users_folder}/$in{get_cookie}.t" ) 
		{
			open(U, "$sys{script_users_folder}/$in{get_cookie}.t" ) or die "$sys{script_users_folder}/$in{get_cookie}.t";
			$u = <U>;
			close U;
			
			chomp $u;
			@u = split(/\|/, $u);
			
			&header1( title => "Already Logged In", cookie_status => "get" );
			&any("$u[2]" );
			&footer();
		}
		else 
		{
			&header1(title => "Cannot find/get $in{get_cookie}", cookie_status => "get");
			##&authForm();
			print qq{
				
				<h2>Cannot find/load user/cookie '$in{get_cookie}'</h2>
				
				<p>If you are not "$in{get_cookie}," please <a href="$ENV{SCRIPT_NAME}?action=logout">logout &amp; login again</a></p>
				
				<p>If that does not work, try deleting the "user/$in{get_cookie}" cookie from browser history and restarting your browser</p>
				
				<p>This is caused by a "browser cookie" that has not expired and needs to be removed</p>
				
				<div class="spacer"></div>
			};
			&footer();
		}
	}
	else
	{
	
		&header1( title => "$in{title}",  cookie_status => "$in{cookie_status}", cookie_value => "$in{cookie_value}" );

		print qq{
		
			<h2>$lang{login}</h2>
			
			<div class="spacer"></div>
		
			<form name=auth method=post action='$sys{script_url}' accept-charset='utf-8' enctype='multipart/form-data'>
				<input type=hidden name=action value=auth>
				<div class="form-group">
					<label for="user">Username</label>
					<input class="form-control" name=user id="user" type=text aria-describedby="user name" placeholder="Enter your user name">
				</div>
				<div class="form-group">
				<label for="pass">Password</label>
					<input class="form-control" name=pass type=password id="pass" aria-describedby="password" placeholder="Enter password">
				</div>
				<button type=submit value='LOGIN' class="btn btn-primary">Login</button>
			</form>
		
			<div class="spacer"></div>
			
			<div class="cookie">
				$in{get_cookie}
			</div>
			
			<div class="spacer">$in{body_cont}</div>
		
		};

		&footer();
	
	}
}

sub auth 
{
	&sys_vars;

	if ($u ne '' and $p ne '') 
	{ 
			if (open (USER, "$sys{script_users_folder}/$u.t") )	 
			{
				$u{'file'} = <USER>;
				chomp($u{file});
				
				( $u{'name'}, $u{'pass'}, $u{'dir'}, $u{'email'}, $u{the_rest} ) = ( split/\|/, $u{'file'} );
				
				( $u{'start_date'}, $u{'end_date'}, $u{'signup_ip'}, $u{'membership_level'}, $u{'membership_status'} ) = ( split/\|/, $u{the_rest}); 
				
				
				if ( $u eq $u{name} and $p eq $u{pass} ) 
				{
					if ( $getUserCookie eq $u{name} )
					{
						##&cgi_header(  );
						&header1( title => "$sys{script_name}", cookie_status => "get");
						&any("$u{dir}");
					}
					else
					{												
						##&cgi_header(  );
						&header1( title => "$sys{script_name}", cookie_status => "set", cookie_value => "$u{name}");
						&any("$u{'dir'}"); 
					
					}
				}
				else 
				{
					&authForm( title => "$lang{check_credentials}");
				}

			}
			else 
			{
				&authForm( message => "$u not found on this server" );
			}
	}
	else 
	{ 
		&authForm( message => "Username/Password cannot be empty" ); 
	}

	&footer;
}

sub createFile
{
&sys_vars;

&header1( title => "Create New File");
$curDir = $q->param('curDir');
$file2create = $q->param('file2create');
print "<center> $u, creating $file2create in $curDir <br> ";
if (-e "$curDir/$file2create") 
	{ print "Oops.  \"$file2create\" already exists.  <br> Please choose another file name to create."; 
	&any("$curDir");
	}
else 
	{ open (FILE, ">$curDir/$file2create") or print "Error#8_$0_627_$$"; 
	print " <br> $file2create created successfully
	To edit the file <a href='$ENV{'SCRIPT_NAME'}?action=edit&file=$curDir/$file2create'>Click Here</a>
	";
	close FILE;
	}

&footer;
}

sub createFolder
{
	&sys_vars;

	&header1( title => "Create Folder");

	$curDir = $q->param('curDir'); chomp $curDir;
	$folder2create = $q->param('folder2create'); chomp $folder2create; 

	if (-e -d "$curDir/$folder2create") 
	{ 
		print qq{<div class="alert alert-danger"> "$folder2create" already exists. Please choose another name </div>};	
			
		&any("$curDir");
	}
	else 
	{
		`"$sys{script_powershell}" New-Item -Path "$curDir/$folder2create" -ItemType "directory" -Force`; 
	
		print qq{<div class="alert alert-success">'$folder2create' was created successfully </div>};
	
		&any("$curDir");
	}

	&footer;

}

sub alphaNumImg
{
foreach (@_) 
	{ 
	#			path							first part		last part
	print "<img src=\"//bislinks.com/i/img/cms/";  print $_;  print "15.jpg\" height=10 border=0><br>"; 
	}
}

sub CMform
{
&sys_vars;
$file = $q->param('f');
@file2rename = (split/\//, $file, $#file2rename);
$onebefore = $#file2rename - 1;

$url1 = &url("$file");

&header1( title => "Change Mode of $file2rename[$#file2rename]");

$firstOne = join('/', @file2rename[0..$onebefore]);
print "<center> You have chosen to chmod \"$url1\"  <br> 

	<form action=\"$ENV{'SCRIPT_NAME'}\" method=post accept-charset=utf-8 enctype='multipart/form-data'>
	<input type=hidden name=user value=$u>
	<input type=hidden name=file value=$file>
	<input type=hidden name=action value=doCM>
	<input type=hidden name=CMfolder value=\"$firstOne\">
	<input type=hidden name=CMfile value=\"$file2rename[$#file2rename]\">
	<input name=CMvalue type=radio value=0744>Owner R W X
	<input name=CMvalue type=radio value=0754>Group R  X
	<input name=CMvalue type=radio value=0755>World R  X
<br> 
	<input type=submit value=\"Change File Mode of $file2rename[$#file2rename]\">
	</form>
	</center>
	";											## had to remove the extra forward slash in $firstOne in order to get proper folder path in up:

&footer;
}

sub doCM
{
&sys_vars;
$file = $q->param('file');						# this var is a must and it is submitted when user clicks on any of rename/chmod/edit/dup/del.  it is transfered from sub to sub using hidden forms (name=f value=$file or a variant of the same)
@file2rename = (split/\//, $file, $#file2rename);		# taken as is from sub rename wihtout changing the var name
$onebefore = $#file2rename - 1;

$url1 = &url("$file");

$u{'CMvalue'} = $q->param('CMvalue');				# in this sub, i have exclusively used %u
$u{'folder'} = $q->param('CMfolder');
$u{'file'} = $q->param('CMfile');

if ($u{'CMvalue'} eq "0744") { $u{'human_CMvalue'} = "<table valign=top align=center cellspacing=1 cellpadding=1 bgcolor=lightblue> <th bgcolor=white> Owner </th> <th bgcolor=white> Group </th> <th bgcolor=white> World </th> <tr bgcolor=white> <td> R </td> <td> R </td> <td> R </td> </tr>   <tr bgcolor=white> <td> W </td> <td>  </td> <td>  </td> </tr>    <tr bgcolor=white> <td> X </td> <td>  </td> <td>  </td> </tr></table> "; }
elsif ($u{'CMvalue'} eq "0754") { $u{'human_CMvalue'} = "Group R X"; }
elsif ($u{'CMvalue'} eq "0755") { $u{'human_CMvalue'} = "World R X"; }

&header1( title => "Successfully Changed Mode of $file2rename[$#file2rename]");

`chmod $u{'CMvalue'} $u{'folder'}/$u{'file'}`;

print "<center> Successfully changed mode of <b> ($file) $file2rename[$#file2rename] </b> to ( $u{'CMvalue'} ) $u{'human_CMvalue'}</center>";

&any("$u{'folder'}");

&footer;

}

sub duplicateForm
{
&sys_vars;
$file = $q->param('f');
@file2rename = (split/\//, $file, $#file2rename);
$onebefore = $#file2rename - 1;

$url1 = &url("$file");

&header1( title => "Make a copy of $file2rename[$#file2rename]");

$firstOne = join('/', @file2rename[0..$onebefore]);
print "<center> You have chosen to copy \"$url1\"  <br> 

	<form action=\"$ENV{'SCRIPT_NAME'}\" method=post accept-charset=utf-8 enctype='multipart/form-data'>
	<input type=hidden name=user value=$u>
	<input type=hidden name=file value=$file>
	<input type=hidden name=action value=doDuplicate>
	<input type=hidden name=CopyFolder value=\"$firstOne\">
	<input type=text name=CopyFile value=\"$file2rename[$#file2rename]\">

<br> 
	<input type=submit value=\"Copy $file2rename[$#file2rename] to above new file\">
	</form>
	</center>
	";											## had to remove the extra forward slash in $firstOne in order to get proper folder path in up:

&footer;

}

sub doDuplicate
{
&sys_vars;

$file = $q->param('file');						
@file2rename = (split/\//, $file, $#file2rename);		# 
$onebefore = $#file2rename - 1;

$url1 = &url("$file");

$u{'CMvalue'} = $q->param('CMvalue');				# in this sub, i have exclusively used %u
$u{'folder'} = $q->param('CopyFolder');
$u{'file'} = $q->param('CopyFile');

`"$sys{script_powershell}" Copy-Item "$file" -Destination "$u{'folder'}/$u{file}"`;

&header1( title => "$url1 copied to $u{'file'}");

print "<center> successfully copied $url1 to $u{'file'}";

&any("$u{'folder'}");

&footer;

}

sub deleteForm
{
&sys_vars;
$file = $q->param('f');
@file2rename = (split/\//, $file, $#file2rename);
$onebefore = $#file2rename - 1;

$url1 = &url("$file");

&header1( title => "Make a copy of $file2rename[$#file2rename]");

$firstOne = join('/', @file2rename[0..$onebefore]);
print "<center> You have chosen to delete \"$url1\" <h1> <font color=red> Are You Sure <br> Do you want to delete $url1? </font> </h1>   

	<form action=\"$ENV{'SCRIPT_NAME'}\" method=post accept-charset=utf-8 enctype='multipart/form-data'>
	<input type=hidden name=user value=$u>
	<input type=hidden name=file value=$file>
	<input type=hidden name=action value=doDelete>
	<input type=hidden name=deleteFolder value=\"$firstOne\">
	<input type=hidden name=deleteFile value=\"$file2rename[$#file2rename]\">

<br> 
	<input type=submit value=\"YES I AM SURE, DELETE $file2rename[$#file2rename]\">
	</form>
	</center>
	";											## had to remove the extra forward slash in $firstOne in order to get proper folder path in up:

&footer;

}

sub doDelete
{
&sys_vars;
$file = $q->param('file');						
@file2rename = (split/\//, $file, $#file2rename);		# 
$onebefore = $#file2rename - 1;

$url1 = &url("$file");

$u{'CMvalue'} = $q->param('CMvalue');				# in this sub, i have exclusively used %u
$u{'folder'} = $q->param('deleteFolder');
$u{'file'} = $q->param('deleteFile');

`"$sys{script_powershell}" Remove-Item -Path "$file" -Force`;

&header1( title => "$u{'file'} deleted");

print "<h2> successfully deleted $u{'file'} </h2> ";

&any("$u{'folder'}");

&footer;

}



sub header1
{
	my %in = 
	(
		title => "$sys{script_name}",
		cookie_status => "",
		cookie_value => "",
		@_,
	);
	
	$title = "$_[0]"; #shows the script path which i dont want 
	@t = (split/\//, $title, $#t);
	
	##print header( -charset => "utf-8" ); # deep recursion on subroutine main::header 
	
	&cgi_header( cookie_status => "$in{cookie_status}", cookie_value => "$in{cookie_value}");

	print qq{<!doctype html>
<html>
<head>

	<title>$in{title}</title>

	<meta charset="utf-8">
	<meta name="keywords" content="windows xp, windows 7, windows 8.1, windows 10, windows server 2012, file manager, blogs, hosted by a1z.us">
	<meta name="description" content="Windows file Manager by a1z.us">
	<meta name="viewport" content="width=device-width, initial-scale=1">

	<link rel="stylesheet" href="https://stackpath.bootstrapcdn.com/bootstrap/4.1.3/css/bootstrap.min.css" integrity="sha384-MCw98/SFnGE8fJT3GXwEOngsV7Zt27NXFoaoApmYm81iuXoPkFOJwJ8ERdknLPMO" crossorigin="anonymous">
	<link href="https://fonts.googleapis.com/css?family=Open+Sans+Condensed:300,300italic,700&amp;subset=latin,cyrillic-ext,latin-ext,cyrillic" rel="stylesheet" type="text/css">
	<link rel="stylesheet" href="https://netdna.bootstrapcdn.com/font-awesome/4.0.1/css/font-awesome.min.css">

	<link rel="stylesheet" href="index.css">

</head>

<body>

<h1>
	$sys{script_name}
</h1>

};

}

sub footer 
{
	my $out = '';
	
	my $server_info = ''; $server_info = &server_info();
	
	my $browser_info = ''; $browser_info = &browser_info();
	
	print qq~
	
		<div class="spacer">
			$lang{help_us_improve} <a href="$sys{bugs_url}" title="$lang{help_us_improve}">$lang{bugs} $lang{here}</a>
		</div>
		
		<div class="spacer">
			&copy; &nbsp; &nbsp; 
			<button 
				type="button" class="btn btn-sm btn-info" data-html="true" data-toggle="popover" title="Server Info"
				data-content='$server_info' 
			>
				$ENV{'COMPUTERNAME'}/$ENV{'SERVER_NAME'}
			</button>
		</div>
		
		<div class="spacer dev-error">
			$sys{lang_file_error}   
		</div>
		
		<div class="spacer browser">
			$browser_info
		</div>
		
		<script src="https://code.jquery.com/jquery-3.3.1.min.js" integrity="sha256-FgpCb/KJQlLNfOu91ta32o/NMZxltwRo8QtmkMRdAu8=" crossorigin="anonymous"></script>
		<script src="https://cdnjs.cloudflare.com/ajax/libs/popper.js/1.14.3/umd/popper.min.js" integrity="sha384-ZMP7rVo3mIykV+2+9J3UJ46jBk0WLaUAdn689aCwoqbBJiSnjAK/l8WvCWPIPm49" crossorigin="anonymous"></script>
		<script src="https://stackpath.bootstrapcdn.com/bootstrap/4.1.3/js/bootstrap.min.js" integrity="sha384-ChfqqxuZUCnJSK3+MXmPNIyE6ZbWh2IMqE241rYiqJxyMiZ6OW/JmZQ5stwEULTy" crossorigin="anonymous"></script>

		<script src="index.js"></script>
		
		<script>
		
			\$(function () {
				\$('[data-toggle="popover"]').popover()
			});
			
			\$(function () {
				\$('[data-toggle="tooltip"]').tooltip()
			});
			
		</script>
		
		</body>
		
		</html>
	~;
}


sub dir_error 
{
	 my $dir = shift;
	 
	 return qq`
	 <div class="error">
		<p>
			Unable to open dir, error #$dir. 
			<a href="//$ENV{SERVER_NAME}/$ENV{SCRIPT_NAME}"></a> 
			Click or touch &nbsp; <span class="highlight">UP: C:/</span> &nbsp; below to go to your home directory.
		</p>
	 </div>`;
}


sub logout 
{
	# authform 
	&authForm( title => "Logout", cookie_status => "delete" );		# includes cgi_header 
}


sub cgi_header
{

=head1 cgi_header 
	Can be used to set, get, or delete a cookie.
=head1 Usage 
	header1 includes this sub! So, usage would be 
	&header1( .... );
=cut

	my %in = (
		cookie_value => "",
		cookie_status => "get",
		@_,		
	);
	
	my %coo = '';
	
	if ( $in{cookie_status} eq 'set') 
	{
		
		$coo{set} = new CGI::Cookie
		(
			-name    =>  "$sys{cookie_name}",
			-value   =>  $in{cookie_value},
			-expires =>  "+10m",
			-domain  =>  "$sys{cookie_domain}",
			-path    =>  "$sys{cookie_path}",
			-secure  =>  $sys{cookie_secure}
		);
	
		print header( -charset => "utf-8", -cookie => $coo{set} ); 

	}
	elsif ( $in{cookie_status} eq 'delete' )
	{
		$coo{delete} = new CGI::Cookie
		(
			-name    =>  "$sys{cookie_name}",
			-value   =>  $in{cookie_value},
			-expires =>  "-3M",
			-domain  =>  "$sys{cookie_domain}",
			-path    =>  "$sys{cookie_path}",
			-secure  =>  $sys{cookie_secure}
		);
	
		print header( -charset => "utf-8", -cookie => $coo{delete} );
	}
	else 
	{
		print header( -charset => "utf-8"); 
	}
}

# browser info via popover
sub browser_info 
{
	my %in = (
		ad_html => qq{},
		@_,
	);
	 
	my $out = '';
	
	$out .= qq{<table class="table table-responsive table-sm browser-info">};
	for (sort keys %ENV)
	{
		if ( $_ =~ /(http_|gate|remote)/i ) 
		{ 
			$out .= qq{<tr> <td>$_</td> <td>$ENV{$_}</td> </tr>} if ( $_ and $ENV{$_} );
		}
	}
	$out .= qq{</table>}; 
	
	if( $sys{enable_browser_info} ) 
	{
		return qq{<button type="button" class="btn btn-sm btn-info" data-toggle="popover" title="Browser Info" data-html="true" data-content='$out'>Browser Info</button>}; 
	}
	else 
	{
		return qq{Your IP: $ENV{REMOTE_ADDR} };
	}
	
}

sub server_info 
{
	my %in;
	
	my $out = '';
	
	%in = (
		info => '',
		@_,
	);
	
	$out .= qq{<table>};
	
	for (keys %ENV ) { $out .= qq{<tr> <td>$_</td> <td>$ENV{"$_"}</td> </tr>} if ( $_ and $ENV{$_} and $_ =~ /server/i ); }
	
	$out .= qq{
			<tr> <td>Proc</td>    <td> $ENV{'PROCESSOR_ARCHITECTURE'}</td> </tr>		
	};
	
	$out .= qq{</table>};
	
	if( $sys{enable_server_info} ) 
	{
		return qq{$out}; 
	}
	else 
	{
		return qq{$lang{server_info_disabled} <a href="$sys{PCAccessAdminUrl}" title="$lang{script_name}">$sys{script_name} Admin</a> };
	} 
}



1;
