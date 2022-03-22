#!/usr/bin/env perl

use Mojolicious::Lite -signatures;

use Mojo::File qw(curfile);
my $dir = ''; $dir = curfile->dirname;
$dir =~ s!\/lib!!;
#use lib "".$dir."/lib";

use lib 'C:/Users/sumu/public/github/PCAccessFree/lib';

use Users;

# Make signed cookies tamper resistant
app->secrets(['Mojolicious rocks']);

helper users => sub { state $users = Users->new };

# Main login action
any '/' => sub ($c) {

  # Query or POST parameters
  my $user = $c->param('user') || '';
  my $pass = $c->param('pass') || '';

  # Check password and render "index.html.ep" if necessary
  return $c->render unless $c->users->check($user, $pass);

  # Store username in session
  $c->session(user => $user);

  # Store a friendly message for the next page in flash
  $c->flash(message => 'Thanks for logging in.');

  # Redirect to protected page with a 302 response
  $c->redirect_to('admin/welcome');

} => 'login/index';

# Make sure user is logged in for actions in this group
group {
  under '/admin' => sub ($c) {

    # Redirect to main page with a 302 response if user is not logged in
    return 1 if $c->session('user');
    $c->redirect_to('admin/welcome');
    return undef;
  };

  # A protected page auto rendering "protected.html.ep"
  get '/protect' => sub ($c) {
    $c->render('admin/protect');
  };

  get '/welcome' => sub ($c) {
    $c->render('admin/welcome');
  };

};

post '/admin' => sub ($c) {
  $c->render('admin/welcome');
};# end post /admin

get '/admin' => sub ($c) {
  $c->render('admin/welcome');
};# end post /admin

get '/admin/welcome' => sub ($c) {
  $c->render('admin/welcome');
};# end post /admin

get '/admin/protected' => sub ($c) {
  $c->render('admin/protected');
};# end post /admin


# Logout action
get '/logout' => sub ($c) {

  # Expire and in turn clear session automatically
  $c->session(expires => 1);

  # Redirect to main page with a 302 response
  $c->redirect_to('login/index');
};

app->start;

1;


__DATA__

@@ dash.html.ep


@@ protected.html.ep
