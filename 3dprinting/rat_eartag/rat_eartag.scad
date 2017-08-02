$fn=50;


module inside_ear(){
	difference(){
		sphere(r=4.5);
		sphere(r=3.5);
		cylinder(h=100,r=0.7, center=true);
		translate([0,0,-5]) cube([9,9,9], center=true);
	} 
}

module back_of_ear(){
	difference(){
		union(){
		sphere(r=4.5);
		translate([0,0,4])cylinder(r=2,h=4, center=true);
		}
		sphere(r=3.5);
		cylinder(h=100,r=0.9, center=true);
		translate([0,0,-5]) cube([9,9,9], center=true);
	}
} 


//back_of_ear();
inside_ear();
