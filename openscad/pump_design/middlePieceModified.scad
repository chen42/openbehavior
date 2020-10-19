pumpHolderWidth=50.25;
pumpHolderHeight=36;//38.26;
pumpHolderThickness=10.20;


semiCircleDiameter=19; //16.36;
semiCircleRadius=semiCircleDiameter/2;

semiCircleHeight=26.54;
semiCircleThickness=7.23;

recBlockHeight=13.63;
recBlockWidth=8.25;

offsetThickness=2.03;



sideScrewRadius=1.75;
sideScrewHeight=4;
sideScrewOffsetRatio=0.38;

rotate([90,0,0]) scale([0.94,1,1]) translate([0,0,0]) difference(){
minkowski(){
    
difference(){
difference(){
difference(){
    cube([pumpHolderWidth,pumpHolderThickness,pumpHolderHeight],center=true);

    translate([0,(pumpHolderThickness/2)-(semiCircleThickness/2)+.001,(pumpHolderHeight/2) - (semiCircleHeight/2) + .5]) color("red") union(){
    rotate([90,0,0]) cylinder(h=pumpHolderThickness+5,r=semiCircleRadius, center=true);

    color("blue") translate([0,0,(semiCircleHeight/2)/2]) cube([semiCircleDiameter,pumpHolderThickness+5,semiCircleHeight/2 +.1],center=true);
    }
}

union(){
color("red") translate([(pumpHolderWidth/2)-(recBlockWidth/2),0,-(pumpHolderHeight/2)+(recBlockHeight/2)]) cube([recBlockWidth,pumpHolderThickness,recBlockHeight],center=true);

color("red") translate([-((pumpHolderWidth/2)-(recBlockWidth/2)),0,-(pumpHolderHeight/2)+(recBlockHeight/2)]) cube([recBlockWidth,pumpHolderThickness,recBlockHeight],center=true);
}

}

translate([0,(pumpHolderThickness/2)-(offsetThickness/2),(pumpHolderHeight-recBlockHeight)/2 - ((pumpHolderHeight/2) - recBlockHeight)]) color("black") cube([pumpHolderWidth-3,offsetThickness,pumpHolderHeight-recBlockHeight],center=true);

}


cylinder(1,center=true,$fn=50);
    
}
    union(){
        screwZAxisoffSet=2.15;
        color("red") translate([pumpHolderWidth/2 - (recBlockWidth/2) - (sideScrewHeight/2)-3.1,0,(pumpHolderHeight/2) + 1/2 -(pumpHolderHeight-recBlockHeight) - (sideScrewOffsetRatio*recBlockHeight) - screwZAxisoffSet]) rotate([0,90,0]) cylinder(h=sideScrewHeight,r=sideScrewRadius,$fn=50,center=true);

color("red") translate([-(pumpHolderWidth/2 - (recBlockWidth/2) - (sideScrewHeight/2)-3.1  ),0,(pumpHolderHeight/2) + 1/2 -(pumpHolderHeight-recBlockHeight) - (sideScrewOffsetRatio*recBlockHeight) - screwZAxisoffSet]) rotate([0,90,0]) cylinder(h=sideScrewHeight,r=sideScrewRadius,$fn=50,center=true);
    }
}



//
////pumpHolderWidth
////recBlockWidth/2 + (sideScrewHeight/2)
//color("red") translate([pumpHolderWidth/2 - (recBlockWidth/2) - (sideScrewHeight/2)-3.1,0,(pumpHolderHeight/2) + 1/2 -(pumpHolderHeight-recBlockHeight) - (sideScrewOffsetRatio*recBlockHeight)]) rotate([0,90,0]) cylinder(h=sideScrewHeight,r=sideScrewRadius,$fn=50,center=true);
//
//color("red") translate([-(pumpHolderWidth/2 - (recBlockWidth/2) - (sideScrewHeight/2)-3.1 ),0,(pumpHolderHeight/2) + 1/2 -(pumpHolderHeight-recBlockHeight) - (sideScrewOffsetRatio*recBlockHeight)]) rotate([0,90,0]) cylinder(h=sideScrewHeight,r=sideScrewRadius,$fn=50,center=true);
////cube([60,1,1],center=true);
//
//
//color("blue") translate([0,0,recBlockHeight/2]) cube([recBlockWidth, pumpHolderThickness,recBlockHeight],center=true);
//minkowski(){
//    translate([0,0,recBlockHeight/2]) cube([recBlockWidth, pumpHolderThickness,recBlockHeight],center=true);
//    cylinder(.00000000001,center=true,$fn=50);
//}



//-----------------------------------------

//translate([0,(pumpHolderThickness/2)-(offsetThickness/2),(pumpHolderHeight-recBlockHeight)/2 - ((pumpHolderHeight/2) - recBlockHeight)]) color("black") cube([pumpHolderWidth-3,offsetThickness,pumpHolderHeight-recBlockHeight],center=true);

//
//difference(){
//    %cube([pumpHolderWidth,pumpHolderThickness,pumpHolderHeight],center=true);
//
//    translate([0,(pumpHolderThickness/2)-(semiCircleThickness/2)+.001,(pumpHolderHeight/2) - (semiCircleHeight/2)]) color("red") union(){
//    rotate([90,0,0]) cylinder(h=pumpHolderThickness+5,r=semiCircleRadius, center=true);
//
//    color("red") translate([0,0,(semiCircleHeight/2)/2]) cube([semiCircleDiameter,pumpHolderThickness+5,semiCircleHeight/2 +.1],center=true);
//    }
//}