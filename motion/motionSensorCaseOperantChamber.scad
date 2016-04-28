$fn=100;

module mounting_m25(innR=1.6, h=10){ // screw 
	difference(){
		color("orange") cylinder(r=3.8, h);
		cylinder(r=innR, h=10);
	}
}

module mounting_pi(){
	translate([-58/2,-49/2,0]) mounting_m25();
	translate([58/2,-49/2,0]) mounting_m25();
	translate([-58/2,49/2,0]) mounting_m25();
	translate([58/2,49/2,0]) mounting_m25();
	translate([-10,0,0]) cube([85,56,0.1], center=true);
} 

module volhouse () {  /* voltage converter*/
	difference(){
		cube([22,27,12],center=true);
		cube([18,23,12.1],center=true);
	}
}
module mounting(){
	cube([14,12,3],center=true);
}

module col2nd(){
	difference(){
		cube([6,6,12], center=true);
		screw();
	} 
}
module cover(){
	difference() {
		cube([x0,y0,3], center=true);
		rotate([0,0,180]) translate([0,0,-20]) color("blue") screw4();
	}
	y=-20;
	x=16;
	z=4.5;
	translate([x,y,z]) volhouse();
	translate([-x,y,z]) volhouse();
	translate([x+13,y, z]) col2nd();
	translate([-x-13,y, z]) col2nd();
}
//!cover();


module col(){
		cube([8,8,12],center=true);
}
module col4(){
	zz=19;
	translate([x0/2-4, y0/2-15, zz]) col();
	translate([-x0/2+5, y0/2-15, zz]) col();
	translate([x0/2-5, -y0/2+5, zz]) col();
	translate([-x0/2+5, -y0/2+5, zz]) col();

}

module screw() {
	translate([0,0,-10])	cylinder(r=1.6, h=20);
}


module screw4(){
	zz=18;
	translate([x0/2-5, y0/2-15, zz]) screw();
	translate([-x0/2+5, y0/2-15, zz]) screw();
	translate([x0/2-5, -y0/2+5, zz]) screw();
	translate([-x0/2+5, -y0/2+5, zz]) screw();
}

x0=70;
y0=104;
z0=50;


module case(){
	difference(){
		cube([x0, y0, z0], center=true); 
		translate([0,0,4]) cube([x0-4, y0-4, z0+5], center=true); 
		translate([0,y0/2,z0-45.2]) cube([56, 8, 41], center=true);
		translate([0,-40,25]) rotate([90,0,0]) cylinder(r=3,h=30);
	}
	translate([0,-7,-z0/2+1]) rotate([0,0,-90]) mounting_pi();
	difference(){
		col4();
		screw4();
	}
}

module volcover(){
	sx=30;
	sy=20;
	sz=13;
	difference(){
		translate([0, sy,sz]) cube([64,10,3],center=true);
		translate([sx, sy,sz])screw();
		translate([-sx, sy,sz])screw();
	}
}


module motionBoxPos() {
	translate([0,-2/2,0]) 	cube([63.4, 2,40], center=true) ; //backplate
	translate([0,-2/2-4.5,0]) cube([63.4, 2,40], center=true) ;//bbackplate
	translate([0,-25,0]) cube([77.4, 2,40], center=true); //faceplete
	translate([0,-25/2,0])	cube([55.4,25,40], center=true); // outside 
}

module motionBoxNeg() {
	translate([0,-25/2+2.1, 0]) cube([51.4, 21, 31], center=true); // inside 
	translate([14.5,0,0]) rotate([90,0,0]) cylinder(r=1, h=24); // motion sensor mounting screw
	translate([-14.5, 0,0]) rotate([90,0,0]) cylinder(r=1, h=24); // motion sensor mounting screw
	rotate([90,0,0]) cylinder(r=4.5, h=30); // motion sensor proper
}

module motionBoardBox(){
	difference() {
		motionBoxPos();
		motionBoxNeg();
	}
}

case();
translate([0,47.7,5]) rotate([0,0,180] ) motionBoardBox();
translate([0,0,25]) rotate([0,180,180]) cover();
color("yellow") volcover();

