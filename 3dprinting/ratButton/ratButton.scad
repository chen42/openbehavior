$fn=60;

module button(){
	difference() {
		//cylinder(r=10, h=.6) ; // medium thickness
        cylinder(r=10, h=.4) ; // think thickness
		//	#translate([0,0,0]) cylinder(r1=8, r2=7,  h=0.5) ; // base
		 
			
        for (a=[1:8]){
           rotate([0,0,a*45])translate([5,5,0]) #cylinder(r=1, h=2, center=true); //  hole 
   
		}
	}
}



module groove(){	
	z=1;
	w=1.2;
	cube([80,w,z], center=true);
    for (a=[1:3]){
        translate([0,-a*3,0]) cube([80,w,z], center=true);
        translate([0,a*3,0]) cube([80,w,z], center=true);
    } 
}


module base(){
	difference() {
		union(){
			cylinder(r=10, h=1) ; // base
			translate([0,0,1]) cylinder(r1=10, r2=7,  h=0.5) ; // base
		} 
		translate([0,0,0])
		union(){
			cylinder(r1=3, r2=0.68, h=1); //bottom cone
			scale([0.5,1,0.5]) rotate([0,0,45]) cube([20,16,0.7]);
			groove();
			rotate([0,0,90]) translate([0,0,1.5]) groove();
            x=4.5;
            y=4.5;
            r=1;
            for (a=[0:8]){
           		rotate([0,0,45*a])translate([x,-y,0]) cylinder(r=1.5, h=12, center=true); //  hole 
                rotate([0,0,45*a])translate([-x,y,0]) cylinder(r=1.5, h=12, center=true); //  hole 
            }
		}
	}

}

difference(){
	union(){
		//scale([1,1,1])        
        base();        
		translate([0,0,0.3])cylinder(r=2.8, h=12) ; // stem above the base		
        //#translate([0,0,0.5])cylinder(r2=4, r1=6.1, h=1) ; // Qin's suggestion
   		translate([0,0,6])cylinder(r=5, h=9); // top above the base
        translate([0,0,4])cylinder(r2=5, r1=3, h=2); // top above the base

	}
    translate([0,0,8])cylinder(r=1.55, r2=1.65, h=7); // spring connector, i.e. center cone

	cylinder(r=0.66, h=30, center=true); // center hole 	
}
