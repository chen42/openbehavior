$fn=100;
module slide(){
	cube([13,35,4],center=true);
}

module cutter(){
	difference(){
		cube ([26,26,14], center=true); // outside
		translate([0,4,0]) cube ([14,26,15], center=true); // inside
		for (i = [8:11])  { 
			translate([0,i,1]) cube ([30,0.4,14], center=true); // knife cuts
			}
	}
}

module base(){
	difference (){
		cube ([38,40,16], center=true);
		translate([0,5,4]) cube ([28,34,20], center=true);
		}
	translate([16,18,13]) cube([4,2,10], center=true);
	translate([-16,18,13]) cube([4,2,10], center=true);
	translate([16,11,13]) cube([4,2,10], center=true);
	translate([-16,11,13]) cube([4,2,10], center=true);
}

slide();
//translate([0,5,1]) cutter();

//base();

