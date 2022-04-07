#!perl

=head1 Test admin.cgi
  Please refer to https://metacpan.org/pod/Test::Mojo for details
=cut

use lib '..', '../', '../lib';

use Test::More tests => 4;

=head3 Get Cwd
  Get Current Working Directory
=cut

use Cwd qw();
my $cwd = Cwd::abs_path();
$cwd =~ s!\\!\/!g;
$cwd =~ s!\\t\\!!g;

=head3 Test cwd
=cut

ok( $cwd =~ /users/i  => "$cwd" );

=head3 Test for existence of admin.cgi
=cut

ok( -f "$cwd/admin.cgi");

=head3 Test Welcome page
  Test:
    perl admin.cgi get /
=cut

ok( `perl "$cwd/admin.cgi" get /` =~ /welcome/i );

=head3 Test Login page
  perl admin.cgi get /login
=cut

ok( `perl "$cwd/admin.cgi" get /login` =~ /username/i );
