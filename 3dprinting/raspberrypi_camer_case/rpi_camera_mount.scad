// original design by devzero, published Oct 19, 2013
// https://www.thingiverse.com/thing:168581
// modified by Hao Chen Oct 11 2017

board_width=25.5;
board_height=23;
board_thick=4.75;
cable_width=18;
cable_thick=1;
side_cover=7.5;
camera_hole_width=10;
camera_hole_height=5.5;
screw_hole_r=2.65;
padding=2.5;
d=0.001;
mount_offset=2*padding+board_width;
mount_thickness=8;


//camera holder
difference(){
	cube([board_thick+2*padding, board_width+2*padding, board_height+2*padding]);
	//main compartment
	translate([padding, padding, padding]) cube([board_thick, board_width, board_height+padding+d]);
	//front camera slot
	translate([board_thick+padding-d, padding+side_cover, padding+camera_hole_height]) cube([padding+2*d, camera_hole_width, board_height+padding-camera_hole_height+d]);
	//hole for cable in the bottom
	translate([padding+2,padding+(board_width-cable_width)/2,0]) cube([cable_thick, cable_width+2*d, padding+2*d]);
}

//handle

translate([7.8,10,-40])cube([2,10, 40]);

