$fn=50;

module inside_ear(){
	scale([0.8,0.8,1.1])
	difference(){
		sphere(r=4.5);
		sphere(r=3.7);
		cylinder(h=10,r=1.4, center=true);
	} 
	difference(){
		translate([0,0,-0.5])cylinder(h=0.5, r=3.6,center=false);
		translate([1,0,0])cube([4,8,3], center=true);
	}
}

module back_of_ear(){
	difference(){
		union(){
			scale([1,1,0.9])sphere(r=4.5);
			translate([0,0,4])cylinder(r=3.2,h=3, center=true);
		}
		sphere(r=3.5);
		cylinder(h=13,r=1.4, center=true);
		translate([0,0,5.4]) cube([1.30,7,4], center=true); // top cut
	}
	//}
//	translate([1.2,0,4.7])rotate([90,0,0])difference(){ // notch
//			cylinder(h=1,r=0.8, center=true);
//			translate([0,-1,0]) cube([2,2,4], center=true);
} 


difference(){
	union(){
		back_of_ear();
		translate([12,0,0]) inside_ear();
	}
	translate([0,0,-5]) cube([40,9,9], center=true);
}

