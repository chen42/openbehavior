// this boot further increases the height of the plus maze so that it can be placed in the openfield and not worry about the open arm is close to the wall of the open field.

$fn=1000;

module hollow(w1, w2,h){
	difference(){
		cube([w1, w1, h], center=true);
		cube([w2, w2, h], center=true);
	}

}


difference(){
	hollow(152,142,100);
	translate([0,0,50]) cube([142, 142, 20], center=true);
	difference(){
		cylinder (r=110, h=100, center=true);
		cylinder(r=104, h=100,center=true, $fs=0.2);
	}
}
translate([0,0,-3.2]) rotate([0,0,45]) hollow(107,100,100-6.4); 

