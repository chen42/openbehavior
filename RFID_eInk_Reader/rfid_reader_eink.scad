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
	color("grey")cube([70, 93, 3], center=true); // base board
} 
module sidewall(){ // include the top cover mounting holes
	color("blue") cube([2,93,25], center=true);
	translate([3, 43,10]) difference( ) { cylinder(r=3.5, h=5, center=true); cylinder(r=1.6, h=43);}
	translate([3,-43,10]) difference( ) { cylinder(r=3.5, h=5, center=true); cylinder(r=1.6, h=43);}
}


module topCoverMounting() {
	mx=31;
	my=-30.5;
	my2=50.5;
	color("blue") translate([mx,my,0])  cylinder(r=1.9,h=40);
	color("blue") translate([-mx,my,0]) cylinder(r=1.9,h=40);
	color("blue") translate([-mx,my2,0])cylinder(r=1.9,h=40);
	color("blue") translate([mx,my2,0]) cylinder(r=1.9,h=40);
} 

module topCover(){
	difference(){
		color("green")translate([0,10,28]) cube([70, 90, 3], center=true);
		topCoverMounting();
	}
}

module case(){
	union(){
			difference() {
				union(){
					rotate([0,0,-90]) translate([0,0,1])mounting_pi(); // pi  // rpi
					translate([0,11.5,1]) baseboard();
					bx=34;
					by=11.5;
					translate([bx,by,13]) rotate([0,0,180]) sidewall();
					translate([-bx,by,13]) sidewall(); 
				} 
				translate([30,-30, 4]) cube([10, 15, 9]); // power plug 
			}
			difference(){ // short end
				translate([0,-34,13]) cube([70,2,25], center=true);// backwall
				translate([0,-34,4]) cube([20,10, 6], center=true); // sdcard slot  
			}
			difference(){ // USB end
				translate([0,57,13]) cube([70,2,25], center=true);// backwall
				translate([-10,56,18]) cube([35,20,25], center=true); // USB  
			}
	
	}

}
case();
//topCover();


