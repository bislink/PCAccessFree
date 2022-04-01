package Utils;
use Mojo::Base 'Mojolicious::Controller';

=head2 Package Utils

=cut

=head2 subroutine cleanse
  remove metachars from a string
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

1;
