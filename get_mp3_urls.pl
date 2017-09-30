#! /usr/bin/perl

# DEPENDENCIES:
# sudo apt-get install xsltproc



use Getopt::Std;
use FindBin;
use lib "$FindBin::Bin";
#use HTTP::Lite;
use LWP::UserAgent;
use lib "/home/tina/bin";
use Rube;

$|=1;

while (<>) {
  if (m!\"(http://escondidoopc.org/\?q\=sermons/.*?)\"!) {
    $url = $1;
    $ua = LWP::UserAgent->new;
    $res = $ua->get($url);
    print "$url:\t";
    if ($res->is_success) {
      $html = $res->decoded_content;
      if ($html =~ m!\"http:....escondidoopc.org..sites..default..files..sermons..(.*?mp3)\"!) {
	$mp3_url = $1;
	print "$mp3_url\n";
      } else {
	print "mp3 not found\n";
      }
    }
  }
}
