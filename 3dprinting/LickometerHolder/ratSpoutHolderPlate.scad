$fn=100;
difference(){

cube([77,82,1.8]); // plate per se
translate([13,21,-1]) cube([50,50,3]); // open in the middle
translate([77/2,10,-1]) cylinder(r1=1.8, r2=3, h=3); // screw
translate([8.5,42.5,-1]) cylinder(r1=1.8, r2=3, h=3); // screw
translate([68.5,42.5,-1]) cylinder(r1=1.8, r2=3,h=3); // screw

}



