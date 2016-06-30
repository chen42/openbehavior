// this boot further increases the height of the plus maze so that it can be placed in the openfield and not worry about the open arm is close to the wall of the open field.

$fn=100;

module hollow(w1, w2,h){
	difference(){
		cube([w1, w1, h], center=true);
		cube([w2, w2, h], center=true);
	}

}


module space(w, h){
	w1=10;
	gap=20;
	for (i = [1:6]) {
		translate([gap*i,0,0]) cube([w1,w,h]);
	}
}


difference(){
	hollow(152,142,100);
	translate([0,0,50]) cube([142, 142, 20], center=true);
	difference(){
		cylinder (r=110, h=100, center=true);
		cylinder(r=104, h=100,center=true, $fs=0.2);
	}
	// reduce the printing time 
	translate([-75, 140/2,  -40]) space(10,80);
	rotate([0,0,90])translate([-75, 140/2,  -40]) space(10,80);
	rotate([0,0,180])translate([-75, 140/2,  -40]) space(10,80);
	rotate([0,0,270])translate([-75, 140/2,  -40]) space(10,80);
    translate([0,0,-50])rotate([90,0,90]) scale([1,0.1,1]) cylinder(r=55, h=160, center=true);
    translate([0,0,-50])rotate([90,0,180])scale([1,0.1,1]) cylinder(r=55, h=160, center=true);

}

difference(){
	translate([0,0,-3.2]) rotate([0,0,45]) hollow(107,100,100-6.4); 
	// further reduce print time
    translate([0,0,-50])rotate([90,0,45]) cylinder(r=45, h=120, center=true);
    translate([0,0,-50])rotate([90,0,135]) cylinder(r=45, h=120, center=true);
}

