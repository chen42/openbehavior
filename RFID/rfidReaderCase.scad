$fn=100;

module mounting_m25(innR=1.6, h=4){ // screw 
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

module rfid_antenna_housing(){
	difference(){
		cube([53,40,10], center=true); // rfid antenna outside;
		translate([0,-6,0]) cube([47,46,5], center=true); // rfid antenna groove;
		cube([36,25,18], center=true); //rfid antenna loop inside  
	}
}

module lcdPanel(){
		w=75;
		l=31;
		difference(){
		union(){
			hull(){
				translate([w/2,   l/2,0])cylinder(r=3.8, h=10);
				translate([w/2,  -l/2,0])cylinder(r=3.8, h=10);
			}
			hull(){
				translate([-w/2, -l/2,0])cylinder(r=3.8, h=10);
				translate([-w/2,  l/2,0])cylinder(r=3.8, h=10);
			}
		}
		union (){
			translate([w/2,   l/2,0])cylinder(r=1.6, h=11);
			translate([w/2,  -l/2,0])cylinder(r=1.6, h=11);
			translate([-w/2, -l/2,0])cylinder(r=1.6, h=11);
			translate([-w/2,  l/2,0])cylinder(r=1.6, h=11);
		}
		}

}

module baseboard(){
	difference(){
		color("grey") translate([-90/2,-215+36,-5]) cube([90, 160, 4]); // base board
		translate([0,-76,0])cube([11.5,3.3,4.5], center=true); // rfid board connection via the pins; 
		translate([0,-6,0]) cube([47,46,5], center=true); // rfid antenna groove;
	}
} 
module sidewall(){
	color("blue") cube([2,100,40], center=true);
	translate([3,48,0]) difference( ) { cube([7,7,40], center=true); cylinder(r=1.9, h=43);}
	translate([3,-48,0]) difference( ) { cube([7,7,40], center=true); cylinder(r=1.9, h=43);}
}


module topCoverMounting() {
	mx=41;
	my=-80;
	my2=-176;
	color("blue") translate([mx,my,0]) cylinder(r=1.8,h=50);
	color("blue") translate([-mx,my,0]) cylinder(r=1.8,h=50);
	color("blue") translate([-mx,my2,0]) cylinder(r=1.8,h=50);
	color("blue") translate([mx,my2,0]) cylinder(r=1.8,h=50);
} 

module topCover(){
	difference(){
		translate([0,-128,40]) cube([90, 104, 3], center=true);
		topCoverMounting();
	}
}


rfid_antenna_housing();
baseboard();
translate([0,-40,-1]) lcdPanel();
translate([0,-143,-1.0]) rotate([0,0,-90]) mounting_pi(); // pi 
bx=44;
by=-128;
translate([bx,by,18]) rotate([0,0,180]) sidewall();
translate([-bx,by,18])sidewall(); 
difference(){
translate([0,-178,18]) cube([90,2,40], center=true);// backwall
translate([0,-178,3]) cube([20,10, 5], center=true);  
}
!topCover();

