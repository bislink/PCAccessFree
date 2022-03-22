#!C:/Strawberry/perl/bin/perl.exe
#C:/Users/sumu/public/github/PCAccessFree/lib/Dates.pm

=head1 CGI Helper

=cut

=head2 Dates
  Date stuff
=cut

package Dates;
use strict;
use DateTime;

sub general {
  my $date = DateTime->now();
  $date->set_time_zone('UTC');

  my @out;

  my %in = (
    type => 'name',
    name => 'epoch1',
    @_,
  );

  my %out = (
    epoch1 => $date->epoch,
  );

  if ( $in{type} eq 'array' ) { return @out; }
  elsif ( $in{type} eq 'hash') { return %out; }
  elsif ( $in{type} eq 'name' ) { return $out{"$in{name}"}; }
  else { return $date->now(); }

}
# end package Dates


=head2 Server
  Server/Host info
=cut

package Server;

sub server_info
{
	my %in;

	my $out = '';

	%in = (
		info => '',
		@_,
	);

	$out .= qq{<table class="table $in{tableclasses} browser-info">};

	for (keys %ENV ) {
		$ENV{$_} =~ s!\'! !g;
		$out .= qq{<tr> <td>$_</td> <td>$ENV{"$_"}</td> </tr>} if ( $_ and $ENV{$_} and $_ =~ /server/i );
	}

	$out .= qq{<tr> <td>Proc</td> <td> $ENV{'PROCESSOR_ARCHITECTURE'}</td> </tr> };

	$out .= qq{</table>};

	if( $in{enable_server_info} )
	{
		return qq{$out};
	}
	else
	{
		return qq{$in{server_info_disabled} <a href="$in{PCAccessAdminUrl}" title="$in{script_name}">$in{script_name} Admin</a> };
	}

}
# end server_info


# end package Server



1;
