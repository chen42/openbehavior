$fn=100;

module volhouse () {  /* voltage converter*/
	difference(){
		cube([22,27,12],center=true);
		cube([18,23,12.1],center=true);
	}
}

module screw() {
	translate([0,0,-10])	cylinder(r=2.1, h=20);
}

module pole(){
	difference(){
		cube([8,8,12],center=true);
		cylinder(r=1.9, h=6.1);
	}
}


module screw4(){
	translate([x0/2-5, y0/2-5, 0]) screw();
	translate([-x0/2+5, y0/2-5, 0]) screw();
	translate([x0/2-5, -y0/2+5, 0]) screw();
	translate([-x0/2+5, -y0/2+5, 0]) screw();

}

module mounting(){
	cube([14,12,3],center=true);
}

module mounting4(){
	difference(){
		union(){
			translate([x0/2-4, y0/2-6, 0]) mounting();
			translate([-x0/2+4, y0/2-6, 0]) mounting();
			translate([x0/2-4, -y0/2+2.5, 0]) mounting();
			translate([-x0/2+4, -y0/2+3, 0]) mounting();
		}
		screw4();

	}
}


x0=81; /* cover width */
y0=115; /* cover length */

module cover(){
	difference() {
		cube([x0,y0,3], center=true);
		translate([0,60,-3]) cylinder(r=30,h=5);
		screw4();

	}
	y=-20;
	x=20;
	z=4.5;
	translate([x,y,z]) volhouse();
	translate([-x,y,z]) volhouse();
	translate([x+13,y, z]) pole();
	translate([-x-13,y, z]) pole();
}

module case(){
	x0=90;
	y0=125;
	z0=50;
	difference(){
		cube([x0, y0, z0], center=true); 
		translate([0,0,4]) cube([x0-4, y0-4, z0+5], center=true); 
		translate([0,y0/2,z0-42-4]) cube([56, 8, 42.2], center=true);
	}
	translate([35, -15, -25]) rotate([0,0,90]) mounting_pi();
	translate([0,0,20]) mounting4();
}


module mounting_m25(innR=1.9){ // screw 
	difference(){
		cylinder(r=3.8, h=10);
		cylinder(r=innR, h=10);
	}
}

module mounting_pi(){
	mounting_m25();
	translate([58,0,0]) mounting_m25();
	translate([0,49,0]) mounting_m25();
	translate([58,49,0]) mounting_m25();
} 

module volcover(){
	sx=33;
	sy=20;
	sz=10;
	difference(){
		translate([0, sy,sz]) cube([74,14,3],center=true);
		translate([sx, sy,sz])screw();
		translate([-sx, sy,sz])screw();
	}
}


translate([0,0,25]) rotate([0,180,180]) cover();
%case();
volcover();


