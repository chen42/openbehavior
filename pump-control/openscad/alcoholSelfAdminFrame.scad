// frame for home cage alcohol self-administration. 
// Hao Chen
// UTHSC
 
$fn=100;
max_w=210;
max_h=138;
max_d=90;

pw=40;// spout holder width x 
ph=45;// spout holder length y
pg=60;// spout holder height z
r=10; // forgot what this is for??
fv=0.1; // for better visualization



module corner(ln=20, wd=30 ){ // a negative part for making a round corner 
	difference (){
		cube([wd,wd,ln]);
		translate([0,0,0])
		cylinder(r=wd, h=ln);
	}
}

module outbox(){ // outside box for the frame
	corner_wd=10;
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

module mounting_m25(innR=1.9){ // screw 
	difference(){
		cylinder(r=3.8, h=10);
		cylinder(r=innR, h=10);
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




module top_groove(){ // for the top cover
	difference(){
		translate([0,0,max_h/2-4])
		cube([204, 79, 10], center=true);
		translate([0,0,max_h/2-4])
		cube([204-8, 79-8,11], center=true);
	}
}

module round_corner_box( r0=10, wd=20, ht=30, lg=40) { // generic 
	hull(){
	translate([wd/2,lg/2,0])
	cylinder(r=r0, h=ht);
	translate([wd/2,-lg/2,0]) cylinder(r=r0, h=ht);
	translate([-wd/2,-lg/2,0]) cylinder(r=r0,h=ht);
	translate([-wd/2,lg/2,0]) cylinder(r=r0, h=ht);
	}
}

module motion_sensor (){
	translate([-14,0,5])
	cylinder(r=1, h=7);
	translate([14,0,5])
	cylinder(r=1,h=7);
	cylinder(r=4.5, h=20);
	cylinder(r1=20,r2=4.5, h=6);
}
module spout_holder_inner (sh_x=70, sh_y=40){
			translate([-sh_x,-sh_y+10,15]) rotate([90,0,0]) round_corner_box(r0=3,wd=pw-6, ht=ph+5,lg=pg-16); // spout holder inside
}

module spout_holder(sh_x=70, sh_y=40, sh_z=20){
	//sh_x: spout holder x
	//sh_y: spout holder y
	//sh_z: spout holder z
	difference(){
		union(){
			translate([-sh_x,-sh_y,sh_z]) rotate([90,0,0]) round_corner_box(r0=3,wd=pw, ht=ph,lg=pg); //spout holder outside
			translate([-sh_x,-sh_y,-pg/2-6]) rotate([90,0,0]) round_corner_box(r0=2,ht=5,wd=13,lg=8); //positive for attachment screw, bottom 
			translate([-sh_x,-sh_y,pg/2+6]) rotate([90,0,0]) round_corner_box(r0=2,ht=5,wd=13,lg=8); //positive for attachment screw, top
		}
		union(){
			translate([-sh_x,-sh_y+10,sh_z-5]) rotate([90,0,0]) round_corner_box(r0=3,wd=pw-6, ht=ph+5,lg=pg-16); // spout holder inside
			translate([-sh_x-30,-sh_y-10,sh_z]) rotate([0,90,0]) cylinder(r=2.5, h=55); //holes for alignment of the spout tip 
			translate([-sh_x,-sh_y,sh_z]) rotate([90,0,0]) cylinder(r=12, h=55); //holes for obverving the rat 
			translate([-sh_x,-sh_y-10,sh_z]) rotate([35,0,0]) cylinder(r=4.6, h=55); // location of the spout 
			translate([-sh_x,-sh_y-42, sh_z+31]) rotate([-55, 0,0]) cube([8.4, 18, 4.1], center=true);// hex screw for spout 
			translate([-sh_x,-sh_y-60,sh_z+14]) rotate([-55,0,0]) cylinder(r=1.9, h=50); //screw hole for tightening the spout 
			translate([-sh_x,-sh_y-10,-pg/2-7]) rotate([-90,0,0]) cylinder(r=1.9, h=25); //negative for attachment screw, top
			translate([-sh_x,-sh_y-10,pg/2+7]) rotate([-90,0,0]) cylinder(r=1.9, h=25); //negative for attachment screw, top
		}
	}
}




module the_thing (){
	union(){
		difference(){
				pw=40;// spout holder width x 
				ph=40;// spout holder length y
				pg=50;// spout holder height z
				sh_x=70;// spout holder box x
			union(){
				frame();
		//		translate([-1*sh_x,-40,20]) rotate([90,0,0]) round_corner_box(r0=3,wd=pw, ht=ph,lg=pg); //spout holder
		//		translate([sh_x,-40,20]) rotate([90,0,0]) round_corner_box(r0=3,wd=pw, ht=ph,lg=pg);
			}
			union(){
				top_groove();
				rotate([90,0,0]) translate([0,0,34]) 	motion_sensor();
				translate([-max_w/2,0,65]) rotate([0,90,0]) cylinder(r=1.9, h=10); //screw hole for the top cover on the side;
				translate([max_w/2-10,0,65]) rotate([0,90,0]) cylinder(r=1.9, h=10); //screw hole for the top cover on the side; 
				spout_holder_inner(sh_x=-70);
				spout_holder_inner(sh_x=70);
				spout_holder(sh_x=70, sh_y=44);
				spout_holder(sh_x=-70, sh_y=44);


			}
		}
		mounting_screws();
	}
}



spout_holder(sh_x=0,sh_y=0, sh_z=0)

//the_thing()

difference(){
cube([20,26,20],center=true);
translate([0,0,-10]) rotate([-55, 0,0]) cube([8.5, 18, 4.2], center=true);// hex screw for spout 
 }


// use r=1.7 for m5 screw
