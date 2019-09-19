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
				translate([w/2,   l/2,0])cylinder(r=3.6, h=10);
				translate([w/2,  -l/2,0])cylinder(r=3.6, h=10);
				translate([-w/2, -l/2,0])cylinder(r=3.6, h=10);
				translate([-w/2,  l/2,0])cylinder(r=3.6, h=10);
			
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
		color("grey") translate([0,-96,-3]) cube([90, 120, 4], center=true); // base board
#		translate([-39,-105,-2])cube([3.0, 11.5,5], center=true); // rfid board connection via the pins; 
//		translate([0,-150,0]) cube([40,20,5], center=true); // rfid antenna groove;
	}
} 
module sidewall(){
	color("blue") cube([2,100,30], center=true);
	translate([3,46.5,8]) difference( ) { cube([7,7,14], center=true); cylinder(r=1.9, h=43);}
	translate([3,-46.5,8]) difference( ) { cube([7,7,14], center=true); cylinder(r=1.9, h=43);}
}


module topCoverMounting() {
	mx=41;
	my=-73.3;
	my2=-166.6;
	color("blue") translate([mx,my,0])  cylinder(r=1.8,h=40);
	color("blue") translate([-mx,my,0]) cylinder(r=1.8,h=40);
	color("blue") translate([-mx,my2,0])cylinder(r=1.8,h=40);
	color("blue") translate([mx,my2,0]) cylinder(r=1.8,h=40);
} 

module topCover(){
	difference(){
		translate([0,-120,30]) cube([90, 104, 3], center=true);
		topCoverMounting();
	}
}


module rfid_antenna_housing(){
	difference(){
		cube([50,43,7], center=true); // rfid antenna outside;
#		translate([0,4,0]) cube([48,40,3], center=true); // rfid antenna groove;
   //     color("green") translate([12,2,0]) cube([30,37,3.2], center=true); // rfid antenna groove, expand for wires
		cube([41,29,30], center=true); //rfid antenna loop inside  
	}
}
       


module case(){
	union(){
			difference() {
				union(){
					translate([8,-143+8,-1.0]) rotate([0,0,-90]) mounting_pi(); // pi  // rpi
					bx=44;
					by=-120;
					translate([0,-33,0]) baseboard();
					translate([bx,by,13]) rotate([0,0,180]) sidewall();
					translate([-bx,by,13]) sidewall(); 
					translate([0,-214,-1.5]) rotate([0,0,90]) rfid_antenna_housing();
				} 
				translate([37,-170, 2]) cube([10, 50, 15]); 
			}
			difference(){
				translate([0,-171,13]) cube([90,2,30], center=true);// backwall
				translate([15,-170,3]) cube([28,10, 5], center=true); // sdcard slot  
				translate([-35,-170, 4]) rotate([90,0,0]) cylinder(r=5, h=20); //rfid antenna wire
			}
	}
}
//case();
topCover();


