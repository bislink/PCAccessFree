#!/usr/bin/env perl

package Lang;
sub new { bless {}, shift }
sub english {
  my $c = shift;
  my %in = (
    file => "",
    @_,
  );
  my $out;
  $out .= qq{<form action="/admin/savesettings" method="post">};
  if ( -f "$in{file}" ) {
    if ( open(my $file, "$in{file}") ) {
      while ( my $line = <$file> ) {
        #$out .= qq{$line };
        chomp $line;
        next if $line =~ /^$/;
        my ($name, $value) = split(/\=/, $line, 2);
        $out .= qq{
          <div class="mb-3">
            <label for="$name" class="form-label">$name</label>
            <input type="text" class="form-control" id="$name" aria-describedby="name" value="$value">
          </div>
        };
      }
    } else {
      $out = qq{<div class="alert alert-danger">Unable to open file</div> };
    }
  } else {
    $out = qq{<div class="alert alert-danger">Could not open/find file</div> };
  }

  $out .= qq{<div class="mb-3"><input type="submit" value="Save"></div></form>};

  return $out;

}
# end


=head2 Get User Language

=cut

sub get_language {

  my %in = (
    dir => '',
    @_,
  );

  my $default_language = '';

  my %lang = (
    error => ''
  );

  if ( -e -f "$in{dir}/lang/default-language.txt" )
  {
  	open( my $LANG, "$in{dir}/lang/default-language.txt") or $lang{error} = qq{ <div class="alert alert-warning">#61 $!</div> };
  	$default_language = <$LANG>;
  	close $LANG;
  	chomp $default_language;
  }
  else
  {
  	$default_language = 'en-us';
  }

  chomp $default_language;

  if ( -e -f "$in{dir}/lang/$default_language.txt" )
  {
  	open(my $DL, "<:encoding(utf-8)", "$in{dir}/lang/$default_language.txt" ) or $lang{error} = qq{<div class="alert alert-warning">#76 $!</div>};
  	my @dl = <$DL>;
  	#close $DL;

  	##while ( my $item = <@dl> )                # gets only first word!!
  	foreach my $item (@dl)
  	{
  		chomp $item;
  		my ( $left_item, $right_value ) = split(/\=/, $item, 2);

  		$lang{"$left_item"} = qq{$right_value};
  	}
  }
  else
  {
  	$lang{error} = qq{<div class="alert alert-danger">Could not open language file "$default_language" $in{dir} </div> };
  }

  return %lang;
}

# end get user language


1;
