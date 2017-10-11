#! /usr/bin/perl

use Date::Parse;
use lib "$ENV{HOME}/bin";
use Rube;


$PRE = Rube::slurp( "pre.xml");
@ITM = Rube::slurp("item.xml");
$PST = Rube::slurp("post.xml");
$mp3dir = "http://escondidoopc.org/sites/default/files/sermons/sermon_";

sub correct_name_book {
  if ($_[0] =~ /keele/i)     { $_[0] = 'Keele' }
  if ($_[0] =~ /vandrunen/i) { $_[0] = 'VanDrunen' }
  if ($_[0] =~ /baugh/i)     { $_[0] = 'Baugh' }
  $_[0] = ucfirst($_[0]);

  if ($_[1] eq 'Number')     { $_[1] = 'Numbers' }
  if ($_[1] =~ /jeremiah/i)  { $_[1] = 'Jer' }
  if ($_[1] =~ /1sam/i)      { $_[1] = '1Samuel' }
  if ($_[1] =~ /firstcor/i)  { $_[1] = '1Cor' }
  if ($_[1] =~ /galatian/i)  { $_[1] = 'Gal' }
  if ($_[1] =~ /genesis/i)   { $_[1] = 'Gen' }
}

open DATE, "sermon_dates.txt";
while (<DATE>) {
  next if /DATE CLASH/;
  m!(.*?)\s+([\d-]{10}) ([ap]m)!;
  $psg = $1;
  $dateof{$psg} = $2;
  $ampmof{$psg} = $3;
}

sub find_date_of {
  my $psg = shift;
  my $dt = '';
  my $ap = '';
  my $tmp = '';
  if (exists $dateof{$psg}) {
    $dt = $dateof{$psg};
    $ap = $ampmof{$psg};
  }

  if ($dt eq '') {
    ($tmp = $psg) =~ s!-.*!!;
    if (exists($dateof{$tmp})) {
      $dt = $dateof{$tmp};
      $ap = $ampmof{$tmp};
    }
  }

  if ($dt eq '') {
    ($tmp = $psg) = s!:.*!!;
    if (exists($dateof{$tmp})) {
      $dt = $dateof{$tmp};
      $ap = $ampmof{$tmp};
    }
  }

  if ($dt eq '') {
    print STDERR "Can't find date for $psg\n";
    $nsec++;
    $time = sprintf "12:%02d:%02d", int($nsec/60), $nsec%60;
    $sdate = "2000-01-02";
    $ldate = "Sun, 2 Jan 2000";
  } else {
    $sdate = $dt;
    ($yyyy, $mon, $day) = (split /-/, $sdate);
    $ldate = sprintf "Sun, $day %s $yyyy",
      ['', 'Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun',
           'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']->[$mon];
    if ($ampm eq 'pm') { $time = "18:00:00" }
    else               { $time = "10:00:00" }
  }

  return ($sdate, $ldate, $time);
}


print $PRE;

$unum = 8999;
$bigint = 1506702000;

while (<>) {
  s!\s+$!!;
  next unless m!sermon_(.*mp3)!;
  $mp3 = $1;
  $mp3url = $mp3dir . $mp3;
  ($short=$mp3) =~ s!\.mp3!!;


  if ($mp3 eq 'Deut4v25-40_and_Deut30_keele.mp3') {
    $book = 'Deut';
    $chp1 = 4;
    $vbeg = 25;
    $vend = 42;
    $chp2 = 30;
    $name = 'Keele';
    correct_name_book($name, $book);
    $passage = 'Deut 4:25-40; Deut 30';
  } elsif ($mp3 eq 'Ezra1_Ezra6v13-22_Nehemiah13v30-31_keele.mp3') {
    $book = 'Ezra;Nehemiah';
    $passage = 'Ezra-Nehemiah';
    $name = 'Keele';
  } elsif ($mp3 eq 'Jeremiah22v1-23-23-8_Keele.mp3') {
    $book = 'Jeremiah';
    $chp1 = 22;
    $vbeg = 1;
    $chp2 = 23;
    $vend = 8;
    $name = 'Keele';
    correct_name_book($name, $book);
    $passage = 'Jeremiah 22:1-23:8';
  } elsif ($mp3 eq 'Matt3v1-2_4v17_keele_0.mp3') {
    $book = 'Matt';
    $chp1 = 3;
    $vbeg = 1;
    $vend = 2;
    $chp2 = 4;
    $vers = 17;
    $name = 'Keele';
    correct_name_book($name, $book);
    $passage = 'Matt 3:1-2; Matt 4:17';
  } elsif ($mp3 =~ m!^(\d*\w+?)(\d+)v(\d+)\-(\d+)_(\w+)\.mp3!) {
    $book = $1;
    $chap = $2;
    $vbeg = $3;
    $vend = $4;
    $name = $5;
    correct_name_book($name, $book);
    $passage = "$book $chap:$vbeg-$vend";
  } elsif ($mp3 =~ m!^(\d*\w+?)(\d+)v(\d+)\-(\d+)v(\d+)_(\w+)\.mp3!) {
    $book = $1;
    $chp1 = $2;
    $vbeg = $3;
    $chp2 = $4;
    $vend = $5;
    $name = $6;
    correct_name_book($name, $book);
    $passage = "$book $chp1:$vbeg-$chp2:$vend";
  } elsif ($mp3 =~ m!^(\d*\w+?)(\d+)v(\d+)_(\w+)\.mp3!) {
    $book = $1;
    $chap = $2;
    $vers = $3;
    $name = $4;
    correct_name_book($name, $book);
    $passage = "$book $chap:$vers";
  } elsif ($mp3 =~ m!^(\d*\w+?)(\d+)\-(\d+)_(\w+)\.mp3!) {
    $book = $1;
    $chp1 = $2;
    $chp2 = $3;
    $name = $4;
    correct_name_book($name, $book);
    $passage = "$book $chp1-$chp2";
  } elsif ($mp3 =~ m!^(\d*\w+?)(\d+)_(\w+)\.mp3!) {
    $book = $1;
    $chap = $2;
    $name = $3;
    correct_name_book($name, $book);
    $passage = "$book $chap";
  } elsif ($mp3 =~ m!^(\d*\w+?)(\d+)v(\d+)\-(\d+)\-(Keele)\.mp3!) {
    $book = $1;
    $chap = $2;
    $vbeg = $3;
    $vend = $4;
    $name = $5;
    correct_name_book($name, $book);
    $passage = "$book $chap:$vbeg-$vend";
  } elsif ($mp3 =~ m!^(\d*\w+?)(\d+)v(\d+)\-(\d+)\.mp3!) {
    $book = $1;
    $chap = $2;
    $vbeg = $3;
    $vend = $4;
    $name = 'Keele';
    correct_name_book($name, $book);
    $passage = "$book $chap:$vbeg-$vend";
  } elsif ($mp3 =~ m!^(\d*\w+?)(\d+)v(\d+)\-(\d+)v(\d+)\.mp3!) {
    $book = $1;
    $chp1 = $2;
    $vbeg = $3;
    $chp2 = $4;
    $vend = $5;
    $name = 'Keele';
    correct_name_book($name, $book);
    $passage = "$book $chp1:$vbeg-$chp2:$vend";
  } else {
    print "Can't parse $mp3\n";
  }

  

  #printf "%-30s %-15s $mp3\n", $passage, $name;


  
  $namect{$name}++;
  $bookct{$book}++;

  ($shortdate, $longdate, $time) = find_date_of($passage);

  $unum++;
  $bigint++;
  $book_lc = lc($book);
  $name_lc = lc($name);
  if ($book=~m!Mat|Mar|Luk|Joh|Act|Rom|Cor|Gal|Eph|Phi|Col|Thes|Tim|Heb|Pet|Jam|Rev!) {
    $testament = 'New Testament';
    $test      = 'new-testament';
  } else {
    $testament = 'Old Testament';
    $test      = 'old-testament';
  }

  @item = @ITM;
  for (@item) {
      #print STDERR "Line is : $_";
    next if (s!WDAY_DD_MMM_YYYY_HERE!$longdate! &&
	     s!TIME_HERE!$time!);
    next if (s!YYYY_MM_DD_HERE!$shortdate! &&
	     s!TIME_HERE!$time!);
    next if (s!PASSAGE_HERE!$passage!);
    next if   (s!SHORT_HERE!$short!);
    next if    (s!TIME_HERE!$time!);
    next if    (s!UNUM_HERE!$unum!);
    next if      (s!BOOK_LC!$book_lc! &&
                     s!BOOK!$book!);
    next if    (s!TESTAMENT!$testament! &&
                     s!TEST!$test!);
    next if      (s!NAME_LC!$name_lc! &&
                     s!NAME!$name!);
    next if  (s!BIGINT_HERE!$bigint!);
    next if (s!MP3_URL_HERE!$mp3url!);
  }

  for (@item) { print }
}


#print "Names:\n";
for (sort keys %namect) {
  #print "$namect{$_}\t$_\n";
}

#print "\n\nBooks:\n";
for (sort keys %bookct) {
  #print "$bookct{$_}\t$_\n";
}

print $PST;
