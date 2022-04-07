#!C:\\Strawberry\\perl\\bin\\perl5.26.1.exe

=head1 PCAccessFree
	admin.cgi
	created especially for Windows operating systems.
	PCAccessFree brings your windows pc to your browser.
		Shows all files right inn your favorite browser.
		Easily open all files contained in IIS/public directoreies
		Add users to windows system.
		Store notes
		create/maintain a personal blog
		A complete content management system written in Perl/Mojolicious for Windows.
	Tested in windows 11, windows 10, and partially in windows 2016
=head2 Open Source
	Source code is shared on 4 different open source providers
		Git Hub
			where I maintain all bugs
		Git Lab
		Windows
		Own instance of Git Lab
			where I maintain notes to self but visible to public

=cut

use strict;
use vars qw/ %ENV /;
use Mojolicious::Lite;

use Mojo::File qw(curfile);
my $dir = ''; $dir = curfile->dirname;
$dir =~ s!\/lib!!;
##use lib "".$dir."/lib";
# libraries: Windows does not allow variables
use lib ("lib", "./lib", "C:/inetpub/wwwroot/PCAccessFree/lib", "C:/inetpub/wwwroot/pc-access-free/lib", "C:/Users/sumu/public/github/PCAccessFree/lib");
##use lib qw(lib ./lib, $dir/lib);

=head2 Helpers
	Mojo Lite Helpers
	CGI helper packages
	Database helpers
=cut

=head2 Users
	10.6.5-MariaDB on my laptop.
		See lib/Database for creating/importing tables in SQL.
		Used for PCAF users, notes, and blog
=cut

use Users;
helper users => sub { state $users = Users->new(); };

=head2 Languages/Locales
	Default is us-en
	Also see POD for Languages
=head3 English/US
	lang/en-us.txt
	Basis for translation into all other languages.
=head3 Kannada
	Translation
		Doing it myself. Looking pretty good.
=head3 Tamil

=head2 Telugu

=head3 Hindi

=head3 South Korean

=head3 Spanish

=cut

=head2 use Languages
	Essential Class
=cut

use Languages;

=head2 helper lang
	Will not work, see #2 in git.byzland.com
	But Lang::method does work, used quite extensively throughout all templates
=cut

helper lang => sub { state $lang = Lang->new(); };

=head2 Use Syst
=cut

use Syst;
helper syst => sub { state $syst = Syst->new(); };

=head2 Package Utils
	Utilities used everywhere
=cut

use Utils;
helper utils => sub { state $utils = Utils->new(); };

=head2 Package Admin
	Everyting needed by a logged in user
=cut

use Admin;
helper admin => sub { state $admin = Admin->new(); };

=head2 sys Hash
	The hash %sys carries important name/value pairs like app dir, etc.
	Future plan: move to lib
=cut

my %sys;
%sys = (
	script_name => "PCAccessFree",
	password_dir_name => "PCAF072",
);

# error
$sys{error} = '';

# path
$sys{zero} = $0;
$sys{zero} =~ s!\\!/!g;
my @path;
@path = split(/\//, $sys{zero}, $#path);
$sys{script_dir} = join('/', @path[0..$#path-1]);

# suggested place to store user/pass files
if ( $sys{zero} =~ /^[A-Z]:\/Users/ )
{
	$sys{password_dir} = "$path[0]/$path[1]/$path[2]/$sys{password_dir_name}";
	$sys{csjs_url} = "//$ENV{SERVER_NAME}:$ENV{SERVER_PORT}/";
}
elsif ( $sys{zero} =~ /^[A-Z]:\/inetpub\/wwwroot/ )
{
	$sys{password_dir} = "$path[0]/$path[1]/$sys{password_dir_name}";
	$sys{csjs_url} = "$ENV{SCRIPT_NAME}:$ENV{SERVER_PORT}/$path[2]";
}
else
{
	$sys{password_dir} = "$sys{password_dir_name}";
	$sys{csjs_url} = "/";
}

=head2 plugin NotYAMLConfig
=cut

plugin 'NotYAMLConfig' => { file => "$sys{script_dir}/pcaccessfree.yml" };

my $config = plugin 'NotYAMLConfig' => { file => "$sys{script_dir}/pcaccessfree.yml" };


=head2 %fun Hash

=cut

my %fun;

if ( -e -f "$sys{script_dir}/lib/system_functions.txt" )
{
	open(my $SysFun, "$sys{script_dir}/lib/system_functions.txt") or $sys{error} = qq{<div class="alert alert-warning">$!</div>};
	my @sf = <$SysFun>;

	while ( my $function = <@sf> )
	{
		chomp $function;
		my ( $left, $right ) = split(/\=/, $function, 2);
		$fun{"$left"} = "$right";
	}
	close $SysFun;
}
else
{
	$sys{error} = qq{<div class="alert alert-warning">File system_functions does not exist. Creating one</div>};

	open( my $sysfun, ">$sys{script_dir}/lib/system_functions.txt" ) or $sys{error} .= qq{<div class="alert alert-danger">$!</div>};
	print $sysfun qq{cookie_domain=localhost\ncookie_expiry=+3M\ncss_js_url=//localhost/\nenable_browser_info=1\nenable_cookie_secure=1\nenable_date_folder=1\nenable_server_info=1\nlanguage=en-us\npassword_dir=C:/inetpub/PCAF22\nscript_web_dir=C:/inetpub/wwwroot/PCAccessFree\nserver_port=80\nuser_pref_home_dir=C:/inetpub/wwwroot/PCAccessFree\nweb_root=C:/inetpub/wwwroot\nweb_root_url=//localhost\n};
	close $sysfun;
}

=head2 Form for /nologin
=cut

my $form = '';
$form .= qq{<form action="/github/PCAccessFree/nologin.cgi/change" method="post">};
for (sort keys %fun )
{
	chomp;

	if ( $_ =~ /^enable/ )
	{
		$sys{title_tip} = qq{0=disable 1=enable};
		$sys{"suggest$_"} = qq{ (0=disable 1=enable) };
	}
	elsif ( $_ =~ /password_dir/ )
	{
		if ( $fun{$_} eq '' )
		{
			$fun{$_} = "$sys{password_dir}";
			$sys{title_tip} = "Suggested Path";
		}
		else
		{
			$sys{title_tip} = "Please change value";
			$sys{"suggest$_"} =  qq{ ($sys{password_dir})};
		}
	}
	elsif ( $_ =~ /css_js_url/ )
	{
		if ( $fun{$_} eq '' )
		{
			$fun{$_} = "$sys{csjs_url}";
			$sys{title_tip} = "Suggested Path";
		}
		else
		{
			$sys{title_tip} = "Please change value";
			$sys{"suggest$_"} = qq{ ($sys{csjs_url}) };
		}
	}
	elsif ( $_ =~ /cookie_domain/ )
	{
		if ( $fun{$_} eq '' )
		{
			$fun{$_} = "$ENV{SERVER_NAME}";
			$sys{title_tip} = "Suggested Path";
		}
		else
		{
			$sys{title_tip} = "Please change value";
			$sys{"suggest$_"} = qq{ ($ENV{SERVER_NAME}) };
		}
	}
	elsif ( $_ =~ /user_pref_home_dir/ )
	{
		if ( $fun{$_} eq '' )
		{
			$fun{$_} = "$sys{script_dir}";
			$sys{title_tip} = "Suggested Path";
		}
		else
		{
			$sys{title_tip} = "Please change value";
			$sys{"suggest$_"} = qq{ ($sys{script_dir}) };
		}
	}
	elsif ( $_ =~ /script_web_dir/ )
	{
		if ( $fun{$_} eq '' )
		{
			$fun{$_} = "$sys{script_dir}";
			$sys{title_tip} = "Suggested Path";
		}
		else
		{
			$sys{title_tip} = "Please change value";
			$sys{"suggest$_"} = qq{ ($sys{script_dir}) };
		}
	}
	elsif ( $_ =~ /server_port/ )
	{
		if ( $fun{$_} eq '' )
		{
			$fun{$_} = "$ENV{SERVER_PORT}";
			$sys{title_tip} = "Suggested Path";
		}
		else
		{
			$sys{title_tip} = "Please change value";
			$sys{"suggest$_"} = qq{ ($ENV{SERVER_PORT}) };
		}
	}
	elsif ( $_ =~ /web_root/ )
	{
		if ( $fun{$_} eq '' )
			{
				$fun{$_} = "$ENV{DOCUMENT_ROOT}";
				$sys{title_tip} = "From ENV ";
			}
			else
			{
				$sys{title_tip} = "Please change value";
				$sys{"suggest$_"} = qq{ ($ENV{DOCUMENT_ROOT}) };
			}
	}
	else
	{
		$sys{title_tip} = qq{Please change value };
	}

	$form .= qq{
		<div class="form-group">
			<label for="$_" title="">$_ $sys{"suggest$_"}</label>
			<input class="form-control" type="text" name="$_" id="$_" value="$fun{$_}" title="$sys{title_tip}">
		</div>
	};
}
$form .= qq{<button type="submit" class="badge badge-pill badge-secondary">Go</button>};
$form .= qq{</form>};
$form .= qq{
	$sys{error}
};
# end form
# end system stuff


=head2 get /nologin
	Show settings for user to change/update without logging in
	This is here for backwards compatibility ( was front page in versions prior to around 050?)
=cut

get '/nologin' => sub {
	my $c = shift;
	my %lang = Lang::get_language( dir => "$sys{script_dir}" );
	$c->render(
		'index',
		h1 => qq{ $sys{script_name} },
		csjs => "/$sys{csjs_url}",
		dir => "$sys{script_dir}",
		form => qq{$form}
	);
};
# end no login

=head2 post /nologin
	Save Settings posted from /nologin
=cut

post '/change' => sub {

	my $c = shift;

	my $result = '';
	my %result;

	my %in;

	for (keys %fun ) {

		# Assign name = value
		$result{$_} = $c->param("$_");
	}

	my $fdb = '';
	if ( -e -f "$sys{script_dir}/lib/system_functions.txt" )
	{
		open(FDB, ">$sys{script_dir}/lib/system_functions.txt") or die $!;
	}

	$result .= qq{<table>};
	for ( keys %result )
	{

		# Write to File Database
		print FDB qq{$_\=$result{$_}\n};

		# to browser
		$result .= qq{ <tr> <td>$_</td> <td>$result{$_}</td> </tr> };
	}
	$result .= qq{</table>};

	close FDB;

	$c->render(
		'change',
		h1 => qq{$sys{script_name}},
		csjs => "$sys{csjs_url}",
		result => qq{ $result },
	);
};
# end post change

get '/' => sub {
	my $c = shift;
	my $out = '';
	$c->render(
		'welcome',
		h1 => qq{ $sys{script_name} },
		csjs => "/$sys{csjs_url}",
		dir => "",
		out => qq{$out}
	);
};


# env
get '/env' => sub {
	my $c = shift;

	my $out = '';
	$out .= qq{};

	if (%ENV) {

		for (keys %ENV) {
			$out .= qq{<tr> <td>$_</td> <td>$ENV{"$_"}</td> </tr>\n};
		}
		$out .= qq{};

	}

	$c->stash(out => qq{$out});
	$c->render(
		'env',
		h1 => qq{$sys{script_name}},
		csjs => "$sys{csjs_url}",
		result => qq{},
	);
};
# end env

get '/search' => sub {
	my $c = shift;
	$c->render('search/welcome', h1 => "Search");
};
# end search


# Result

post '/search' => sub {
	my $c = shift;
	#
	my @out;
	# search term
	my $searchterm = $c->param('searchterm');
	$searchterm =~ s!(\$|\#|\@|\&|\*|\(|\)|\%|\^|\!)!!g; # add more later.
	my $searchresult = '';
	my $error = '';
	# result
	my $searchdir = $dir;
	$searchdir =~ s!\/github\/PCAccessFree!!;
	# hide some basic/imp info from hackers
	my $dir4web = $searchdir;
	$dir4web =~ s!C:/Users/sumu/public!!;
	#
	if ( -d "$searchdir" ) {
		if ( opendir(my $sd, $searchdir) ) {
			# find a match
			while (my $file = readdir $sd) {
				#
				#next if $file =~ /^.$/;
	      #next if $file =~ /^..$/;
				# find match
				if ($file =~ /$searchterm/i) {
					# Does not work for some reason i dono
					#$searchresult .= qq{ <a href="/found?name=$file" title="match found">$file</a> };
					# works
					push( @out, qq{<a href="$dir4web/$file&dir=$dir4web" title="found match $file">$file</a>} );
					# error
					$error = qq{<div class="alert alert-default">Results found for "$searchterm" in "$searchdir" </div>};
				} else {
					# will show up only if no content in searchresult. See logic in result.*.ep
					$error = qq{<div class="alert alert-warning">No results found for "$searchterm" in "$searchdir" </div>};
				}
			}
			closedir $sd;
			# end while
		} else {
			$searchresult = qq{<div class="alert alert-danger">Unable to open directory $searchdir </div>};
		}
	} else {
		$searchresult = qq{<div class="alert alert-danger">Search Directory is inaccessible or not found </div> };
	}

	for (@out) { $searchresult .= qq{$_ }; }

	# render
	$c->render(
		'search/result',
		searchterm => $searchterm,
		searchdir => "$searchdir",
		searchresult => qq{$searchresult},
		error => $error,
		h1 => "Results for search"
	);
	# end render
};
# end search result


=head2 Login
	Login
=cut

get '/login' => sub {
	my $c = shift;
	$c->render('login/index', h1 => "Login");
};
# end login form

post '/admin' => sub {
	my $self = shift;
	my $session = $self->session;

	my $session_user = $self->session('user');

	my $user = $self->param('user') || '';
	my $pass = $self->param('pass') || '';

	if ( $session_user )
	{
		$self->render('/admin/welcome', h1 => 'Welcome');
	}
	# end if session user
	else
	{
		#return $self->render unless $self->users->check($user, $pass);
		if ( $self->users->check($user, $pass) ) {
			# Add to session
			$self->session(user => $user);
			$self->flash(message => 'Thanks for logging in.');
			$self->render('admin/welcome', h1 => "Welcome back");
		} else {
			$self->render('login/index', h1 => "");
		}
		#########$self->redirect_to('/admin');
	}
	# end else session user
};
# end post login


get '/admin' => sub {
	my $self = shift;

	my $session_user = $self->session('user');

	if ( $session_user )
	{
		$self->render('/admin/welcome', h1 => "Welcome back $session_user");
	}
	# end if session user
	else
	{
		$self->render('/login/index', h1 => "Login");
	}
};
# end get /admin



=head2 Admin/settings
	system_functions.txt
	Database settings: settings.txt
=cut

# admin/settings
get '/admin/settings' => sub {
	my $self = shift;
	my $session_user = $self->session('user');
	#
	my $out = '';
	#
	my %set = ();
	#
	$set{system_functions} = $self->syst->settings( file => "$dir/lib/system_functions.txt");
	#
	$set{db_settings} = $self->syst->settings( file => "$dir/lib/Database/settings.txt");
	#

	#
	if ($session_user) {
		$self->render(
			'/admin/settings',
			h1 => "PC Access Free - App Settings",
			user => "$session_user",
			system_settings => $set{system_functions},
			db_settings => $set{db_settings},
			out => $out
		);
	} else {
		$self->render('/admin/settings',
			h1 => "Session Expired", user => '', system_settings => '', db_settings => '', out => ""
		);
	}
};
# end


post '/admin/savesettings' => sub {
	my $self = shift;
	my $out = '';	#
	my $tofile = '';
	my @names = $self->syst->settings_names_array( file => "$dir/lib/system_functions.txt");
	$out .= qq{<table class="table">};
	for (sort @names) {
		$tofile .= qq{$_=} . $self->param("$_"). qq{\n};
		$out .= qq{<tr> <td>$_</td> <td>} . $self->param("$_") . q{</td> </tr>};
	}
	$out .= qq{</table> <textarea class="form-control">$tofile</textarea>};
	# write to file
	if ( open( my $sysfile, ">", "$dir/lib/system_functions.txt") ) {
		print $sysfile "$tofile";
	}
	#close $sysfile;
	#
	$self->render('admin/savesettings', h1 => "", out => $out);
};
# end post settings

# admin/settings
get '/admin/lang/show/:lang' => sub {
	my $self = shift;
	my $lang = $self->param('lang');
	my $session_user = $self->session('user');
	my $out = $self->lang->english( file => "$dir/lang/$lang.txt");
	if ($session_user) {
		$self->render(
			'/admin/settings',
			h1 => "PC Access Free - Lang Settings",
			out => $out
		);
	} else {
		$self->render('/login')
	}
};

# admin/settings
post '/admin/lang/save/:lang' => sub {
	my $self = shift;
	my $lang = $self->param('lang');
	my $session_user = $self->session('user');
	my $out = $self->lang->english( file => "$dir/lib/system_functions.txt");
	if ($session_user) {
		$self->render(
			'/admin/settings',
			h1 => "PC Access Free - App Settings",
			out => $out
		);
	} else {
		$self->render('/login')
	}
};


=head2 Logout
=cut

get '/logout' => sub {
	my $c = shift;
	$c->session(expires => 1);
	$c->render('login/logout', h1 => "Logout successful");
};
# end logout


=head2 Profile

=cut

get '/admin/profile/:user' => sub {
	my $c = shift;
	my $user = $c->param('user');
	chomp $user;
	$user = $c->utils->cleanse( string => "$user" );
	my $out = '';
	#$out .= qq{$user};
	#
	my $verify = '';
	if ( $user =~ /[a-zA-Z0-9]/ ) {
			# run sql and get return value from .pm
			$verify = $c->admin->profile(
				user => "$user",
				url4save => $c->url_for('/admin/profile/save')->to_abs(),
				url4update => $c->url_for('/admin/profile/update')->to_abs(),
				url4view => $c->url_for("/profile/$user")->to_abs()
			);
	}
	$out .= qq{$verify};
	# render
	$c->render('admin/profile/welcome', h1 => "Profile", user => "$user", out => $out);
};


=head2 Save Profile
=cut

post '/admin/profile/save' => sub {
	my $c = shift;

	my $user = $c->session('user');

	my %in = (
		url4save => $c->url_for('/admin/profile/save')->to_abs(),
		url4update => $c->url_for('/admin/profile/update')->to_abs(),
		url4view => $c->url_for("/profile/$user")->to_abs(),
		@_,
	);

	#
	my %out = ();

	#
	for ( qw/id username created firstname lastname email description/ ) {
    $out{"$_"} = $c->param("$_");
  }
	# take care of new lines in textarea content
	$out{description} =~ s!\n! NEWLINE !g;
	# sql
	#sql
	#( $in{firstname}, $in{lastname}, $in{email}, $in{description} ) = (  );
	my $save_profile_sql = qq{INSERT INTO `profile` (`id`, `username`, `created`, `firstname`, `lastname`, `email`, `description`)
	values (DEFAULT, "$out{username}", DEFAULT, "$out{firstname}", "$out{lastname}", "$out{email}", "$out{description}") };
	my $out = '';
	for (keys %out ) {
		$out .= qq{$_=$out{$_} <br/>}
	}
	# enable to test only
	#$out .= qq{<hr/> $save_profile_sql};
	#
	#insert into table
	my $commit_sql = $c->admin->profile_save( sql => $save_profile_sql );
	#
	if ( $commit_sql >= '1' ) {
		$out .= qq{
			<div class="alert alert-success">Saved successfully</div>
			<div class="container">
				View <a href="$out{url4view}" title="view profile">profile</a>
			</div>
		};
	} else {
		$out .= qq{ <div class="alert alert-danger">Profile creation failed</div> };
	}
	# render
	$c->render('admin/profile/save', h1 => "save profile", user => $out{username}, out => $out);
};
# end save profile



=head2 Update Profile
	Update profile - data comes from /admin/profile/:user - url4update
=cut

post '/admin/profile/update' => sub {
	my $c = shift;

	my $user = $c->session('user');

	my %out = (
		url4save => $c->url_for('/admin/profile/save')->to_abs(),
		url4update => $c->url_for('/admin/profile/update')->to_abs(),
		url4view => $c->url_for("/profile/$user")->to_abs()
	);

	#
	$out{username} = $c->session('user');
	chomp $out{username};

	#
	for ( qw/firstname lastname email description/ ) {
    $out{"$_"} = $c->param("$_");
  }

	# take care of new lines in textarea content
	$out{description} =~ s!\n! NEWLINE !g;

	#sql
	#( $in{firstname}, $in{lastname}, $in{email}, $in{description} ) = (  );
	my $update_profile_sql = qq{UPDATE `profile` SET `firstname`="$out{firstname}", `lastname`="$out{lastname}", `email`="$out{email}", `description`="$out{description}" WHERE `username`="$out{username}" LIMIT 1};
	my $out = '';

	# enable during test/dev only
	#for (keys %out ) { $out .= qq{$_=$out{$_} <br/>} }

	# enable during test only
	#$out .= qq{<hr/> $update_profile_sql};

	# insert into table
	my $commit_sql = $c->admin->profile_update( sql => $update_profile_sql );

	#
	if ( $commit_sql >= '1' ) {
		$out .= qq{
			<div class="alert alert-success">Updated successfully</div>
			<div class="container">
				View <a href="$out{url4view}" title="view profile">profile</a>
			</div>
		};
	} else {
		$out .= qq{ <div class="alert alert-danger">Profile updating failed</div> };
	}

	# render
	$c->render('admin/profile/save', h1 => "save profile", user => $out{username}, out => $out);
};
# end update profile


=head2 Profile View
=cut

get '/profile/:user' => sub {
	my $c = shift;

	my %in = (
		user => $c->param('user')
	);

	my $out = '';
	my @data = $c->admin->profile_view( user => $in{user} );
	#
	#for (@data) { $out .= qq{$_ }; }

	# build the html output
	# Dont show username <tr> <td> Username </td> <td> $data[1] </td> </tr>
	$out .= qq{
		<table class="table table-responsive">

			<tr> <td> First name </td> <td> $data[3] </td> </tr>
			<tr> <td> Last Name </td> <td> $data[4] </td> </tr>
			<tr> <td> Email </td> <td> $data[5] </td> </tr>
			<tr> <td> Description </td> <td> $data[6] </td> </tr>
		</table>
	};

	#
	$c->render('profile_view', h1 => "View profile", user => $in{user}, out => qq{ $out } );
};
# end profile view



=head2 Versions
	Version identifiers for installed software/package on your system
=cut

get '/versions' => sub {
	my $c = shift;
	$c->render('versions', h1 => "Versions ");
};
# enc versions


=head2 Profile

=cut

get '/profile' => sub {
	my $c = shift;
	my $user = $c->param('user');
	$c->render('profile', user => $user );
};
# end profile


=head2 Save DB Settings
	Save settings to lib/Database/settings.txt 
=cut

post '/admin/save_db_settings' => sub {
	my $self = shift;
	my $out = '';
	# Var to hold content to be written to settings.txt
	my $tofile = '';
	# get names only from settings.txt file with name=value pairs
	my @names = $self->syst->settings_names_array( file => "$dir/lib/Database/settings.txt");
	# begin output to browser/user - table
	$out .= qq{<table class="table"> <tr> <td colspan="2">The following values were saved to settings.txt</td> </tr> };
	for (sort @names) {
		# build content to be saved to file
		$tofile .= qq{$_=} . $self->param("$_"). qq{\n};
		# output - table tr
		$out .= qq{<tr> <td>$_</td> <td>} . $self->param("$_") . q{</td> </tr>};
	}
	# end output - table
	$out .= qq{</table>};
	# test
	#$out .= qq{<textarea class="form-control">$tofile</textarea>};

	# write to file
	if ( open( my $sysfile, ">", "$dir/lib/Database/settings.txt") ) {
		print $sysfile "$tofile";
	}
	# render
	$self->render('admin/save_db_settings', h1 => "", out => $out);
};
# end post save db settings







app->start();



1;




__DATA__
