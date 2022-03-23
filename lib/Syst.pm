package Syst;
sub new { bless {}, shift }
sub settings {
  my $c = shift;
  my %in = (
    file => "",
    @_,
  );
  my $out;
  $out .= qq{};
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
            <input type="text" class="form-control" name="$name" aria-describedby="name" value="$value">
          </div>
        };
      }
    } else {
      $out = qq{<div class="alert alert-danger">Unable to open file</div> };
    }
  } else {
    $out = qq{<div class="alert alert-danger">Could not open/find file</div> };
  }

  $out .= qq{};

  return $out;

}
# end


sub settings_names_array {
  my $c = shift;
  my %in = (
    file => "",
    @_,
  );
  my @out = ();
  if ( -f "$in{file}" ) {
    if ( open(my $file, "$in{file}") ) {
      while ( my $line = <$file> ) {
        #$out .= qq{$line };
        chomp $line;
        next if $line =~ /^$/;
        my ($name, $value) = split(/\=/, $line, 2);
        chomp $name;
        push(@out, "$name");
      }
    } else {
      $out[0] = qq{<div class="alert alert-danger">Unable to open file</div> };
    }
  } else {
    $out[0] = qq{<div class="alert alert-danger">Could not open/find file</div> };
  }

  return @out;

}





1;
