#! /bin/perl


open BOOKS, 'books.txt';
while (<BOOKS>) {
  chomp;
  ($num, $book) = (split /,/);
  $n{$book} = $num;
}


$root = "http://escondido-opc.org/sites/default/files/sermons";

while (<>) {
  next unless /\S/;
  ($file, $name, $book, $pass) = (split /,/);
  $bookOf{$file} = $book;
  $passOf{$file} = $pass;
  $nameOf{$file} = $name;
  $htmlOf{$file} = qq(<p><a href="$root/sermon_$file">$book $pass ($name)</a>\n);
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


