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
		color("grey") translate([0,-96,-3]) cube([90, 152, 4], center=true); // base board
		translate([40,-105,-2])cube([3.0, 11.5,5], center=true); // rfid board connection via the pins; 
		translate([0,-6,0]) cube([47,46,5], center=true); // rfid antenna groove;
		screwsV_frontCover();
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
		translate([0,-121,30]) cube([90, 102, 3], center=true);
		topCoverMounting();
	}
}

module lcd(){ // model:  HD44780 
	translate([0,-43, 13.1]) cube([69+1, 24+1, 8.4], center=true);
	translate([0,-43, 13.1-3.7]) cube([80.6, 36, 1], center=true);
}

module screws_frontCover(){
	r0=1.6;
	h0=25;
	// in the  base 
	translate([40,-67,-20]) cylinder(r=r0, h0);
	translate([-40,-67,-20]) cylinder(r=r0, h0);
	// on the side
	h1=10;
	translate([41,-67,20]) rotate([90,0,0])  cylinder(r=r0, h1);
    translate([-41,-67,20]) rotate([90,0,0]) cylinder(r=r0, h1);
} 

module frontCover (){
	difference() {
		union(){
			translate([-45,-70,-1]) color("pink") cube([2,50,15]);
			translate([45-2,-70,-1]) color("pink") cube([2,50,15]);
			translate([-45,-22,-1]) color("pink") cube([90, 2,15]);
			translate([-45,-70,13])  cube([90, 50,3]);
			translate([-45,-70,13]) cube ([90,2,15]);
			#translate([-40,-67,6]) cube([6,6,14],center=true); // for screws
			#translate([40,-67,6]) cube([6,6,14],center=true); // for screws
		}
		lcd();	
		screws_frontCover();
	}

}

union(){
		lcd();	
		difference() {
			union(){
				rfid_antenna_housing();
				translate([0,-43,-1]) lcdPanel();
				translate([-13,-143+8,-1.0]) rotate([0,0,-90]) mounting_pi(); // pi  // rpi
				bx=44;
				by=-120;

				baseboard();
				translate([bx,by,13]) rotate([0,0,180]) sidewall();
				translate([-bx,by,13]) sidewall(); 
			} 
			screws_frontCover();
		}

		difference(){
			translate([0,-171,13]) cube([90,2,30], center=true);// backwall
			translate([-13,-170,3]) cube([20,10, 5], center=true); // sdcard slot  
			translate([35,-170, 28]) rotate([90,0,0]) cylinder(r=2.5, h=20); 
		}

}
topCover();
frontCover();


