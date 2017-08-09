$fn=13;
$fn=40;
module bar(){
	difference(){
	cylinder(r1=14, r2=8, h=106, center=true);
	cylinder(r1=12, r2=6, h=104, center=true);
	}
}

bar();
rotate([90,0,0]) bar();
rotate([0,90,0]) bar();
difference (){
	radius=50;
	sphere(r=radius);
	sphere(r=radius-48);
}

