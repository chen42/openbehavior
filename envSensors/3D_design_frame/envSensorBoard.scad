$fn=20;

translate([-65,-100,0]) base();
pi();
translate([-60,-60,0]) color("red") devboard();
translate([-5,-35,0]) rtc();
translate([7,-70,0]) humidity();
color("green") translate([-26,-70,0]) lux();
color("black") translate([-60,-70,0]) barometer();

module barometer(){
	m25();
	translate([20,0,0]) m25();
}	

module humidity(){
	m25();
	translate([20,0,0]) m25();
}	

module lux(){
	m25();
	translate([20,0,0]) m25();
}	


module devboard() {
	translate([4,4,0]) m25();
    translate([44,4,0]) m25();
   	translate([4,26,0]) m25();
   	translate([44,26,0]) m25();
}

module rtc(){
	m25();
	difference(){
		union(){
			translate([22.5,0,0]) cylinder(r=3.8, h=5);
			translate([24.5,0,0]) cylinder(r=3.8, h=5) ;
		}
		translate([22.5,0,0]) cylinder(r=1.2, h=10);
		translate([24.5,0,0]) cylinder(r=1.2, h=10); 
	}
}


module m25(innR=1.6, h=4){ // screw 
	difference(){
		color("orange") cylinder(r=3.8, h);
		cylinder(r=innR, h=10);
	}
}

module pi(){
	translate([-58/2,-49/2,0]) m25();
	translate([58/2,-49/2,0]) m25();
	translate([-58/2,49/2,0]) m25();
	translate([58/2,49/2,0]) m25();
	translate([-10,0,0]) cube([85,56,0.1], center=true);
} 

module base(){
	%color("grey") cube([100,130,2]);
}


