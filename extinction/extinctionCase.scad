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
	translate([0,0, 13.1]) cube([70, 25, 8.4], center=true);
	//translate([0,0, 13.1-3.7]) cube([80.6, 36, 0.1], center=true); // base plate
}


module cover(){
	difference() {
		union(){
			cube([x0,y0,3], center=true);
			translate([14,2,0])rotate([0,0,90]) lcd_mounting();
		}
		rotate([0,0,180]) translate([0,0,-20]) color("blue") screw4();
		translate([13,2,15]) rotate([0,180,90])lcd();
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
		translate([0,-40,21]) rotate([90,0,0]) cylinder(r=3,h=30); // power cords
		translate([-4,-53,-z0/2+5]) cube([20,10, 5], center=true); // sdcard slot  
		translate([-25,-44,16]) rotate([90,0,0]) cylinder (r=1.5, h=20); // touch sensor
		translate([3,-44,16]) rotate([90,0,0]) cylinder (r=1.5, h=20); // touch sensor
		translate([30,21,8]) cube ([10,10,13]); // potential meter for lcd
	}
	translate([-4,-17,-z0/2+1]) rotate([0, 0, -90]) mounting_pi();
	translate([-25,-47,16]) rotate([90,0,0]) mounting_touch();
	difference(){
		col4();
		screw4();
	}
}

module motionBoxPos() {
	translate([0,-2/2,0]) 	cube([63.4, 2,40], center=true) ; //backplate
	translate([0,-2/2-4.5,0]) cube([63.4, 2,40], center=true) ;//bbackplate
	translate([0,-25,0]) cube([77.4, 2,40], center=true); //faceplete
	translate([0,-25/2,0])	cube([55.4,25,40], center=true); // outside 
}

module motionBoxNeg() {
	translate([0,-25/2+2, 0]) cube([51.4, 26, 31], center=true); // inside 
	translate([14.5,0,0]) rotate([90,0,0]) cylinder(r=1, h=25); // motion sensor mounting screw
	translate([-14.5, 0,0]) rotate([90,0,0]) cylinder(r=1, h=25); // motion sensor mounting screw
	rotate([90,0,0]) cylinder(r=4.5, h=30); // motion sensor proper
	translate([0,-25,0])rotate([90,0,0]) cylinder(r1=4.5, r2=14,h=3); // motion sensor proper
}

module motionBoardBox(){
	difference() {
		motionBoxPos();
		motionBoxNeg();
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
//translate([0,48,1]) rotate([0,0,180] ) motionBoardBox();
translate([0,0,25]) rotate([0,180,180]) cover();
//translate([-50,0,50]) rotate([90,0,270]) frontCover();
