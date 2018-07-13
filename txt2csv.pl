#! /bin/perl

# reverse parsed_mp3s.txt into parsed_mp3s.csv

while (<>) {
  chomp;
  ($book, $pass, $name, $file) = split;
  $book =~ s!1Cor!1 Corinthians!;
  $book =~ s!1John!1 John!;
  $book =~ s!1Peter!1 Peter!;
  $book =~ s!1Samuel!1 Samuel!;
  $book =~ s!1Thess!1 Thessalonians!;
  $book =~ s!1Timothy!1 Timothy!;
  $book =~ s!2Cor!2 Corinthians!;
  $book =~ s!2John!2 John!;
  $book =~ s!2Peter!2 Peter!;
  $book =~ s!2Samuel!2 Samuel!;
  $book =~ s!2Thess!2 Thessalonians!;
  $book =~ s!2Timothy!2 Timothy!;
  $book =~ s!Deut!Deuteronomy!;
  $book =~ s!Ecc!Ecclesiasties!;
  $book =~ s!Eph!Ephesians!;
  $book =~ s!Gal!Galatians!;
  $book =~ s!Gen!Genesis!;
  $book =~ s!Jer!Jeremiah!;
  $book =~ s!Matt!Matthew!;
  $book =~ s!Rev!Revelation!;
  
  print (join ',', $file, $name, $book, $pass, "\n");
}
