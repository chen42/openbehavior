$fn=50;

module screw(){
	translate([-30,0,0])rotate([0,90,0]) cylinder(r=1.50, h=35,center=true);
}

module screwset(){
	dist=31;
  	translate([0,dist,dist])screw();
    translate([0,-dist,dist])screw();
	translate([0,dist,0])screw();
	translate([0,-dist,0])screw();
  	translate([0,-dist,-dist])screw();
  	translate([0,dist,-dist])screw();

}


dia=23; // of the antenna

module antenna_cover(){
	difference(){
		union(){
			cylinder(r=dia+4,h=6,center=true);
			cube([6,dia*2+22,6],center=true);
		}
		translate([0,0,-1])cylinder(r=dia+2,h=5,center=true);
		cylinder(r=dia-2,h=7,center=true);
		translate([0,0,30])rotate([0,-90,0])screwset();
        translate([5,0,-2])cube([2,80,2],center=true);
	}
}

module rfid_board_hook(){
	distance=25;
    stickout=36;
    x=23;
	translate([x,stickout,distance]) cube([3,4,4],center=true);
	translate([x,stickout,-distance]) cube([3,4,4],center=true);
	translate([x,-stickout,distance]) cube([3,4,5],center=true);
	translate([x,-stickout,-distance]) cube([3,4,5],center=true);
}


module cboard_cover(){
	translate([5,0,0])difference(){
		union(){
			translate([15,43,0])cube([30,12,63],center=true);
			translate([15,37,0])cube([30,3,70],center=true);
		}
		translate([15,40,0])cube([26,10,58],center=true);
		translate([18,38,0])cube([26,7,10],center=true);
		translate([15,34.5,0])cboard_screw(dia=2);
	}
}

module spoutholder(){
    rfid_board_hook();
	difference(){
        union(){
            cube([70,70,70],center=true); //outside
            translate([17.2,0,29])rotate([0,35,0])cube([22,30,30],center=true); // plate for spout
        }
		translate([-14,0,0])screwset();
		translate([-14,0,0])rotate([0,90,0])cylinder(r=dia-3,h=35,center=true);//rfid ring
		translate([-20,0,0])cube([55,60,56],center=true); //front chamber
		translate([25.1,0,-15])cube([20,50,80],center=true); //back chamber
		translate([-30,0,0])cube([10,80,56],center=true);//side slot
		translate([-15,11,-29])rotate([4,0,0])cube([45,27,6.2],center=true);//bottom
		translate([-15,-11,-29])rotate([-4,0,0])cube([45,27,6.2],center=true);//bottom
        translate([-14,0,5])rotate([0,0,90])union(){  // spout assembly
		translate([0,-10,3]) rotate([0,90,0]) cylinder(r=3, h=75,center=true); //holes for alignment of the spout tip 			
		translate([0,-10,0]) rotate([35,0,0]) cylinder(r=4.6, h=55); // location of the spout 
		translate([0,-47,31]) rotate([-55, 0,0]) cube([8.4, 18, 4.1], center=true);// hex screw for spout 
		translate([0,-65,14]) rotate([-55,0,0]) cylinder(r=1.9, h=50); //screw hole for tightening the spout 
		translate([0,-10,-60]) cylinder(r=5, h=40); //hole for collection tube //yes
		}
		translate([20,35,0])cboard_screw();
		translate([0,0,30])cylinder(r=2.8,h=20,center=true);//cue light
		translate([-8,0,30])cylinder(r=2.8,h=20,center=true);//cue light
	}
}

module cboard_screw(dia=1.5){
	distance=32;
	translate([0,0,distance])rotate([90,0,0]) cylinder(r=dia, h=350,center=true);
	translate([0,0,-distance])rotate([90,0,0]) cylinder(r=dia, h=350,center=true);
	translate([0,19,-distance])rotate([90,0,0]) cylinder(r=dia+3, h=30,center=true); // screw head
	translate([0,19,distance])rotate([90,0,0]) cylinder(r=dia+3, h=30,center=true); // screw head
}

module frontpanel(){
    difference(){
        union(){
            cube([82,77,2],center=true);
            translate([0,0,2])cube([82,69,3],center=true);
            translate([0,0,5])cylinder(r=dia-1,h=5,center=true);
        }
  		//translate([0,0,4])cylinder(r=dia-3,h=14,center=true);
    	scale([.8,.95,1])translate([-5,0,4])cylinder(r=dia-3,h=14,center=true,$fn=100);
        translate([0,0,-20])rotate([0,90,0])screwset();
    }
}


//translate([-40,0,0])rotate([0,90,0])frontpanel();
//translate([-35,0,0])rotate([0,90,0])antenna_cover();
spoutholder();
//color("blue")cboard_cover();

