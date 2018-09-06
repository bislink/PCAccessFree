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
);

# error 
$sys{error} = '';

# path 
$sys{zero} = $0; 
$sys{zero} =~ s!\\!/!g; 
my @path;
@path = split(/\//, $sys{zero}, $#path);
$sys{script_dir} = join('/', @path[0..$#path-1]);
$sys{csjs} = "$path[4]";

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
	
	if ( $_ =~ /^enable/ ) { $sys{title_tip} = qq{0=disable 1=enable}; } else { $sys{title_tip} = qq{Please change value }; }
	
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
		h1 => qq{ $sys{script_name} $ENV{SCRIPT_NAME}}, 
		csjs => "/$sys{csjs}",
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
		csjs => "$sys{csjs}",
		result => qq{ $result },
	);
};




1;

app->start();


__DATA__
