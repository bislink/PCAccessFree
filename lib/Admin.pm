package Admin;
use Mojo::Base 'Mojolicious::Controller';


sub welcome {
  my $c = shift;
  $c->render('admin/welcome', out => "OUT" ); # $c->appconfig->{thisapp}->{name}
}





1;
