$fn=100;

module mounting_m25(innR=1.6, h=10){ // screw 
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


module mounting(){
	cube([14,12,3],center=true);
}

module col2nd(){
	difference(){
		cube([6,6,12], center=true);
		screw();
	} 
}

module cover(){
	difference() {
		cube([x0,y0,3], center=true);
		rotate([0,0,180]) translate([0,0,-20]) color("blue") screw4();
	}
	y=-20;
	x=16;
	z=4.5;
	translate([x,y,z]) volhouse();
	translate([-x,y,z]) volhouse();
	translate([x+13,y, z]) col2nd();
	translate([-x-13,y, z]) col2nd();
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
		translate([-4,-53,-z0/2+10]) cube([20,10, 5], center=true); // sdcard slot  
	}
	translate([-4,-17,-z0/2+1]) rotate([0, 0, -90]) mounting_pi();
	difference(){
		col4();
		screw4();
	}
}

module volcover(){
	sx=29;
	sy=-20;
	sz=10;
	difference(){
		translate([0, sy,sz]) cube([64,8,2],center=true);
		translate([sx, sy,sz])screw();
		translate([-sx, sy,sz])screw();
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

module frontCover (){
	difference() {
		union(){
			translate([-45,-70,-1]) color("pink") cube([2,50,16]);
			translate([45-2,-70,-1]) color("pink") cube([2,50,16]);
			translate([-45,-22,-1]) color("pink") cube([90, 2,16]);
			translate([-45,-70,15])  color("blue") cube([90, 50,2]);
			translate([-45,-70,13]) cube ([90,2,15]);
			translate([-40,-67,6]) cube([6,6,14],center=true); // for screws
			translate([40,-67,6]) cube([6,6,14],center=true); // for screws
		}
		lcd();	
		translate([-27,-69,10]) cylinder(r=5,h=6); // brightness adjust
		screws_frontCover();
	}
}



module lcd(){ // model:  HD44780 
	translate([0,-44, 13.1]) cube([69+1, 24+1, 8.4], center=true);
	translate([0,-44, 13.1-3.7]) cube([80.6, 36, 1], center=true);
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


case();
translate([0,48,1]) rotate([0,0,180] ) motionBoardBox();
//translate([0,0,25]) rotate([0,180,180]) cover();


translate([-50,0,0])rotate([90,0,90]) lcdPanel();

translate([-50,0,50]) rotate([90,0,270]) frontCover();
