#!C:\\Strawberry\\perl\\bin\\perl5.26.1.exe

=head1 admin
admin.cgi
=cut

use strict;
use vars qw/ %ENV /;
use Mojolicious::Lite;

use Mojo::File qw(curfile);
my $dir = ''; $dir = curfile->dirname;
$dir =~ s!\/lib!!;
#use lib "".$dir."/lib";

use lib 'C:/Users/sumu/public/github/PCAccessFree/lib';

use Users;
helper users => sub { state $users = Users->new(); };

use Languages;
helper lang => sub { state $lang = Lang->new(); };

use Syst;
helper syst => sub { state $syst = Syst->new(); };

# system
my %sys;
%sys = (
	script_name => "PCAccessFree",
	password_dir_name => "PCAF_UP_041",
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
#functions
my %fun;

if ( -e -f "$sys{script_dir}/lib/system_functions.txt" )
{
	open(SysFun, "$sys{script_dir}/lib/system_functions.txt") or die $!;
	my @sf = <SysFun>;
	close SysFun;

	while ( my $function = <@sf> )
	{
		chomp $function;
		my ( $left, $right ) = split(/\=/, $function, 2);
		$fun{"$left"} = "$right";
	}
}
else
{
	$sys{error} = qq{Unable to open system_functions. 	$sys{zero} $sys{script_dir} };
}

# Form
my $form = '';
$form .= qq{<form action="$ENV{SCRIPT_NAME}/change" method="post">};
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

get '/nologin' => sub {
my $c = shift;
	$c->render(
		'index',
		h1 => qq{ $sys{script_name} },
		csjs => "/$sys{csjs_url}",
		dir => "",
		form => qq{$form}
	);
};

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
					$searchresult .= qq{ <a href="/found?name=$file" title="match found">$file</a> };
					# works
					push( @out, qq{<a href="/found?name=$file&dir=$dir4web" title="match found">$file</a>} );
				} else {
					$searchresult = qq{<div class="alert alert-warning">No results found for "$searchterm" in "$searchdir" </div>};
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
		searchresult => qq{$searchresult}
	);
	# end render
};
# end search result

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

# admin/settings
get '/admin/settings' => sub {
	my $self = shift;
	my $session_user = $self->session('user');
	my $out = $self->syst->settings( file => "$dir/lib/system_functions.txt");
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

get '/logout' => sub {
	my $c = shift;
	$c->session(expires => 1);
	$c->render('login/logout', h1 => "Logout successful");
};
# end logout

app->start();



1;




__DATA__
