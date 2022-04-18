package Admin;
use Mojo::Base 'Mojolicious::Controller';

use utf8;
use open ':encoding(utf-8)';

use DBI;

use Database::Config;
my %db = Database::Config->db();

#connect
my $dbh = DBI->connect("DBI:mysql:host=$db{'host'};port=$db{port};database=$db{'db'}", "$db{'user'}", "$db{'pass'}",
  {'RaiseError' => 1, PrintError => 1, AutoCommit => 1, mysql_auto_reconnect => 1}
) or $db{'error_users_db'} = "Users#18 $DBI::err ($DBI::errstr)";


sub welcome {
  my $c = shift;
  $c->render('admin/welcome', out => "OUT" ); # $c->appconfig->{thisapp}->{name}
}

sub profile {

  my $c = shift;

=head2 %in
  url4* vars  are not set here in this sub but set in .cgi: see admin.cgi 642
=cut

  my %in = (
    user => '',
    sql_table_users => 'users',
    sql_table_profile => 'profile',
    sql_match => qq{},
    url4save => '',
    url4update => '',
    url4view => '',
    @_,
  );

  # get/verify logged in user
  my $check_user = $dbh->prepare( qq{ SELECT `username` from `$in{sql_table_users}` WHERE `username` = "$in{user}" } );
  $check_user->execute();
  my $get_u = $check_user->fetchrow();

  #
  if ( $in{user} eq $get_u ) {
    $in{sql_match} = qq{<button type="button" class="btn btn-primary disabled">$get_u</button>};
    # profile
    # check if profile exists
    my $check_profile = $dbh->prepare( qq{ SELECT count(`id`) from `$in{sql_table_profile}` WHERE `username` = "$in{user}" limit 0, 1} );
    $check_profile->execute();
    my $get_profile = $check_profile->fetchrow();

    # show forms for editing or creating profile
    # form for editing
    if ( $get_profile >= '1' ) {
      $in{sql_match} .= qq{
        <div class="alert alert-success">Profile exists. Edit/Update your profile </div>

        <button type="button" class="btn btn-primary position-relative disabled">
          Update Profile
          <span class="position-absolute top-0 start-100 translate-middle badge rounded-pill bg-success">$get_profile<span class="visually-hidden">unread messages</span></span>
        </button>
      };
      # get profile data from table profile (for updating )
      my $check_profile_data = $dbh->prepare( qq{ SELECT `id`, `username`, `created`, `firstname`, `lastname`, `email`, `description` from `$in{sql_table_profile}` WHERE `username` = "$in{user}" LIMIT 1} );
      $check_profile_data->execute();
      my $get_profile_data = $check_profile_data->fetchrow_hashref();
      # profile exists, show form to edit
      #for (@get_profile_data) { $in{sql_match} .= qq{$_ <br/>}; }
      # build form for editing
      $in{sql_match} .= qq{<div class="container"> <form action="$in{url4update}" method="post"> };
      for (qw/firstname lastname email/) {
        $in{sql_match} .= qq{<div class="mb-3">
          <label class="form-label" for="$_">$_</label>
          <input class="form-control" type="text" name="$_" id="$_" value="$get_profile_data->{$_}">
        </div>
        };
      }
      # textarea
      $get_profile_data->{description} =~ s! NEWLINE !\n!g;
      $in{sql_match} .= qq{
        <div class="mb-3">
          <label class="form-label" for="description">Description</label>
          <textarea class="form-control" name="description" id="description">$get_profile_data->{description}</textarea>
        </div>
      };
      # end textarea
      # end form
      $in{sql_match} .= qq{<button type="submit" class="btn btn-primary">Update</button>
        </form>
        </div>
      };
      # end build form
      # form for creating
    } elsif ( $get_profile <= '0' ) {
      $in{sql_match} .= qq{ <div class="alert alert-warning">Profile does not exist. Create one. </div> $get_profile };
      # profile does not exist, show form to create a new one
      $in{sql_match} .= qq{<form action="$in{url4save}" method="post">
        <input type="hidden" name="created" id="created" value="">
        <input type="hidden" name="username" value="$in{user}">
        <div class="mb-3">
          <label class="form-label" for="firstname">First Name</label>
          <input class="form-control" type="text" name="firstname" id="firstname" value="">
        </div>
        <div class="mb-3">
          <label class="form-label" for="lastname">Last Name</label>
          <input class="form-control" type="text" name="lastname" id="lastname" value="">
        </div>
        <div class="mb-3">
          <label class="form-label" for="email">Email</label>
          <input class="form-control" type="email" name="email" id="email" value="">
        </div>
        <div class="mb-3">
          <label class="form-label" for="description">Description</label>
          <textarea class="form-control" name="description" id="description"></textarea>
        </div>
        <button type="submit" class="btn btn-primary">Create</button>
      </form>
      };
    } else {
      $in{sql_match} = qq{ <div class="alert alert-danger">Error</div> };
    }
    # end check profile exists
  } else {
    $in{sql_match} = qq{<button type="button" class="btn btn-danger disabled">$in{user}</button>};
  }

  # final return
  return $in{sql_match};
}
# end sub profile


=head2 Save profile
  Data received from /admin/profile/:user
  save data to table profile
=cut

sub profile_save {
  my $c = shift;
  my %in = ( sql => '', @_, );
  my %out = ();
  my $insert_profile = '';
  if ( $in{sql} ne '') {
    $insert_profile = $dbh->prepare( qq{ $in{sql} } );
    $insert_profile->execute();
  }
  else {
    $insert_profile = qq{ERROR103 SQL Empty};
  }

}
# end save profile

=head2 Update profile SQL
  Data received from /admin/profile/:user
  save data to table profile
=cut

sub profile_update {
  my $c = shift;
  my %in = ( sql => '', @_, );
  my %out = ();
  my $update_profile = '';
  if ( $in{sql} ne '') {
    $update_profile = $dbh->prepare( qq{ $in{sql} } );
    $update_profile->execute();
  }
  else {
    $update_profile = qq{ERROR103 SQL Empty for update };
  }

}
# end update profile


=head2 Profile View SQL

=cut

sub profile_view {

  my $c = shift;

    my %in = (
      user => '',
      sql_table_users => 'users',
      sql_table_profile => 'profile',
      @_,
    );

    # get/verify logged in user
    my $check_user = $dbh->prepare( qq{ SELECT `username` from `$in{sql_table_users}` WHERE `username` = "$in{user}" } );
    $check_user->execute();
    my $get_u = $check_user->fetchrow();

    #
    if ( $in{user} eq $get_u ) {
      $in{sql_match} = qq{<button type="button" class="btn btn-primary disabled">$get_u</button>};
      # profile
      # check if profile exists
      my $check_profile = $dbh->prepare( qq{ SELECT count(`id`) from `$in{sql_table_profile}` WHERE `username` = "$in{user}" LIMIT 0, 1} );
      $check_profile->execute();
      my $get_profile = $check_profile->fetchrow();

      #
      my @get_profile_data = ('');
      # form for editing
      if ( $get_profile >= '1' ) {
        # get profile data from table profile (for updating )
        my $check_profile_data = $dbh->prepare( qq{ SELECT `id`, `username`, `created`, `firstname`, `lastname`, `email`, `description` from `$in{sql_table_profile}` WHERE `username` = "$in{user}" LIMIT 1} );
        $check_profile_data->execute();
        @get_profile_data = $check_profile_data->fetchrow_array();
      } else {
        $get_profile_data[0] = qq{ERROR 215}
      }

      return @get_profile_data;
    } else {
      return qq{No data};
    }

}





1;
