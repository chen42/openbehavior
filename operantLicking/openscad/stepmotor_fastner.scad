$fn=40;
module step_motor_fastener (){
	difference(){
		cube([13, 9, 3],center=true);
		translate([4,0,-3]) cylinder(r=1.7, h=8);
	}
}

step_motor_fastener() ;

