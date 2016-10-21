$fn=50;
rotate([180,0,180]) translate([0,0,-55]) color("blue") cover();

% difference(){
	cylinder(r=16, h=110, center=true);
	cylinder(r=12, h=110, center=true);
//	translate([0,5,60])cube([40, 30,20, ] ,center=true);
	ventHole();
	translate([0,0,25]) ventHole();
	translate([0,0,-25]) ventHole();
	translate([-15,0,-20])cube([10,3,80], center=true ); // later cut 
	translate([0,-15,-20])cube([3,10,80], center=true ); // top cut head end
	translate([0,-15,65])cube([3.2,10,30], center=true ); // top cut tail end
//	translate([0,0,50]) rotate([0,0,90]) slit2();
	slit2();
	translate([0,0,12]) slit2();
	translate([0,0,-12]) slit2();
	translate([0,0,-24]) slit2();
	translate([0,0,-36]) slit2();
	translate([0,0,-48]) slit2();

}

module ventHole() {
	rotate([0,90,0])translate([0,0,20]) cylinder (r=3, h=40, center=true);
}

module slit2() {
	translate([-13,3,0])rotate([0,90,0]) slit();
	}

module slit(){
	cylinder(r=1.7, h=10, center=true);
	rotate([0,0,135]) translate([0,1.7,0]) cube([3.4,4,10], center=true);
}

//!cover();
module cover(){
	h2=4;
	difference(){
		union(){
		translate([0,0,h2/2])	cylinder(r=12, h=h2, center=true);
		cylinder(r=15.6, h=2, center=true);
		}
		translate([0,-1,0]) rotate([0,0,90]) cylinder(r=3.2, h=9, center=true);
		translate([0,14,0]) cube([6.4,30,10], center=true ); // verticl cut 
		rotate([90,0,0]) translate([0,1.5,0]) cylinder(r=1.6,h=20); //screw
		translate([0,-9,0]) cube ([6,3,9], center=true) ; //hex nut
	}
}


translate([0,0,-50]) color("red") nosecone();
module nosecone() {
	difference (){
		cylinder(r=12.2, h=29.4);
		cylinder(r2=11, r1=8.5/2, h=30);
		rotate([90,0,-90]) translate([0,3,0]) cylinder(r=1.6,h=20); //screw
		}
}


	

