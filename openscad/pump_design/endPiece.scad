

pumpHolderWidth=50.25;
pumpHolderHeight=38.17;
pumpHolderThickness=10.15;


semiCircleDiameter=22; //16.36;
semiCircleRadius=semiCircleDiameter/2;

semiCircleHeight=26.54;
semiCircleThickness=7.23;


//difference(){
//    cube([pumpHolderWidth,pumpHolderThickness,pumpHolderHeight],center=true);
//
//    translate([0,(pumpHolderThickness/2)-(semiCircleThickness/2)+.001,(pumpHolderHeight/2) - (semiCircleHeight/2)]) color("red") union(){
//    rotate([90,0,0]) cylinder(h=pumpHolderThickness+5,r=semiCircleRadius, center=true);
//
//    color("red") translate([0,0,(semiCircleHeight/2)/2]) cube([semiCircleDiameter,pumpHolderThickness+5,semiCircleHeight/2],center=true);
//    }
//}

recHeight=32.96;
recWidth=33.45;
recThickness=6.3;

sideScrewDiameter=3.5;
sideScrewRadius=sideScrewDiameter/2;
sideScrewDepth=4.65;



cubeShape=6.38;


topPlateHeight= 23.44;//1.45;
topPlateOffset = 1.45;

module sideScrew(){
    cylinder(h=sideScrewDepth,r=sideScrewRadius,center=true);
}

module makeFourSideScrews(){
union(){
color("red") translate([(recWidth/2)-(sideScrewDepth/2),0,(recHeight/2) - (cubeShape/2)]) rotate([0,090,0]) sideScrew();
color("red") translate([-((recWidth/2)-(sideScrewDepth/2)),0,(recHeight/2) - (cubeShape/2)]) rotate([0,090,0]) sideScrew();

color("red") translate([((recWidth/2)-(sideScrewDepth/2)),0,-((recHeight/2) - (cubeShape/2))]) rotate([0,090,0]) sideScrew();
color("red") translate([-((recWidth/2)-(sideScrewDepth/2)),0,-((recHeight/2) - (cubeShape/2))]) rotate([0,090,0]) sideScrew();   
}

}




module endPieceBlock(){
difference(){
cube([recWidth,recThickness,recHeight],center=true);
makeFourSideScrews();
}
}


hookWidth=12;//7.40;
hookHeight=7;
hookThickness=5;

stopperWidth=(1/2)*hookWidth;
stopperHeight=(1/2)*hookHeight;


module recStopper(){
//difference(){
//    //hookHeight+2
//cube([hookWidth,recThickness,hookHeight+2],center=true);
//
//translate([(stopperWidth/2) + (hookWidth/2)-(stopperWidth),0,-stopperHeight/2]) union(){
//cube([stopperWidth,recThickness,stopperHeight],center=true);
//color("blue") translate([-((1/2)*stopperWidth)/2,0,2*((stopperHeight-1)/2)]) cube([(1/2)*stopperWidth,hookThickness,stopperHeight-1],center=true);
//}
//}

difference(){
cube([hookWidth,recThickness,hookHeight+2],center=true);
    translate([1.5,0,-(hookHeight/1.5)/2]) cube([hookWidth/4,recThickness,hookHeight/1.2],center=true);
}
}




module circleStopper(){
difference(){
rotate([90,0,0]) cylinder(h=recThickness,r=5,center=true,$fn=50);
union(){
rotate([90,0,0]) cylinder(h=recThickness,r=2.5,center=true,$fn=50);
translate([-(2.5/2)-(2.5),0,0]) cube([2.5+.1,recThickness,0.8],center=true);
}
}
}

module pumpHolder(){
translate([0,0,(topPlateHeight/2) + recHeight/2]) union(){
difference(){
    color("red") cube([recWidth,recThickness,topPlateHeight],center=true);

translate([0,0,-(topPlateHeight/2)+(semiCircleRadius) +topPlateOffset+5]) union(){
translate([0,0, semiCircleRadius/2]) cube([semiCircleDiameter,recThickness,semiCircleRadius],center=true); //topPlateHeight/2+5
rotate([90,0,0]) cylinder(h=recThickness,r=semiCircleRadius,center=true);
}

}
union(){
translate([(hookWidth/2)+(recWidth/2),0,((hookHeight+2)/2)]) recStopper();

translate([-5 - (recWidth/2) +1,0,((hookHeight+2)/2)]) circleStopper();
}
}
}



module endPiece(){
    union(){
        endPieceBlock();
        pumpHolder();
    }
}

endPiece();


//difference(){
//    //hookHeight+2
//%cube([hookWidth,recThickness,hookHeight+2],center=true);
//
//translate([(stopperWidth/2) + (hookWidth/2)-(stopperWidth),0,-stopperHeight/2]) union(){
//%cube([stopperWidth,recThickness,stopperHeight],center=true);
////color("blue") translate([-((1/2)*stopperWidth)/2,0,2*((stopperHeight-1)/2)]) 
//    color("blue") cube([(1/2)*stopperWidth,hookThickness,stopperHeight-1],center=true);
//}
//}



//translate([stopperWidth/2,0,-((hookHeight+2)/4)]) %cube([stopperWidth,recThickness,(hookHeight+2)/2],center=true);
////color("blue") translate([-((1/2)*stopperWidth)/2,0,2*((stopperHeight-1)/2)]) 
//    color("blue") cube([(1/2)*stopperWidth,hookThickness,stopperHeight-1],center=true);