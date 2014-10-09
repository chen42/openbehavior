#!/usr/bin/perl
#
use Date::Calc qw(Day_of_Week);

$ampm=$ARGV[1] ;
$ratID=$1 if ($ARGV[0]=~/(.+)\.csv/);

#the last Sun is added to be compatible with other scirpts
my @abbrw= qw(Sun Mon Tue Wed Thu Fri Sat Sun);
#my @abbr = qw( Jan Feb Mar Apr May Jun Jul Aug Sep Oct Nov Dec );

if ( $ratID=~s/(201\d)-(\d\d)-(\d\d)//) {
	$day="$2-$3-$1";
	$wday=Day_of_Week($1,$2,$3);
} else {
	my ($sec,$min,$hour,$mday,$mon,$year,$wday,$yday,$isdst) = localtime(time);
	$year += 1900; ## $year contains no. of years since 1900, to add 1900 to make Y2K compliant
	$mday=$mday;
	$wday=$wday;
	$mon++;
	my $day="$mon\-$mday\-$year"; 
}

open(W, "sort /home/hao/data/saccNicSA/bodyweight.csv|") || die;
while (<W>) {
	chomp;
	@ary=split(/\t/,$_);
	next if ($ary[2]!~/\d/);
	$weight{$ary[1]}=$ary[2];# if ($weight{$ary[1]}<$ary[2]);
#	$drops{$ary[1]}=$ary[3]; # injections
}

#$match{"c135"}=$drops{"c130"};
#$match{"c137"}=$drops{"c131"};
#$match{"c138"}=$drops{"c132"};
#$match{"c136"}=$drops{"c133"};
open(IN, $ARGV[0]) || die; 
while (<IN>) { 
	$out1.="\\$_"; 
	chomp; 
	$_=~s/"//g;
	@l=split(/,|\t/, $_); 
	next if (!$l[2]); 
	next if (!$l[9]);

	if (substr($l[10],-4) eq $l[2]){
		$aid=$l[10]; 
	}else{
		$aid=$l[2];
	}


	$warning.="! 6ml Syringe is not nicotine for $aid in box $l[1] to run Nic SA\n" if (($l[9]=~/nic\d\d/i) && ($l[4] !~/nic/i));
	$warning.="! 6ml Syringe is not saline for $aid in box $l[1] to run Saline SA\n" if (($l[9]=~/sal\d\d/i) && ($l[4] !~/sal|x/i));
	$warning.="! remove demo for $aid in box $l[1] to run extinction\n" if (($l[9]=~/ext/i) && ($l[5] !~/x|^$/i));
	$warning.="! remove bottle for $aid in box $l[1] to run extinction\n" if (($l[9]=~/ext/i) && ($l[6] !~/x|^$/i));
	$warning.="! remove syring for $aid in box $l[1] to run extinction\n" if (($l[9]=~/ext/i) && ($l[4] !~/x|^$/i));
	$warning.="! clean spout is needed for $aid in box $l[1] to run extinction\n" if (($l[9]=~/ext/i) && ($l[8] !~/clean/i));
	$warning.="! 10ml syring is not GrapeOnly for $aid in box $l[1] to run OdorReinstatment\n" if (($l[9]=~/odorRein/i) && ($l[8] !~/GrapeOnly/i));
	$warning.="! remove bottle for $aid in box $l[1] to run OdorReinstatment\n" if (($l[9]=~/odorRein/i) && ($l[6] !~/x/i));
	$warning.="! remove demo for $aid in box $l[1] to run OdorReinstatment\n" if (($l[9]=~/odorRein/i) && ($l[5] !~/x/i));
	$warning.="! 10ml syring is not QuinineOnly for $aid in box $l[1] to run TasteReinstatment\n" if (($l[9]=~/TasteRein/i) && ($l[8] !~/QuinineOnly/i));
	$warning.="! remove bottle for $aid in box $l[1] to run TasteReinstatment\n" if (($l[9]=~/TasteRein/i) && ($l[6] !~/x/i));
	$warning.="! remove demo for $aid in box $l[1] to run TasteReinstatment\n" if (($l[9]=~/TasteRein/i) && ($l[5] !~/x/i));
	$warning.="! pse need demo rat $aid in box $l[1]\n" if (($l[9]=~/pse/i) && ($l[5] !~/cgmt|rndm/i));
	$warning.="! nse need demo rat $aid in box $l[1]\n" if (($l[9]=~/nse/i) && ($l[5] !~/cgmt|rndm/i));
	$warning.="! pse need bottle for demo $aid in box $l[1]\n" if (($l[9]=~/pse/i) && ($l[6] =~/x/i));
	$warning.="! remove bottle for nse $aid in box $l[1]\n" if (($l[9]=~/nse/i) && ($l[6] !~/x/i));
	$warning.="! quinine rats should be run with noav: $aid in box $l[1]\n" if (($l[9]!~/noav/i) && ($l[8] =~/quin/i) && $l[9]!~/cue/i);
	$warning.="! full cue reinst needs quinine or sacc syring: $aid in box $l[1]\n" if (($l[8] !~/quin|sacc/i) && $l[9]=~/fullcue/i);
	$warning.="! full cue reinst needs demo: $aid in box $l[1]\n" if (($l[5] !~/demo|rndm|cgmt/i) && $l[9]=~/fullcue/i);
	$warning.="! full cue reinst needs SaccGrape bottle: $aid in box $l[1]\n" if (($l[6] !~/sacc/i) && $l[9]=~/fullcue/i);

#FR
	$prog="R_FRx_IR_AV23h_122012"   if (($l[9]=~/23h/i) & ($l[9]=~/fr/i) & ($l[9]!~/noav/i));
	$prog="R_FRx_IR_noAV23h_102113" if (($l[9]=~/23h/i) & ($l[9]=~/fr/i) & ($l[9]=~/noav/i));
	$prog="R_FRx_IR_AV_120413"   if ($l[9]=~/fr/i); # & ($l[9]=~/av/i));
	$prog="R_FRx_IR_noAV_112513" if ($l[9]=~/noav/i);
	$prog="R_FRx_IR_noAV_init8injmax05272014" if ($l[9]=~/noav/i & $l[9]=~/day1/);

	$prog="R_FRx_IR_noAV_yoked_".$1 if ($aid=~/(k\d+)/i);

	#mice
	$prog="SA_FR10_ir_081710" 	   if (($l[3]=~/mn/i) & ($l[9]=~/fr10/i) & ($l[9]!~/noav/i));
	$prog="SA_FR10_ir_noav_062012" if (($l[3]=~/mn/i) & ($l[9]=~/fr10/i) & ($l[9]=~/noav/i));

## PR
	$prog="SA_PR_020411" if ($l[9]=~/PR/i);
	$prog="SA_PR_noav_012611" if ($l[9]=~/prnoav/i);
	$prog="micePR_noav_061812" if (($l[3]=~/mn/i) & ($l[9]=~/pr/i) & ($l[9]=~/noav/i));
	$prog="M_nic_pr" if ($l[9]=~/micepr|micelnic\d*pr/i);

#ext
	$prog="SA_ext081610" if ($l[9]=~/ext/i) ;   # & ($l[3]=~/mn/)); 
	$prog="R_ext1h" if (($l[9]=~/ext_1h|ext1h/i) & ($l[3]!~/mn/)); 

#reinstate
	$prog="R_OGScue_Reins_3h_100312 " if  ($l[9]=~/reinst/i);
	$prog="R_OGScue_Reins_072612 " if  (($l[9]=~/reinst/i) & ($l[9]=~/1h/));
	$prog="M_OGScue_Reins_072812 " if (($l[9]=~/reinst/i) & ($l[3]=~/mn/i));

#mice lever / food
	$prog="miceFood_0929" if ($l[9]=~/miceFood/i);
	$prog="miceNicLever_0929" if ($l[9]=~/micelNic|micelsal/i);
	$prog="miceNicLeverto60_0929" if ($l[9]=~/micel.*fr5to60/i);
	$prog="miceNicLeverext_1019" if ($l[9]=~/micelext/i);

#forced inj
	$prog="R_ForceInjx_081612" if ($l[9]=~/forceinj/i);
	print "<<<< $prog >>>>\n";
	$o=1.2; #nic30
	$o=0.1 if ($l[9]=~/nic0|sal0|demoTraining/i);
	$o=0.5 if ($l[9]=~/nic15|sal15/i);
	$o=2 if ($l[9]=~/nic60|sal60/i);
	$o=3 if ($l[9]=~/nic90|sal90/i);
	$o=4 if ($l[9]=~/nic120|sal120/i);
	$R=$1 if ($l[9] =~/fr(\d+)/i);
	$C=$1 if ($l[9]=~/forceinj(\d+)/i);
#	print $l[9], "\n";

	if (!$weight{$aid}){
		if ($l[9]=~/adul/i) {
			$weight{$aid}=250.001;
		} elsif ($l[3]=~/^m/) {
			$weight{$aid}=20.001;
		} else{
			$weight{$aid}=120.001 ;
		}
		$l[3]="noWeight";
		$warning.="! default weight is used for $aid\n" if ($l[0] !~/\?/); 
	}

	if ($weight{$aid}>400 & $aid!~/^M/) {
		$l[3]="checkWeight";
		$warning.="$ary[1] >400g, check";
	}

	if (($weight{$aid} <90) && ($l[3]!~/^m/i)){
		$warning.= "! weight of $aid = $weight{$aid} is less than 90g\n"; 
	}

# detect if multiple animals have same weight,indicative of error when entering weights	

	$weightcnt{$weight{$aid}} ++;
	$weightgrp{$weight{$aid}}.="$aid\t";

	next if ($aid=~/sess/i);
	$out1.= "\r\nLOAD BOX $l[1] SUBJ $aid EXPT $l[3] GROUP $l[8]$l[9] PROGRAM $prog\r\n";
	$out1.= "SET W VALUE $weight{$aid} MAINBOX $l[1] BOXES $l[1]\r\n";
#	$out1.= "SET Z VALUE $match{$aid} MAINBOX $l[1] BOXES $l[0]\r\n" if ($match{"$aid"});
	$out1.= "SET O VALUE $o MAINBOX $l[1] BOXES $l[1]\r\n" if ($o);
	$out1.= "SET R VALUE $R MAINBOX $l[1] BOXES $l[1]\r\n" if ($R);
	$out1.= "SET C VALUE $C MAINBOX $l[1] BOXES $l[1]\r\n" if ($C);
}

#$out="mac/@abbrw[$wday]"."$ampm"."_". $ratID."_$day.mac" ;

$out="mac/@abbrw[$wday]"."_$day\_". $ratID.".mac" ;


foreach $w (keys %weightcnt) {
	if ($weightcnt{$w} >= 3) {
		$warning .= "! weight for all the following rats is $w		[$weightgrp{$w}]\n";
	}
}


if ($warning) {
	open(W, ">>mpc.warning") || die "can't open warning file for writing\n"; 
	print W "\n\n!!! warning for $out\n$warning\n";
	close (W);
}

open(OUT, ">$out") || die "can't open $out for writing";
print OUT "$out1";

close (OUT);
$dropbox=$out;
$dropbox=~s/mac/Dropbox\/HaoLabShare\/macro/;


open(OUT, "$out") ||die;
while (<OUT>) {
	if($_=~/^\\/) {
		$_=~s/"//g;
		@l=split(/,/,$_) ;
		$id=$aid;
		open(IND, ">/home/hao/Dropbox/HaoLabShare/macro/singleAnimal/$id.mac") || die;
		next;
	}
	print IND $_;
	print  $_;
}

close(IND);

system("cp $out $dropbox");

