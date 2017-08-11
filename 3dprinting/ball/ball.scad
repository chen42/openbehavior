$fn=40;
$fn=13;
module bar(){
	difference(){
	cylinder(r1=14, r2=8, h=106, center=true);
	cylinder(r1=12, r2=6, h=104, center=true);
	}
}

difference (){
	radius=50;
	union(){
		sphere(r=radius);
		bar();
		rotate([90,0,0]) bar();
		rotate([0,90,0]) bar();
	}
	sphere(r=radius-2);
}

