#! /usr/bin/perl

use lib "/home/tina/bin";
use Rube;


$PRE = Rube::slurp( "pre.xml");
@ITM = Rube::slurp("item.xml");
$PST = Rube::slurp("post.xml");
$mp3dir = "http://escondidoopc.org/sites/default/files/sermons";

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


#print $PRE;

while (<>) {
  $mp3 = m!sermon_(.*mp3)!;
  $mp3 = $1;
  $mp3url = "$mp3dir/$mp3";


  if ($mp3 eq 'Deut4v25-40_and_Deut30_keele.mp3') {
    $book = 'Deut';
    $chp1 = 4;
    $vbeg = 25;
    $vend = 42;
    $chp2 = 30;
    $name = 'Keele';
    correct_name_book($name, $book);
    $psg = 'Deut 4:25-40; Deut 30';
  } elsif ($mp3 eq 'Ezra1_Ezra6v13-22_Nehemiah13v30-31_keele.mp3') {
    $book = 'Ezra;Nehemiah';
    $psg = 'Ezra-Nehemiah';
    $name = 'Keele';
  } elsif ($mp3 eq 'Jeremiah22v1-23-23-8_Keele.mp3') {
    $book = 'Jeremiah';
    $chp1 = 22;
    $vbeg = 1;
    $chp2 = 23;
    $vend = 8;
    $name = 'Keele';
    correct_name_book($name, $book);
    $psg = 'Jeremiah 22:1-23:8';
  } elsif ($mp3 eq 'Matt3v1-2_4v17_keele_0.mp3') {
    $book = 'Matt';
    $chp1 = 3;
    $vbeg = 1;
    $vend = 2;
    $chp2 = 4;
    $vers = 17;
    $name = 'Keele';
    correct_name_book($name, $book);
    $psg = 'Matt 3:1-2; Matt 4:17';
  } elsif ($mp3 =~ m!^(\d*\w+?)(\d+)v(\d+)\-(\d+)_(\w+)\.mp3!) {
    $book = $1;
    $chap = $2;
    $vbeg = $3;
    $vend = $4;
    $name = $5;
    correct_name_book($name, $book);
    $psg = "$book $chap:$vbeg-$vend";
  } elsif ($mp3 =~ m!^(\d*\w+?)(\d+)v(\d+)\-(\d+)v(\d+)_(\w+)\.mp3!) {
    $book = $1;
    $chp1 = $2;
    $vbeg = $3;
    $chp2 = $4;
    $vend = $5;
    $name = $6;
    correct_name_book($name, $book);
    $psg = "$book $chp1:$vbeg-$chp2:$vend";
  } elsif ($mp3 =~ m!^(\d*\w+?)(\d+)v(\d+)_(\w+)\.mp3!) {
    $book = $1;
    $chap = $2;
    $vers = $3;
    $name = $4;
    correct_name_book($name, $book);
    $psg = "$book $chap:$vers";
  } elsif ($mp3 =~ m!^(\d*\w+?)(\d+)\-(\d+)_(\w+)\.mp3!) {
    $book = $1;
    $chp1 = $2;
    $chp2 = $3;
    $name = $4;
    correct_name_book($name, $book);
    $psg = "$book $chp1-$chp2";
  } elsif ($mp3 =~ m!^(\d*\w+?)(\d+)_(\w+)\.mp3!) {
    $book = $1;
    $chap = $2;
    $name = $3;
    correct_name_book($name, $book);
    $psg = "$book $chap";
  } elsif ($mp3 =~ m!^(\d*\w+?)(\d+)v(\d+)\-(\d+)\-(Keele)\.mp3!) {
    $book = $1;
    $chap = $2;
    $vbeg = $3;
    $vend = $4;
    $name = $5;
    correct_name_book($name, $book);
    $psg = "$book $chap:$vbeg-$vend";
  } elsif ($mp3 =~ m!^(\d*\w+?)(\d+)v(\d+)\-(\d+)\.mp3!) {
    $book = $1;
    $chap = $2;
    $vbeg = $3;
    $vend = $4;
    $name = 'Keele';
    correct_name_book($name, $book);
    $psg = "$book $chap:$vbeg-$vend";
  } elsif ($mp3 =~ m!^(\d*\w+?)(\d+)v(\d+)\-(\d+)v(\d+)\.mp3!) {
    $book = $1;
    $chp1 = $2;
    $vbeg = $3;
    $chp2 = $4;
    $vend = $5;
    $name = 'Keele';
    correct_name_book($name, $book);
    $psg = "$book $chp1:$vbeg-$chp2:$vend";
  } else {
    print "Can't parse $mp3\n";
  }

  

  printf "%-30s %-15s $mp3\n", $psg, $name;


  
  $namect{$name}++;
  $bookct{$book}++;

  @item = @ITM;
  for (@item) {
    


  }

  #for (@item) { print }
}

print "Names:\n";
for (sort keys %namect) {
  print "$namect{$_}\t$_\n";
}

print "\n\nBooks:\n";
for (sort keys %bookct) {
  print "$bookct{$_}\t$_\n";
}

#print $PST;
