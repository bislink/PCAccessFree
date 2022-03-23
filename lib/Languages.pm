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



1;
