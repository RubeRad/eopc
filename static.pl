#! /bin/perl


open BOOKS, 'books.txt';
while (<BOOKS>) {
  chomp;
  ($num, $book) = (split /,/);
  $n{$book} = $num;
}


$root  = "http://escondido-opc.org/sites/default/files/sermons";
$root2 = "http://escondido-opc.org/wp-content/uploads/sermons";
open PARSED, "parsed_mp3s.csv"; # all the old files
while (<PARSED>) {
  next unless /\S/;
  ($file, $name, $book, $pass) = (split /,/);
  $bookOf{$file} = $book;
  $passOf{$file} = $pass;
  $nameOf{$file} = $name;
  $htmlOf{$file} = qq(<p><a href="$root/sermon_$file">$book $pass ($name)</a>\n);
}
close PARSED;

while (<>) { # a dump of all the wp-content/uploads/sermons/20NN/NN/*.mp3
  # isolate the mp3 filename
  next if     m!ghost!;
  next unless m!uploads/sermons/(20\d\d/\d\d)/(.*mp3)!;
  $dir  = $1;
  $file = $2;

  # determine the book
  ($f=$file)=~ s!sermon_!!;
  $f =~ s!(^[123]?\D+)!!;
  $book = $1;
  $book =~ s!_$!!;
  $book =~ s!\-$!!;
  die "Can't find $book\n" unless exists $n{$book};

  # Is there a name?
  if ($f =~ m!\d\.mp3!) { # nope
    $name = '';
  } else {
    $f =~ s!(\D+)\.mp3!!;
    $name = $1;
    $name =~ s!_!!g;
  }

  # determine the passage
  $pass = '';
  $f =~ s!\.mp3!!;
  # at this point should be only chapter and verse numbers left
  @d = split /\D/, $f;
  if (@d==1) { # Psalm 45
    $pass = $d[0];
  } elsif (@d==3) { # Luke 12:34-56
    $pass = "$d[0]:$d[1]-$d[2]";
  } elsif (@d==4) { # Luke 12:34-13:56
    $pass = "$d[0]:$d[1]-$d[2]:$d[3]";
  }
  die "Can't determine passage: $f ($file)\n" unless $pass;

  $bookOf{$file} = $book;
  $passOf{$file} = $pass;
  $nameOf{$file} = $name;
  if ($name) {
    $htmlOf{$file} = qq(<p><a href="$root2/$dir/$file">$book $pass ($name)</a>\n);
  } else {
    $htmlOf{$file} = qq(<p><a href="$root2/$dir/$file">$book $pass</a>\n);
  }
}

sub bibleOrder {
  $na = $n{$bookOf{$a}};
  $nb = $n{$bookOf{$b}};
  $passOf{$a} =~ /(\d+):?(\d*)/; my $ca = $1; my $va = $2;
  $passOf{$b} =~ /(\d+):?(\d*)/; my $cb = $1; my $vb = $2;
  if ($a =~ /Ezra.*Nehemiah/) { $na = $n{Ezra}; $ca=$va=0 }
  if ($b =~ /Ezra.*Nehemiah/) { $nb = $n{Ezra}; $cb=$vb=0 }
  if ($na==0) { print STDERR "PROBLEM with $a\n"; }
  if ($nb==0) { print STDERR "PROBLEM with $b\n"; }
  return ($na <=> $nb or
	  $ca <=> $cb or
	  $va <=> $vb);
}


for $file (sort bibleOrder keys %htmlOf) {
  $book = $bookOf{$file};
  if ($book ne $curBook) {
    $html .= qq(<h2>$book</h2>\n);
    $curBook = $book;
  }
  $html .= $htmlOf{$file};
}

print $html;


