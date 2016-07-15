$fn=100;

module LEDBoxPos() {
	translate([0,-2/2,0]) 	cube([63.4, 2,40], center=true) ; //backplate
	translate([0,-2/2-4.5,0]) cube([63.4, 2,40], center=true) ;//bbackplate
	translate([0,-25,0]) cube([77.4, 2,40], center=true); //faceplete
	translate([0,-25/2,0])	cube([55.4,25,40], center=true); // outside 
}
module LEDBoxNeg() {
	translate([0,-25/2+2, 0]) cube([52, 26, 35.5], center=true); // inside 
}

module drillholes() {//all four screw holes for LED board
	translate([4,3,0]) hollow();
	translate([44,3,0]) hollow();
	translate([4,26,0]) hollow();
	translate([44,26,0]) hollow();
}

module hollow() { //the screw holes
	cylinder(9.1,1.5,1.5);
} 

module cols4LED(){ //all four inside columns 
    translate([4,3,2.23]) column();
    translate([44,3,2.23]) column();
    translate([4,26,2.23]) column();
    translate([44,26,2.23]) column();
}

module column(){
	cylinder(2.5,4,4);
} //the inside column

module led() { // hole for the LED lights
	cube([22,10,6],center=true);
}


module CueLightBox() {
	difference() {
		LEDBoxPos();
		difference() {
			LEDBoxNeg(); 
			rotate([90,0,0]) translate([-24,-15,20]) cols4LED();
		}
		rotate([90,0,0]) translate([-24,-15,14]) drillholes();
		translate([0,-25,12.5]) led();
	}
}

module CueLightPanel() {
		difference(){
			union(){
				translate([0,-25,0]) cube([77.4, 2,40], center=true); //faceplete
				rotate([90,0,0]) translate([-24,-15,20]) cols4LED();
			}
		rotate([90,0,0]) translate([-24,-15,14]) drillholes();
		translate([0,-25,12.5]) led();
	}
}
translate([0,48,1]) rotate([0,0,180] ) CueLightBox();
//translate([0,48,1]) rotate([0,0,180] ) CueLightPanel();

