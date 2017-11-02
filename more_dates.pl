#! /bin/perl

use Date::Parse;

sub following_sunday {
  my $datestr = shift;
  $seconds = str2time($datestr);

  if    (/Sat/) { $seconds += 1*86400 }
  elsif (/Fri/) { $seconds += 2*86400 }
  elsif (/Thu/) { $seconds += 3*86400 }
  elsif (/Wed/) { $seconds += 4*86400 }
  elsif (/Tue/) { $seconds += 5*86400 }
  elsif (/Mon/) { $seconds += 6*86400 }

  @tary = localtime($seconds);

  return sprintf "%4d-%02d-%02d", $tary[5]+1900, $tary[4]+1, $tary[3];
}


while (<>) {
  s!\s+$!!;

  if (/^Date: (.*)/) {
    $date = $1;
    next;
  }

  if (/^\s*am\b/) {
    #print;
    #print "\n";
    <>; # first hymn
    $ot = <>;
    <>; # second hymn
    $nt = <>;

    if ($ot =~ /Sam/) { $psg = $ot }
    else              { $psg = $nt }
    #print "$psg\n";
    $psg =~ s!\s+$!!;
    $psg =~ s![oOnN][tT]:?!!;
    $psg =~ s!\s!!g;
    $psg =~ s!(\w)(\d)!\1 \2!;
    $psg =~ s!Scrip.*:!!;
    $psg =~ s!Text:!!;
    $psg =~ s!\(.*\)!!;
    $psg =~ s!\-+!\-!;

    printf "%-20s %s am\t$date\n", $psg, following_sunday($date), $date;

    next;
  }

  if (/^\s*pm\b/) {
    $_ = <>; # first hymn
    $psg = <>;
    $psg =~ s!\s+$!!;
    $psg =~ s!\s!!g;
    $psg =~ s!(\w)(\d)!\1 \2!;
    $psg =~ s!Scrip.*:!!;
    $psg =~ s!Text:!!;
    $psg =~ s!\(.*\)!!;
    $psg =~ s!\-+!\-!;
    $psg =~ s!\=E2.*:!-!;

    printf "%-20s %s pm\t$date\n", $psg, following_sunday($date), $date;

    next;
  }

}
