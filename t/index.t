#!perl

=head1 Test of index.cgi
  uses Test::More
  usage
    open powershell as Administrator or current logged in user
    cd
      C:/Inetpub/wwwroot/PCAccessFree
      or
      C:/Users/USER/IISpublicFolder/PCAccessFree
    prove -l t/index.t
=cut

use strict;
use Cwd qw();
my $cwd = Cwd::abs_path();
$cwd =~ s!\\!\/!g;

=head2 Get current working dir
  Should either be '/inetpub/wwwroot' or ':/users/'
=cut

my $dir = '';
if ( $cwd =~ /inetpub/i ) { $dir = "C:/inetpub/wwwroot/PCAccessFree"; }
elsif ( $cwd =~ /users/i) { $dir = "C:/Users/sumu/public/github/PCAccessFree"; }
else { $dir = '.'; }

=head3 USE lib
  Enable this if you get error similar to
    'Empty compile time value given to use lib at .\t\index.t line 40'
=cut

use lib "..", "../", "../lib"; #, "".$dir."", "".$dir."/lib";
#use lib 'C:/inetpub/wwwroot/PCAccessFree', 'C:/Users/sumu/public/github/PCAccessFree';

=head3 Import other/more libraries
  CGI
=cut

use CGI;
require 'index.cgi';

=head2 Set number of tests to run
  Import Test::More
=cut

use Test::More tests => 9;

=head3 Most basic test
  check if perl -v returns ok, version is 5, and OS matches mswin
=cut

my @perlv = `perl -v`;
# 1
#  perl[0] is empty line
ok ( $perlv[1] =~ /this is perl 5/i and $perlv[1] =~ /mswin/i );


=head3 Simple math test
  1 + 1 == 2
  Should always pass!
=cut

# 2
ok( 1 + 1 == 2);


=head3 Test existence of files/folders
  Test if all required files and folders exist/accessible
    PCAccessFree
      index.cgi
      lib/system_functions.txt
      lib/Helper.pm
=cut

# 3
ok( -f 'index.cgi' );
# 4
ok( -f "$dir/lib/system_functions.txt");
# 5
ok( -d $dir );
# 6
ok( -f "$dir/lib/Helper.pm");


=head3 Tests on index.cgi
  index.cgi should show form with phrases login, pcaccessfree
=cut

# 7
ok( `perl index.cgi` =~ /login/i );
# 8
#  do not add -w flag
ok( `perl index.cgi` =~ /pcaccessfree/i );

=head3 Test Helper.pm
  Test if Helper is loaded;
=cut

use Helper;
my $date = Dates->general();
# 8
ok( $date );
