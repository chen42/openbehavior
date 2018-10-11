module rfid_antenna_housing(){
	difference(){
		cube([53,43,7], center=true); // rfid antenna outside;
		translate([3,0,0]) cube([56,36,3], center=true); // rfid antenna groove;
         color("green") translate([12,2,0]) cube([30,37,3.2], center=true); // rfid antenna groove, expand for wires
		cube([41,29,30], center=true); //rfid antenna loop inside  
	}
}
       

rfid_antenna_housing();