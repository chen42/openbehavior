#!/usr/bin/perl 

# reformat text export from iDoneThis.com so that the indentations are maintained when pasted to workflowy.

# need to open the output from a browser and then copy the text.
 
use  Date::Simple qw/ date today /;

while(<>){
	chomp;
	$_=~s/\r//;
	next if( $_=~/Progress made by|Created with http/);
	if ($a==-1) {
		if ($_=~s/(^Hao Chen|^wescarter|^Wang, Tengfei|^hanwenyan1)/<li>$1<ul>/){
			print $_, "\n";
			$a=1;
			next;
		}
	}
	if ($a==1) {
		if ($_=~s/(^Hao Chen|^wescarter|^Wang, Tengfei|^hanwenyan1)/<\/ul><\/li><li>$1<ul>/){
			print $_, "\n";
			next;
		}
	}

	if ($_=~/(201\d-\d+-\d+)/) {
		my $dow=date($1);
		#print "<\/ul><\/li><ul>$_\t" , $dow->strftime("%A"), "\n";
		print "</ul></li></ul></li></ul><ul><li>$_\t" , $dow->strftime("%A"), "<ul>\n";
		$a=-1;
		next;
	}
	next if( $_!~/\w/);
	$_=~s/^- -//;
	$_=~s/^- \+//;
	$_=~s/^-//;
	print "<li>$_</li>\n";
}

