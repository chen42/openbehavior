$fn=50;


module inside_ear(){
	scale([1,1,0.7])
	difference(){
		sphere(r=4.5);
		sphere(r=3.5);
		cylinder(h=100,r=1.3, center=true);
		translate([0,0,-5]) cube([9,9,9], center=true);
	} 
}

module back_of_ear(){
	difference(){
		union(){
		scale([1,1,.8])sphere(r=4.5);
		translate([0,0,4])cylinder(r=2.2,h=4, center=true);
		}
		sphere(r=3.5);
		cylinder(h=100,r=1.2, center=true);
		translate([0,0,-5]) cube([9,9,9], center=true);
	}
} 


//back_of_ear();
inside_ear();
