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



module baseboard(){
	difference(){
		color("grey")cube([70, 90, 4], center=true); // base board
	}
} 
module sidewall(){
	color("blue") cube([2,90,26], center=true);
	translate([3, 40.5,6]) difference( ) { cube([7,7,14], center=true); cylinder(r=1.6, h=43);}
	translate([3,-40.5,6]) difference( ) { cube([7,7,14], center=true); cylinder(r=1.6, h=43);}
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

module case(){
	union(){
			difference() {
				union(){
					rotate([0,0,-90])mounting_pi(); // pi  // rpi
					translate([0,10,-2]) baseboard();
					bx=34;
					by=10;
					translate([bx,by,13]) rotate([0,0,180]) sidewall();
					translate([-bx,by,13]) sidewall(); 
				} 
				translate([30,-32, 2]) cube([10, 15, 10]); 
			}
			difference(){ // short end
				translate([0,-34,13]) cube([70,2,26], center=true);// backwall
				translate([0,-34,1]) cube([28,10, 5], center=true); // sdcard slot  
			}
			difference(){ // USB end
				translate([0,54,13]) cube([70,2,26], center=true);// backwall
				translate([0,54,1]) cube([50,20,25], center=true); // USB  
			}
	
	}

}
case();
//topCover();


