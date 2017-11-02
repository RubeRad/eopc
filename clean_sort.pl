#! /bin/perl

use Date::Parse;
use lib "$ENV{HOME}/bin";
use Rube;

@lines = (<>);
for (@lines) { s!\s+$!! }
$all = join "\n", @lines;

@mails = split /From \d+\@xxx/, $all;

for $mail (@mails) {
  next unless $mail =~ m!\n
                         (am\.?
                         \n
                         .*?)
                         \n\n!sx;
  $amtxt = $1;

  next unless $mail =~ m!\nDate: (..., \d\d? ... \d{4} \d\d:\d\d:\d\d) \-0[78]00!;
  $date = $1;
  $posix = str2time($date);

  $mail =~ m!\nFrom: (.*?)\n!;
  $from = $1;


  $pmtxt = '';
  if ($mail =~ m!\n
                 (pm\.?
                 \n
                 .*?)
                 \n\n!sx) {
    $pmtxt = $1;
  }

  $info{$posix} = "Date: $date\nFrom: $from\n$amtxt\n$pmtxt";
}

for $posix (sort keys %info) {
  print "$info{$posix}\n\n";
}
