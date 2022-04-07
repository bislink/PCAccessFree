package Utils;
use Mojo::Base 'Mojolicious::Controller';

=head2 Package Utils

=cut

=head3 Get Cwd
  Get Current Working Directory
  Used in get_cwd down below
    which in turn is used in admin.cgi via 'use Utils'
=cut

use Cwd qw();
my $cwd = Cwd::abs_path();
$cwd =~ s!\\!\/!g;


=head3 Cleanse A String
  remove metacharacters from a given string and return the cleansed string 
=cut

sub cleanse {
  my $c = shift;
  my %in = (
    string => "",
    @_,
  );
  if ($in{string} ne '') {
    $in{string} =~ s!(\~|\!\@|\$|\%|\^|\&|\*|\(|\)|\:|\<|\>|\,|\.|\`|\/)!!g;
  } else {
    $in{string} = "NOSTRING";
  }
  return $in{string};
}
# end cleanse

=head3 Return Current Working Directory
	This sub just returns current working directory
=cut

sub get_cwd {
  return $cwd;
}
# end get cwd








1;
