module rfid_antenna_housing(){
	difference(){
		cube([53,43,7], center=true); // rfid antenna outside;
		translate([3,0,0]) cube([56,37,3.6], center=true); // rfid antenna groove;
		cube([39,31,30], center=true); //rfid antenna loop inside  
	}
}

rfid_antenna_housing();