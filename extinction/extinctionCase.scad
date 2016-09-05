$fn=100;

module mounting_m25(innR=1.6, h=10){ // screw 
	difference(){
		color("orange") cylinder(r=3.8, h);
		cylinder(r=innR, h=10);
	}
}

module mounting_pi(){
	translate([-58/2,-49/2,0]) mounting_m25(h=5);
	translate([58/2,-49/2,0]) mounting_m25(h=5);
	translate([-58/2,49/2,0]) mounting_m25(h=5);
	translate([58/2,49/2,0]) mounting_m25(h=5);
	translate([-10,0,0]) cube([85,56,0.1], center=true); // pi
} 


module mounting(){
	cube([14,12,3],center=true);
}

module col2nd(){
	difference(){
		cube([6,6,12], center=true);
		screw();
	} 
}


module lcd(){ // model:  HD44780 
	translate([0,0, 13.1]) cube([71.5, 25, 8.4], center=true);
	//translate([0,0, 13.1-3.7]) cube([80.6, 36, 0.1], center=true); // base plate
}


module cover(){
	difference() {
		union(){
			cube([x0,y0,3], center=true);
			translate([14,2,0])rotate([0,0,90]) lcd_mounting();
		}
		rotate([0,0,180]) translate([0,0,-20]) color("blue") screw4();
#		translate([13,2,15]) rotate([0,180,90])lcd();
	}
}


module col(){
		cube([8,8,12],center=true);
}

module col4(){
	zz=15;
	translate([x0/2-4, y0/2-9, zz]) col();
	translate([-x0/2+5, y0/2-9, zz]) col();
	translate([x0/2-5, -y0/2+5, zz]) col();
	translate([-x0/2+5, -y0/2+5, zz]) col();
}

module screw() {
	translate([0,0,-10])	cylinder(r=1.6, h=20);
}

module screw4(){
	zz=15;
	translate([x0/2-5, y0/2-9, zz]) screw();
	translate([-x0/2+5, y0/2-9, zz]) screw();
	translate([x0/2-5, -y0/2+5, zz]) screw();
	translate([-x0/2+5, -y0/2+5, zz]) screw();
}

x0=76;
y0=104;
z0=42;

module case(){
	difference(){
		cube([x0, y0, z0], center=true); // outside 
		translate([0,0,4]) cube([x0-4, y0-4, z0+5], center=true); // inside 
		translate([0,y0/2,1]) cube([56, 8, 41], center=true);
		translate([0,-40,21]) rotate([90,0,0]) cylinder(r=3,h=30); // cables 
		translate([-4,-53,-z0/2+5]) cube([20,10, 5], center=true); // sdcard slot  
		translate([-25,-44,14]) rotate([90,0,0]) cylinder (r=1.5, h=20); // touch sensor
#		translate([3,-44,14]) rotate([90,0,0]) cylinder (r=1.5, h=20); // touch sensor
		translate([30,21,8]) cube ([10,10,13]); // potential meter for lcd
		translate([30,-45,-16])cube([20,14,8]); //powercord
		translate([-40, -45, -16]) cube([5,2,20]); // peak slit for the Pi LEDs,
		translate([-40, -49, -16]) cube([5,2,20]); // peak slit for the Pi LEDs,
	}
	translate([-4,-17,-z0/2+1]) rotate([0, 0, -90]) mounting_pi();
//	translate([-25,-47,14]) rotate([90,0,0]) mounting_touch();
	difference(){
		col4();
		screw4();
	}
}



module lcd_mounting(){
		w=75;
		l=31;
		difference(){
		union(){
				translate([w/2,   l/2,0])cylinder(r=3.4, h=7);
				translate([w/2,  -l/2,0])cylinder(r=3.4, h=7);
				translate([-w/2, -l/2,0])cylinder(r=3.4, h=7);
				translate([-w/2,  l/2,0])cylinder(r=3.4, h=7);
			
		}
		union (){
			translate([w/2,   l/2,0])cylinder(r=1.2, h=11);
			translate([w/2,  -l/2,0])cylinder(r=1.2, h=11);
			translate([-w/2, -l/2,0])cylinder(r=1.2, h=11);
			translate([-w/2,  l/2,0])cylinder(r=1.2, h=11);
		}
		}

}

module mounting_touch(){
	mounting_m25(innR=1.2, h=4);
	translate([28,0,0]) mounting_m25(innR=1.5, h=4);
} 

//case();
translate([0,0,25]) rotate([0,180,180]) cover();
