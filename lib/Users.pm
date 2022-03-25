package Users;

use strict;
#use warnings;

use lib '../lib', 'lib';

use Mojo::Util 'secure_compare';

##use experimental 'signatures';

use DBI;

use vars qw(%db);

=head1 Location
	moved to ~/ from public_html 2020-05-17-2120
=head1 Database User/Pass
	Change user/pass/db in Config.pm
=cut

use Database::Config;
%db = Database::Config->db();


#connect
my $dbh = DBI->connect("DBI:mysql:host=$db{'host'};port=$db{port};database=$db{'db'}", "$db{'user'}", "$db{'pass'}",
  {'RaiseError' => 1, PrintError => 1, AutoCommit => 1, mysql_auto_reconnect => 1}
) or $db{'error_users_db'} = "Users#18 $DBI::err ($DBI::errstr)";


sub new { bless {}, shift }

sub check {
  my ($self, $user, $pass) = @_;

  #DB

  # get user/pass from mysql
  my $check_user = $dbh->prepare( qq{SELECT `id`, `username`, `password` from `$db{moj_users_table}` WHERE `username` = "$user" } );
  $check_user->execute();
  my @get_up = $check_user->fetchrow_array();

  # get MD5 encrypted version of the $pass
  my $encrypted = $dbh->prepare( qq{SELECT MD5("$pass") } );
  $encrypted->execute();
  my $encrypted_pass = $encrypted->fetchrow();

  # Success
  #return 1 if $USERS->{$user} && secure_compare $USERS->{$user}, $pass;
  return 1 if $get_up[1] && secure_compare $get_up[2], $encrypted_pass;

  # Fail
  return undef;
}

# disconnect
#$dbh->disconnect;	# OK on cmdline after commenting # THE SOLUTION for "MySQL server has gone away" # 2016-04-11 08:49:08


1;
