#! /usr/bin/perl

use Date::Parse;


while (<>) {
  s!\s+$!!;  # remove trailing whitespace

  # Quick skips
  next if m!^\d+\s+!;   # skip number-only lines = hymns
  next if m!^From \d+!; # From 34534523451
  next if m!^0in 0!;    # 0in 0
  next if m!^Jun 23!;   # spurious date looks like book chapter


  if (m!^(Date|Sent): (.*)!) {
    $datestr = $2;
    $datestr =~ s! at ! !;
    $datestr =~ s!, ! !g;
    $seconds = str2time($datestr);

    if    (/Sat/) { $seconds += 1*86400 }
    elsif (/Fri/) { $seconds += 2*86400 }
    elsif (/Thu/) { $seconds += 3*86400 }
    elsif (/Wed/) { $seconds += 4*86400 }
    elsif (/Tue/) { $seconds += 5*86400 }
    elsif (/Mon/) { $seconds += 6*86400 }

    @tary = localtime($seconds);

    $date = sprintf "%4d-%02d-%02d", $tary[5]+1900, $tary[4]+1, $tary[3];
    #print STDERR "$datestr --> $date  ($tary[6])\n",
  }

  if (m!^(am|pm)\b!) {
    $ampm = $1;
  }

  if (m!^((\d )?\w+ \d+(\:\d+)?)!) {
    $firstverse = $1;
    $firstverse =~ s!Ecc !Ecclesiastes !;
    $firstverse =~ s!Num !Numbers !;
    $firstverse =~ s!Ps !Psalm !;
    $firstverse =~ s![Pp]hil !Philippians !;
    if (exists($sundayaft{$firstverse})) {
      $prv = $sundayaft{$firstverse};
      $new = $date;
      if ($prv ne $new) {
	print "DATE CLASH: $firstverse $prv $new\n";
      }
    }
    $emaildate{$firstverse} = $datestr;
    $sundayaft{$firstverse} = $date;
    $serviceof{$firstverse} = $ampm;
  }

}

for $psg (sort keys %emaildate) {
  printf "%-20s $sundayaft{$psg} $serviceof{$psg}\t$emaildate{$psg}\n", $psg;
}

