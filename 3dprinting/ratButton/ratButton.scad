$fn=100;

module groove(){
	x=4;
	y=4;
	translate([-x,y,0]) cylinder(r=1, h=10, center=true); //  hole 
	translate([x,-y,0]) cylinder(r=1, h=10, center=true); //  hole 
	z=1;
	w=1.2;
	cube([80,w,z], center=true);
	translate([0,-3,0]) cube([80,w,z], center=true);
	translate([0,3,0]) cube([80,w,z], center=true);
	translate([0,-6,0]) cube([80,w,z], center=true);
	translate([0,-9, 0]) cube([80,w,z], center=true);
	translate([0,6,0]) cube([80,w,z], center=true);
	translate([0,9, 0]) cube([80,w,z], center=true);
}

module button(){
	difference() {
		union(){
			cylinder(r=1.95, h=18) ; // stem
			cylinder(r=8, h=1) ; // base
			translate([0,0,1]) cylinder(r1=8, r2=7,  h=0.5) ; // base
			cylinder(r=1.4, h=21) ; // spring connector
			translate([0,0,21]) cylinder(r1=1.4, r2=1, h=1.5); // tip 
		} 
		translate([0,0,-0.01])
		union(){
			cylinder(r1=3, r2=0.68, h=1); //bottom cone
			scale([0.5,1,1]) rotate([0,0,45]) cube([20,10,0.7]);
			groove();
			rotate([0,0,90]) translate([0,0,1.4]) groove();
			rotate([0,0,-45])translate([4,4,1]) cylinder(r=1, h=2, center=true); //  hole 
			rotate([0,0,-225])translate([4,4,1]) cylinder(r=1, h=2, center=true); //  hole 
		}
	}

}

module suture(){
	difference(){
	hull(){
	translate([0,2,3.1]) rotate([0,90,0]) cylinder(r0=1,h=2, center=true);
	translate([0,4.5,3.1]) rotate([0,90,0]) cylinder(r0=1,h=2, center=true);
	translate([-1,2,0.7])cube([2,3.4,3], cente=true);
	}
	translate([-3,2,0.7])cube([5,2.3,2.1], cente=true);
	}

}


difference(){
	union(){
		button();
		suture();
		rotate([0,0,180]) suture();
		translate([0,0,1]) cylinder(r=2.5, h=7) ; // larger stem above the base
	}
	cylinder(r=0.68, h=30); // center hole 
}
