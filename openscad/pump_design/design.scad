$fn=50;


height=59.35 - 2.4;
width=47.60;
thickness=10.65;

topWidth=38.29;
topHeight=23.70;
bottomWidth=31.10;
bottomHeight=height-topHeight;
thickness3=6.57;



diameter=28.88;



circleThickness=2;
radius=diameter/2 + 1;

smallRecHeight=8.38;
smallRecWidth=3.33;
cuttingWidth=23.59;
cuttingHeight=14.69;
extraHeight = (height - (smallRecHeight + cuttingHeight));
extraWidth = 3.63;

bigCircleDiameter=27.33;
topHalfHeight=29.63;
remaindingHeight=height-topHalfHeight;

hex_nut_diameter=7.89 + 1.6; // +1.6, 
hex_nut_radius=hex_nut_diameter/2;
hex_nut_thickness=3.85;

hex_nut_inner_diameter= 5.8;//5;
hex_nut_inner_radius=hex_nut_inner_diameter/2 + .4;



temp=(thickness/2) - (thickness - thickness3);
offsetFromCenter=19; //19.25; //1.5 // 2.3
hexNutGroveExtraDepth=2;

screwRadius=1.75;
screwDepth=9.35;

module part1(){
translate([(width/2) - (topWidth/2) ,(thickness/2) - (thickness3)/2,0]) color("blue") difference(){    
    difference(){
cube([topWidth, thickness3, height], center=true);  

union(){
color("blue") translate([topWidth/2 - (extraWidth/2),0,-extraHeight/2 + ( (height/2) - (smallRecHeight + cuttingHeight) )]) cube([extraWidth,thickness3 ,extraHeight],center=true);

color("blue") translate([ -(topWidth/2 - (extraWidth/2)),0,-extraHeight/2 + ( (height/2) - (smallRecHeight + cuttingHeight) )]) cube([extraWidth,thickness3 ,extraHeight],center=true);
}


//translate([0,0,extraHeight - (height/2) - offsetFromCenter]) union(){
//    //-(remaindingHeight/2) + (hex_nut_radius)
//translate([0,5,0]) color("black") rotate([90,0,0]) cylinder(h=hex_nut_thickness/2 + hexNutGroveExtraDepth + 1.3, r=hex_nut_radius,center=true, $fn = 6); //h=thickness3
////-(remaindingHeight/2) + (hex_nut_inner_radius + (hex_nut_radius - hex_nut_inner_radius))
//translate([0, 0,0]) color("red") rotate([90,0,0]) cylinder(h=hex_nut_thickness/2 + 10, r=hex_nut_inner_radius,center=true, $fn = 6);
//}


}
union(){
    translate([0,-((-(thickness3/2)+(thickness3-circleThickness)/2)),(height/2) - (smallRecHeight + cuttingHeight) ]) union(){
translate([0,0,(cuttingHeight/2) + (smallRecHeight)]) cube([cuttingWidth,thickness3 - circleThickness +.1, cuttingHeight],center=true);
                 translate([0,0,smallRecHeight/2]) cube([smallRecWidth,thickness3 - circleThickness+.1,smallRecHeight],center=true);            
}


translate([0,-(thickness3/2 - (circleThickness/2)),(height/2) - (radius)]) color("red")rotate([90,0,0])union(){
        cylinder(h=circleThickness, r=radius, center=true);
        translate([0,radius/2,0])cube([radius*2,radius,circleThickness],center=true);
    }
    
    }

}
}


module part2(){
//translate([0,temp,0]) 
difference(){
cube([width,thickness,height],center=true);
//translate([0,(thickness/2) - (thickness - thickness3)/2,0]) color("blue") cube([topWidth,thickness - thickness3,height],center=true);
//
translate([(width/2) - (topWidth/2),(thickness/2) - (thickness3)/2,0]) color("blue") union(){
cube([topWidth, thickness3, height], center=true);   
union(){
color("red") translate([topWidth/2 - (extraWidth/2),0,-extraHeight/2 + ( (height/2) - (smallRecHeight + cuttingHeight) )]) cube([extraWidth,thickness3+10 ,extraHeight],center=true);

color("red") translate([ -(topWidth/2 - (extraWidth/2)),0,-extraHeight/2 + ( (height/2) - (smallRecHeight + cuttingHeight) )]) cube([extraWidth,thickness3+10,extraHeight],center=true);
}


//translate([0,0, extraHeight - (height/2)  - offsetFromCenter]) union(){
//    
//translate([0, -temp - (hex_nut_thickness/2) - .8,0]) color("red") rotate([90,0,0]) cylinder(h=hex_nut_thickness/2 + hexNutGroveExtraDepth, r=hex_nut_radius,center=true, $fn = 6);
//
//translate([0, -temp - (hex_nut_thickness/2),0]) color("red") rotate([90,0,0]) cylinder(h=hex_nut_thickness/2 + 7, r=hex_nut_inner_radius,center=true, $fn = 6);
//}


}
}

}

module glueScrews(){
translate([0,0.1,0]) union(){
rotate([90,0,0]) translate([(width/2) - (topWidth/2) - (topWidth/4),-(height/3),-(thickness-screwDepth)/2]) cylinder(h=screwDepth,r=screwRadius,center=true);

rotate([90,0,0]) translate([(width/2) - (topWidth/2) + (topWidth/4),-(height/9),-(thickness-screwDepth)/2]) cylinder(h=screwDepth,r=screwRadius,center=true);
}
}


module modifiedParts(part=1){


difference(){
    
        if(part == 1){
            part1();
        }else if(part == 2){
            part2();
        }
//        part2();    

translate([(width/2) - (topWidth/2),0,extraHeight - (height/2) - offsetFromCenter]) union(){
    //-(remaindingHeight/2) + (hex_nut_radius)
    
    //((hex_nut_thickness/2 + 10)/2)-(hex_nut_thickness/2 + hexNutGroveExtraDepth + 1.3)/2
translate([0,0,0]) color("black") rotate([90,0,0]) cylinder(h=hex_nut_thickness, r=hex_nut_radius,center=true, $fn = 6); //h=thickness3
//-(remaindingHeight/2) + (hex_nut_inner_radius + (hex_nut_radius - hex_nut_inner_radius))
translate([0, 0,0]) color("red") rotate([90,0,0]) cylinder(h=hex_nut_thickness+ 20, r=hex_nut_inner_radius,center=true, $fn = 6);
    
//    glueScrews();
}

}
}


rotate([-90,0,0]) difference(){
modifiedParts(1);
   glueScrews(); 
}

//rotate([90,0,0]) difference(){
//
//modifiedParts(2);
//    glueScrews();
//}
