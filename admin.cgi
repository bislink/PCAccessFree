#!C:\\Strawberry\\perl\\bin\\perl5.26.1.exe

=head1 admin
admin.cgi
=cut

use strict;
use vars qw/ %ENV /;
use Mojolicious::Lite;

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
		}
	}
	else 
	{ 
		$sys{title_tip} = qq{Please change value }; 
	}
	
	$form .= qq{
		<div class="form-group">
			<label for="$_" title="">$_</label> 
			<input class="form-control" type="text" name="$_" id="$_" value="$fun{$_}" title="$sys{title_tip}">
		</div>
	}; 
}
$form .= qq{<button type="submit" class="badge badge-pill badge-secondary">Go</button>};
$form .= qq{</form>};
$form .= qq{
	$sys{error}
};

get '/' => sub {
my $c = shift;
	$c->render(
		'index', 
		h1 => qq{ $sys{script_name} $ENV{SCRIPT_NAME} }, 
		csjs => "/$sys{csjs_url}",
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




1;

app->start();


__DATA__
