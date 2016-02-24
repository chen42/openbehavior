// frame for home cage alcohol self-administration. 
// Hao Chen
// UTHSC
 

max_w=210;
max_h=138;
max_d=90;
r=10;
fv=0.1; // for better visualization


module corner(ln=20, wd=30 ){ // a negative part for making a round corner 
	difference (){
		cube([wd,wd,ln]);
		translate([0,0,0])
		cylinder(r1=wd, r2=wd, h=ln);
	}
}

module outbox(){ // outside box for the frame
	corner_wd=20;
	corner_ln=max_d;
	difference(){
		cube([max_w-fv,max_d-fv,max_h-fv],center=true);
		union(){
			translate([max_w/2-corner_wd, max_d/2, -max_h/2+corner_wd]) rotate([90,90,0]) corner(ln=corner_ln, wd=corner_wd);
			translate([-max_w/2+corner_wd, max_d/2, -max_h/2+corner_wd]) rotate([90,180,0]) corner(ln=corner_ln, wd=corner_wd);
		}
	}
}

module innerbox(){ // inside box for the frame
	inn_w=max_w-10;
	inn_h=max_h-20;
	inn_d=max_d-7;
	corner_wd=20;
	corner_ln=max_d;
	difference(){
		cube([inn_w-fv,inn_d-fv,inn_h-fv],center=true);
		union(){
			translate([inn_w/2-corner_wd, inn_d/2, -inn_h/2+corner_wd]) rotate([90,90,0]) corner(ln=corner_ln, wd=corner_wd);
			translate([-inn_w/2+corner_wd, inn_d/2, -inn_h/2+corner_wd]) rotate([90,180,0]) corner(ln=corner_ln, wd=corner_wd);
		}
	}
}

module frame(){
	difference () {
		outbox();
		translate([0,7,-max_h/2]) cube([max_w-20,max_d-7,max_h/2], center=true);
		translate([0,7,-8]) innerbox();
	}
}

module mounting_m25(innR=1.9){  // screw 
	difference(){
		cylinder(r1=3.8, r2=3.8, h=10);
		cylinder(r1=innR, r2=innR, h=10);
	}
}

module mounting_pi(){
	mounting_m25();
	translate([58,0,0]) mounting_m25();
	translate([0,49,0]) mounting_m25();
	translate([58,49,0]) mounting_m25();
} 

module mounting_touch(){
	mounting_m25(innR=1.5);
	translate([28,0,0]) mounting_m25(innR=1.5);
} 

module mounting_RTC(){
	mounting_m25();
	translate([22.5,0,0]) mounting_m25();
}

module mounting_screws(){
	translate([-94,-31.5, max_h/2-2]) mounting_pi();
//	#translate([-97.5,-35.0, max_h/2-2]) cube([85, 56,2]);//the pi
	translate([4,-21.5, max_h/2-2]) mounting_touch();
	translate([40,25, max_h/2-2]) mounting_RTC();
}




module top_groove(){  // for the top cover
	difference(){
		translate([0,0,max_h/2-4])
		cube([204, 79, 10], center=true);
		translate([0,0,max_h/2-4])
		cube([204-8, 79-8,11], center=true);
	}
}

module round_corner_box( r0=10, wd=20, ht=30, lg=40) {  // generic 
	hull(){
	translate([wd/2,lg/2,0])
	cylinder(r1=r0, r2=r0, h=ht);
	translate([wd/2,-lg/2,0]) cylinder(r1=r0, r2=r0,h=ht);
	translate([-wd/2,-lg/2,0]) cylinder(r1=r0, r2=r0,h=ht);
	translate([-wd/2,lg/2,0]) cylinder(r1=r0, r2=r0,h=ht);
	}
}

module motion_sensor (){
	translate([-14,0,5])
	cylinder(r1=1,r2=1,h=7);
	translate([14,0,5])
	cylinder(r1=1,r2=1,h=7);
	cylinder(r1=4.5,r2=4.5, h=20);
	cylinder(r1=20,r2=4.5, h=6);
}

difference(){
		pw=40;// spout holder width x 
 		ph=40;// spout holder length y
		pg=60;// spout holder height z
		sh_x=70;// spout holder box x

	union(){
		frame();
		translate([-1*sh_x,-40,20]) rotate([90,0,0]) round_corner_box(r0=3,wd=pw, ht=ph,lg=pg); //spout holder
		translate([sh_x,-40,20]) rotate([90,0,0]) round_corner_box(r0=3,wd=pw, ht=ph,lg=pg);
	}
	union(){
		top_groove();
		rotate([90,0,0]) translate([0,0,34]) 	motion_sensor();
		translate([-max_w/2,0,65]) rotate([0,90,0])  cylinder(r1=1.9, r2=1.9, h=10); //screw hole for the top cover on the side;
		translate([max_w/2-10,0,65]) rotate([0,90,0])  cylinder(r1=1.9, r2=1.9, h=10); //screw hole for the top cover on the side; 
		translate([70,-30,20]) rotate([90,0,0]) round_corner_box(r0=3,wd=pw-6, ht=ph*1.4,lg=pg-6); // spout holder 
		translate([-70,-30,20]) rotate([90,0,0]) round_corner_box(r0=3,wd=pw-6, ht=ph*1.4,lg=pg-6); // spout holder
	}
}
mounting_screws();


sh_x=70;
		pw=40;// spout holder
#		translate([-100,-80,30]) rotate([0,90,0])  cylinder(r1=1.9, r2=1.9, h=55); //screw hole for the top cover on the side; 
#		translate([-1*sh_x,-60,30]) rotate([45,00,0])  cylinder(r1=4.6, r2=4.6, h=55); //screw hole for the top cover on the side; 
translate([-1*sh_x, -60, 30]) round_corner_box(r0=3, wd=pw-7, ht=15, lg=5);


// hex hole 14 x 8.4 x 4.1
// r=1.8 for screw to for wire
