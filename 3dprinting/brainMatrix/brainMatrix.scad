$fn=100;
module slider(){
	difference(){
		translate([0,-8,9])cube([28,28,14], center=true);
		translate([0,-6,9]) cube ([14,28,15], center=true);
	}
}

module cutter(){
	difference(){
		cube ([26,26,14], center=true); // outside
		translate([0,4,0]) cube ([14,26,15], center=true); // inside
		for (i = [3:6])  { 
			translate([0,i,1]) cube ([30,0.4,14], center=true); // knife cuts
			}
	}
}

module base(){
	cube ([38,40,4], center=true);
	translate([0,6,9]) cube ([13,28,17], center=true);
	translate([-19,0,2])side();
	translate([15,0,2])side();
}

module side(){
//	translate([16,13,13]) cube([4,2,h], center=true);
//	translate([-16,13,13]) cube([4,2,h], center=true);
	translate([0,-2,0]) cube([4,9,h]);
	h=14;
	translate([0,5,h]) cube([4,2,h]);
	translate([0,-2,h]) cube([4,2,h]);
}


color("yellow") translate([0,5,0]) slider(); // 
translate([0,-2,23]) cutter();

color("grey") base();

