package Login;
use Mojo::Base 'Mojolicious::Controller';

my %out;

sub index
{
	my $self = shift;

	my $session = $self->session;

	my $session_user = $self->session('user');

	my $user = $self->param('user') || '';
	my $pass = $self->param('pass') || '';

	if ( $session_user )
	{
		$self->redirect_to('/admin');
	}
	# end if session user
	else
	{
		return $self->render unless $self->users->check($user, $pass);

		# Add to session
		$self->session(user => $user);
		$self->flash(message => 'Thanks for logging in.');
		$self->redirect_to('/admin');
	}
	# end else session user
}
# end


sub logged_in
{
	my $self = shift;

	#my $user = ""; $user = $self->session('user'); chomp $user;

	return 1 if $self->session('user');
	$self->redirect_to('/admin');
	#return undef;

}

sub logout
{
	my $self = shift;

	my $user = $self->session('user');
	chomp $user;

	$self->session(expires => 1);

	$self->redirect_to('/login');
}




1;
