package Database::Config;
# helper
sub new { bless {}, shift }


sub directories {
	my ($self, $dir) = @_;
	my %dir;
	if (opendir(DIR, "$dir") ) {
		my @dir = readdir(DIR);
		close DIR;

		for (@dir) {
			# Just list all directores/files in any/the given DIR
			$dir{items_in_DIR} .= qq`$_` if ($_ =~ /[a-zA-Z0-9.-]/);
		}
	}

=head1 Old
	# Add dir .git to the list.  Change if needed
	$dir{git_dir} = '/home/biblelegacy/biblelegacy/.git';
	# Mojo App dir root.
	$dir{APPDIR} = '/home/biblelegacy/biblelegacy',
	# Secrets
	$dir{secret} = "$ENV{DOCUMENT_ROOT}/SECRETS";
=cut

	# DH
	$dir{git_dir} = "/home/biblelegacy/bl";
	$dir{APPDIR} = "/home/biblelegacy/bl";
	$dir{secret} = "/home/biblelegacy/SECRETS";

	return %dir;
}



sub db
{
	my ($self) = @_;

	my %db;

=head1 DB Settings
Old settings removed.
New settings for Dreamhost
=cut

	# host DH
	$db{'host'} = 'localhost';

  $db{'port'} = '3308';

	# Main database
	$db{'db'} = 'mojocms';		#

	# user
	$db{'user'} = 'mojocms';

	#password
	$db{'pass'} = 'Mojo4Cms,22032';

	# users table
	$db{moj_users_table} = 'users';

	return %db;
}


sub dbh
{
	my ($self, $raiseError, $autoCommit) = @_;

	my %db = db();

	my $dbh = DBI->connect(
		"DBI:mysql:host=$db{'host'};database=$db{'db'}", "$db{'user'}", "$db{'pass'}",
		{'RaiseError' => $raiseError, AutoCommit => $autoCommit, mysql_auto_reconnect => 1 }
	);		#

	return  $dbh;

}

sub table_names {

	my ($self) = @_;

	my %table_names = (
		users 		=> 	'moj-users',
		profile		=>	'moj-profile',
		log_browsers	=>	'moj-log-browsers',
		log_ip		=>	'moj-log-ip',
		log_url		=>	'moj-log-url',
		log_visits	=>	'moj-log-visits',
		chat => 'bl_chat',
		user_pref => 'bl_user_preferences',
	);

	return %table_names;
}

sub userprofile {
	my ($self, $user) = @_;

	return "UserProfile";
}


sub git_latest_commitId {
	# also `git rev-parse HEAD` can be used to get latest id
	my ($self, $dir) = @_;
	my $id = `cat "$dir/refs/heads/master"`;
	chomp $id;
	return $id;
}

=head2 SQL for users
	See Database/tables.sql
=cut

1;
