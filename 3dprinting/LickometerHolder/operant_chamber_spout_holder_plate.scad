difference(){
cube([77,88,2]);
translate([13.5,10,-1])cube([50,50,4]);
translate([38.5,72, 0]) screw();
translate([8.5, 40,0]) screw();
translate([68.5,40,0]) screw();
}


module screw(){
cylinder(r1=3.8, r2=2, h=2);
}
