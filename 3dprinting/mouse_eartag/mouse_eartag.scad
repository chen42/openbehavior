$fn=60;

difference(){
    cylinder(r=3.9, h=0.8); // top above the base
    cylinder(r=0.62, h=30, center=true); // was .42 center hole 	
}

#difference(){
    cylinder(r=3.9, h=3); 
    cylinder(r=3.1, h=3); 
    translate([-4,1,.5])cube([8,8,4]);
}
