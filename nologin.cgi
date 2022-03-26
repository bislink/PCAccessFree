#!C:\\Strawberry\\perl\\bin\\perl5.26.1.exe

=head1 PCAccessFree
	nologin.cgi
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

=head2 use Languages
	Essential Class
=cut

use Languages;

=head2 Use Syst
=cut

use Syst;
helper syst => sub { state $syst = Syst->new(); };

=head2 sys Hash
	The hash %sys carries important name/value pairs like app dir, etc.
	Future plan: move to lib
=cut

my %sys;
%sys = (
	script_name => "PCAccessFree",
	password_dir_name => "PCAF22",
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
$form .= qq{};
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
$form .= qq{};
$form .= qq{};
$form .= qq{ $sys{error} };
# end form
# end system stuff

=head2 get /
	Show settings for user to change/update without logging in
	This is here for ease/simplicity and backwards compatibility
=cut

get '/' => sub {
	my $c = shift;
	my %lang = Lang::get_language( dir => "$sys{script_dir}" );
	$c->render(
		'nologin',
		h1 => qq{ $sys{script_name} },
		csjs => "/$sys{csjs_url}",
		dir => "$sys{script_dir}",
		form => qq{$form}
	);
};
# end / (nologin)




=head2 post to /change
	Save settings posted from / to system_functions.txt file
  Create default username.t file with default user/pass in the password_dir provided by user
=cut

post '/change' => sub {

	my $c = shift;

	my $result = '';
	my %result = (
    error => ''
  );

	my %in = (
    powershell => $c->config->{powershell},
  );

	for (sort keys %fun ) {

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

=head2 Create u.t file with default user/pass

=cut

if (-e -f "$result{password_dir}/pcaccessfree.t") {
  # do nothing
  $result{error_pw} = qq{<div class="alert alert-warning">File 'pcaccessfree.t' already exists 303</div> };
} else {

  # create dir first
  if (-d "$result{password_dir}" ) {
    #
  } else {
    `"$in{powershell}" New-Item -Path "$result{password_dir}" -ItemType "directory" -Force`;
  }
  open( my $UP, ">$result{password_dir}/pcaccessfree.t" ) or $result{error} = qq{<div class="alert alert-danger">299</div>};
  print $UP "pcaccessfree\|pcsfr2203\|C:/inetpub/wwwroot/PCAccessFree";
  close $UP;

  # verify if dir/file was really created
  if (-d "$result{password_dir}" and -e "$result{password_dir}/pcaccessfree.t") {
    # do nothing
    $result{error_pw} = qq{<div class="alert alert-success">File 'pcaccessfree.t' created. 320</div> };
  } else {
    $result{error_pw} = qq{<div class="alert alert-warning">Error creating file 'pcaccessfree.t' 322</div> };
  }

}
# end create default user pass file



=head2 Set default language

=cut

if ( -e -f "$sys{script_dir}/lang/default-language.txt" ) {
  open( my $DL, ">$sys{script_dir}/lang/default-language.txt" ) or $result{error} = qq{<div class="alert alert-danger"> Unable to open default lang file. 299</div>};
  print $DL "$result{language}";
  close $DL;

  $result{error_lang} = qq{<div class="alert alert-success">Default language set</div> };

} else {
  $result{error_lang} = qq{<div class="alert alert-warning">Unknown error setting default language 320 </div> };
}

	$c->render(
		'change',
		h1 => qq{$sys{script_name}},
		csjs => "$sys{csjs_url}",
		result => qq{ $result },
    pass_dir => qq{ $result{password_dir} $result{error_pw} },
    defa_lang => qq{ $result{language} $result{error_lang} }
	);
};
# end post change

app->start;

1;
