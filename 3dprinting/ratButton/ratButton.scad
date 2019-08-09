$fn=60;

module button(){
	difference() {
		cylinder(r=10, h=.6) ; // base
		//	#translate([0,0,0]) cylinder(r1=8, r2=7,  h=0.5) ; // base
		 
			
        for (a=[1:8]){
           rotate([0,0,a*45])translate([5,5,0]) cylinder(r=1, h=2, center=true); //  hole 
   
		}
	}
}




difference(){
	union(){
		//scale([1,1,1])
        button();
		translate([0,0,0.3])cylinder(r=2.8, h=12) ; // stem above the base
   		translate([0,0,6])cylinder(r=5, h=9); // top above the base
        translate([0,0,4])cylinder(r2=5, r1=3, h=2); // top above the base

	}
    translate([0,0,8])cylinder(r=1.55, r2=1.65, h=7); // spring connector, i.e. center cone

	cylinder(r=0.66, h=30, center=true); // center hole 	
}
