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
	color("blue") cube([2,93,27], center=true);
	translate([3, 43,10]) difference( ) { cylinder(r=3.5, h=5, center=true); cylinder(r=1.6, h=43);}
	translate([3,-43,10]) difference( ) { cylinder(r=3.5, h=5, center=true); cylinder(r=1.6, h=43);}
}


module topCoverMounting() {
	mx=31;
	my=-31.5;
	my2=54.5;
	color("blue") translate([mx,my,0])  cylinder(r=1.9,h=40);
	color("blue") translate([-mx,my,0]) cylinder(r=1.9,h=40);
	color("blue") translate([-mx,my2,0])cylinder(r=1.9,h=40);
	color("blue") translate([mx,my2,0]) cylinder(r=1.9,h=40);
} 

module epaper(){
	translate([-18,-24,0]) cube([40, 60, 30]);
}

module header(){
	translate([-30,-26,25.5]) cube([10,60,2]);
	}

module topCover(){
	difference(){
		color("green")translate([0,11.5,27]) cube([70, 93, 3], center=true);
		topCoverMounting();
		epaper();
		header();
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
				translate([0,-34,13]) cube([70,2,27], center=true);// backwall
				translate([0,-34,4]) cube([20,10, 6], center=true); // sdcard slot  
               translate([-18,-34,6]) rotate([90,0,0]) cylinder(r=3,h=5, center=true); // view port for LEDs

			}
			difference(){ // USB end
				translate([0,57,13]) cube([70,2,27], center=true);// backwall
				translate([-10,56,18]) cube([35,20,25], center=true); // USB  
			}
	}
}

module rfidholder(){
	difference() {
		cube ([74, 80, 17],center=true); //outside
		cube ([66, 130,40],center=true); // middle
		translate([0,0,-2])cube ([70, 100,13],center=true); //inner most
	}
}


//case();

topCover();
//translate([0,10,34])rfidholder();

