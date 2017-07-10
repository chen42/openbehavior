$fn=100;
rotate([180,0,180]) translate([0,0,-55]) color("blue") cover();
innerR=15;
difference(){
	cylinder(r=18, h=110, center=true);
	cylinder(r=innerR, h=111, center=true);
	ventHole();
	translate([0,0,25]) ventHole();
	translate([0,0,-25]) ventHole();
	translate([-15,0,-20])cube([10,3,80], center=true ); // later cut 
	translate([0,-15,-20])cube([8,10,80], center=true ); // top cut head end
	translate([0,-13,63])cube([4,10,30], center=true ); // top cut tail end
	translate([-4,-14,50])  rotate([90,225,0]) slit(); // tail end screw slit
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
	cylinder(r=1.9, h=10, center=true);
	rotate([0,0,135]) translate([0,2,0]) cube([4,4,10], center=true);
}

module cover(){
	h2=8;
	difference(){
		union(){
		translate([0,0,h2/2])	cylinder(r=innerR-.7, h=h2, center=true);
		cylinder(r=17, h=2, center=true);
		}
		translate([0,-1,0]) rotate([0,0,90]) cylinder(r=3.2, h=25, center=true);
		translate([0,14,0]) cube([6.4,30,17], center=true ); // verticl cut 
		rotate([90,0,0]) translate([0,5,0]) cylinder(r=1.8,h=20); //screw
		//translate([0,-9,0]) cube ([6,3,9], center=true) ; //hex nut
	}
}


!translate([0,0,-50]) color("red") nosecone();
module nosecone() {
	difference (){
		cylinder(r=innerR-0.5, h=38);
		translate([0,0,-.1])cylinder(r2=innerR-1, r1=5, h=39);
		rotate([90,0,-90]) translate([0,3,4]) cylinder(r=1.8,h=18); //screw
		translate([0,-7,26])cube([8,16,25], center=true ); // top cut head end
		}
}


//cover2();	
module cover2(){
	difference(){
		union(){
			difference(){
				cylinder(r=18.5, h=2, center=true);
				translate([0,-15,0])cube([40,20,2], center=true);
			}
			h2=7; translate([0,0,h2/2-1])	cylinder(r=15, h=h2, center=true);

		}
		translate([0,10,0]) rotate([0,0,90]) cylinder(r=4, h=25, center=true);
		translate([0,14,0]) cube([8,10,17], center=true ); // verticl cut 
		rotate([90,0,0]) translate([0,3,6]) cylinder(r=1.4,h=10); //screw
		rotate([0,90,0]) translate([-6,-6,0]) cylinder(r=4,h=50, center=true); // horizontal groove
		translate([0,4,4])cube([40,25,4], center=true);
	}
}




