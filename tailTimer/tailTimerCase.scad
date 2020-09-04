//include <driverPlate.scad>;
$fn=50;


// define global variables (measurments, unit = mm)
lcdWidth = 121.4 + 25 - 25;
lcdWidthForScrewHolder = 121.4;
lcdThickness = 7.91;
lcdHeight = 76.80 ;
baseBoardThickness = 2;//.5;



squareHeight=7.5;
squareWidth=7.5;
squareThickness= 1;//2.5;

screwInnerRadius = 1.5;//2.56;
smallChipWidth = 19.18;
smallChipHeight = 33.32;

heightToScrew = 13.15; //12.88

smallChipThickness = 1.69;
smallChipHoleRadius = 2.42;
screenWidth = 109.8;
screenHeight = 66.4;

leftSideInputPortsWidth = 50.67;
leftSideInputPortsHeightFromBase = 21.36;
leftSideInputPortsHeight = 8.05;

endInputPortsHeightFromBase = 30.96;
endInputPortsWidth = 52.37;




overallWidth=77.33;
    width=72.91;
    protrodingWidth=overallWidth - width;
    protrodingThickness=2.2;
    
    
module base(){
rotate([0,90,0]) color("red") cube([baseBoardThickness+1, lcdWidth, lcdHeight], center=true);
}

module makeRearendWall(head=1){

    overallWidth=78.4;
    width=72.91;
    protrodingWidth=overallWidth - width;
    protrodingThickness=2.2;
    
    
    newWidth = ((baseBoardThickness+1)/2) + (width/2) +baseBoardThickness+1;

    
//    height=77.33;
//    
//    overallWidth=77.33;
//    width=77.48;//72.91;
//    protrodingWidth=overallWidth - width;
//    protrodingThickness=2.2;
    // front wall
    if(head ==  1){
        union(){
        translate([0,
                   (lcdWidthForScrewHolder/2 - (squareHeight/2)) + (squareHeight/2 + (baseBoardThickness+1) / 2),
                   (newWidth/2) - ((baseBoardThickness+1) / 2)
                  ]) cube([lcdHeight + ((baseBoardThickness+1) * 2),
                            baseBoardThickness+1,
                            newWidth
                            ], center=true);

        }
    }
     if(head == 0){
        translate([0,
                   -(((protrodingThickness) / 2) + (lcdWidth/2)),
                   width/2 - (baseBoardThickness - 1)]) cube([lcdHeight + ((baseBoardThickness+1)*2),
                          protrodingThickness,
                          width], center=true);
     }

    
}


module temp_rearend(){
    overallWidth=78.4;
    width=72.91;
    protrodingWidth=overallWidth - width;
    protrodingThickness=2.2;
    
    
    newWidth = ((baseBoardThickness+1)/2) + (width/2) +baseBoardThickness+1;
    
    difference(){
        translate([0,
                   -((lcdWidthForScrewHolder/2 - (squareHeight/2)) + (squareHeight/2 + (baseBoardThickness+1) / 2)),
                   (newWidth/2) - ((baseBoardThickness+1) / 2)
                  ]) cube([lcdHeight + ((baseBoardThickness+1) * 2),
                            baseBoardThickness+1,
                            newWidth
                            ], center=true);  

    
    union(){
        
    translate([-toTranslateX,-toTranslateYBottom - 5,((baseBoardThickness+1)/2) + (squareThickness/2) + heightToScrew + 3 + (squareHeight/2) + .5 - 1.5]) rotate([90,0,0]) translate([0,0,(depth/2)/2]) color("blue") cylinder(r=screwInnerRadius,h=depth/2,center=true);

translate([toTranslateX,-toTranslateYBottom - 5,((baseBoardThickness+1)/2) + (squareThickness/2) + heightToScrew + 3 + (squareHeight/2) + .5 - 1.5]) rotate([90,0,0]) translate([0,0,(depth/2)/2]) color("blue") cylinder(r=screwInnerRadius,h=depth/2,center=true);    
        
    }
}

}

temp_rearend();



module slider(){
    width = 77.37;
    height = 41.26;
    thickness = 2.11;        
    
    color("red") translate([0,0,lcdHeight/2 + (thickness/2) + (baseBoardThickness/2)]) cube([height, width,thickness],center=true);    
}


module makeTopBottomCover(top=true){
    overallWidth=78.4;
    width=72.91;
    protrodingWidth=overallWidth - width;
    protrodingThickness=2.2;
   if(top){
       // lcdHeight/2
       
//        (lcdWidth) +(baseBoardThickness+1)*2
   translate([0,0,width - (baseBoardThickness) -1]) cube([lcdHeight+((baseBoardThickness+1) *2), lcdWidth , baseBoardThickness+1],center=true);    
   }
   
   if(!top){
       //+ ((baseBoardThickness+1) *2)
       cube([lcdHeight+((baseBoardThickness+1) *2), (lcdWidth) ,baseBoardThickness+1],center=true);
   }
   
}

cutoff1 = (lcdHeight/2) + (baseBoardThickness/2);
xTempVar = ( (lcdHeight/2) + (baseBoardThickness/2) ) + ( ( (lcdHeight+((baseBoardThickness+1)*2)) )/2 - (cutoff1+ (baseBoardThickness/2) ) ) /2;
yTempVar = -( (lcdWidth/2) + ((baseBoardThickness/2)) + ( ((baseBoardThickness+1)/2) - (baseBoardThickness/2) ) );
zTempVar = 40;

module fourVerticalPoles(topPoles=true, head=true){
    radius = 1.50;//baseBoardThickness/2;
if(topPoles){

if(head){
color("red") translate([xTempVar, yTempVar, zTempVar]) cylinder(r=radius,h=20,center=true);
color("red") translate([-xTempVar, yTempVar, zTempVar]) cylinder(r=radius,h=20,center=true);
}
else{
color("red") translate([xTempVar, -yTempVar, zTempVar]) cylinder(r=radius,h=20,center=true);
color("red") translate([-xTempVar, -yTempVar, zTempVar]) cylinder(r=radius,h=20,center=true);
}

}

if(!topPoles){
color("red") translate([xTempVar,yTempVar,0]) cylinder(r=baseBoardThickness/3,h=20,center=true);
color("red") translate([-xTempVar,yTempVar,0]) cylinder(r=baseBoardThickness/3,h=20,center=true);
}

}

//color("blue") cube([lcdHeight+((baseBoardThickness+1) *2), (lcdWidth + ((baseBoardThickness+1) *2)) ,baseBoardThickness+1],center=true);


depth = squareThickness + 10;
module placeScrewHolder(x=(lcdHeight/2 - (squareWidth/2)) , y=(lcdWidthForScrewHolder/2 - (squareHeight/2)) , z=((baseBoardThickness+1)/2) + (squareThickness/2) + heightToScrew + 3, rearEnd=false, flag=1) {
    
    if(rearEnd==false){
    
    translate([x,y,z])
    difference(){
            cube([squareWidth,squareHeight,squareThickness],center=true);
            color("blue") cylinder(r=screwInnerRadius,h=squareThickness,center=true);
    }
    
    }
    
    if(rearEnd==true){
        if(flag == 1){
            translate([x,y,z])
            difference(){
                    cube([squareWidth,squareHeight,squareThickness],center=true);
                    color("blue") translate([.6,-.6,0]) cylinder(r=screwInnerRadius,h=squareThickness,center=true);    
            }
        }
            
        if(flag == 2){
            translate([x,y,z])
            difference(){
                    cube([squareWidth,squareHeight,squareThickness],center=true);
                    color("blue") translate([-.6,-.6,0]) cylinder(r=screwInnerRadius,h=squareThickness,center=true);            
        }
    }
    }
}

module placeCornerScrewHolder(x=0,y=0,z=0){
    translate([x,y,z])
    difference(){
    color("red") cube([squareWidth,squareHeight,depth],center=true);
    translate([0,0,(depth/2)/2]) color("blue") cylinder(r=screwInnerRadius,h=depth/2,center=true);
    }
}



//placeScrewHolder(x=(lcdHeight/2 - (squareWidth/2)),y=(lcdWidth/2 - (squareHeight/2)),z=((baseBoardThickness+1)/2) + (squareThickness/2) + heightToScrew);


toTranslateX = (lcdHeight/2) - (squareWidth/2);
toTranslateY = (lcdWidth/2) - (squareHeight/2);
//toTranslateZ = (lcdHeight/2) - ((baseBoardThickness+1)/2) - (depth/2);
//toTranslateZ =  depth/2 + ((baseBoardThickness+1)/2) + depth + width/2 + baseBoardThickness+1;


//toTranslateZ = 1.5*depth + 1.5*(baseBoardThickness+1) + width/2; //+ 2.5;
toTranslateZ = squareHeight + ((baseBoardThickness+1)/2) + (squareThickness/2) + heightToScrew + 3 + (squareHeight/2) + 1;


toTranslateYBottom = ( (lcdWidth/2) - (depth/2));
toTranslateZBottom =   (squareHeight/2) + ( (baseBoardThickness+1) / 2) + 15;
module makeScrewHolders(){
//placeScrewHolder(rearEnd=true,flag=2);
//
//placeScrewHolder(x=-(lcdHeight/2 - (squareWidth/2)), rearEnd=true);
//    
    




placeScrewHolder(y= -(lcdWidthForScrewHolder/2 - (squareHeight/2) ) );
//placeScrewHolder(y=-(lcdWidth/2 - (squareHeight/2)));

placeScrewHolder(x=-(lcdHeight/2 - (squareWidth/2)),y=-(lcdWidthForScrewHolder/2 - (squareHeight/2)));

// top four screw holder
placeCornerScrewHolder(x=toTranslateX,y=-toTranslateY,z=toTranslateZ);
placeCornerScrewHolder(x=toTranslateX,y=(lcdWidthForScrewHolder/2 - (squareHeight/2)),z=toTranslateZ);
    
placeCornerScrewHolder(x=-toTranslateX,y=-toTranslateY,z=toTranslateZ);        
placeCornerScrewHolder(x=-toTranslateX,y=(lcdWidthForScrewHolder/2 - (squareHeight/2)),z=toTranslateZ); 

// 

translate([toTranslateX,-toTranslateYBottom,((baseBoardThickness+1)/2) + (squareThickness/2) + heightToScrew + 3 + (squareHeight/2) + .5]) rotate([90,0,0]) placeCornerScrewHolder();
// z = toTranslateZBottom + heightToScrew
translate([-toTranslateX,-toTranslateYBottom,((baseBoardThickness+1)/2) + (squareThickness/2) + heightToScrew + 3 + (squareHeight/2) + .5 ]) rotate([90,0,0]) placeCornerScrewHolder();
       
}


module tempHolder(){
translate([0,110,0]) union(){
translate([toTranslateX,-toTranslateYBottom,19.9]) rotate([90,0,0]) placeCornerScrewHolder();
// z = toTranslateZBottom + heightToScrew
translate([-toTranslateX,-toTranslateYBottom,19.9]) rotate([90,0,0]) placeCornerScrewHolder();
}
}




extraBoardWidth = (smallChipHeight * 2) + 10;
extraBoardHeight = smallChipWidth + 5;

module extraBaseExtensions(){
// add extra base to hold two additional modules

//color("blue") translate([lcdHeight/2 + (smallChipWidth/2) + 5 ,0,0]) 
    cube([extraBoardHeight, ( (baseBoardThickness+1) *2) + (lcdHeight),(baseBoardThickness+1)], center=true);
}

GPIOSlotsWidth = 50.76/2;
GPIOSlotsHeight = 12.5;


module makeChipSlot(firstSlot=true){
    if(firstSlot){
translate([0,(smallChipHeight/2 + ((baseBoardThickness+1)/2) ),((baseBoardThickness+1) /2)- (smallChipThickness/2)]) cube([smallChipWidth,smallChipHeight,smallChipThickness],center=true);    
        }
        
     if(!firstSlot){
         translate([0,-(smallChipHeight/2 +((baseBoardThickness+1)/2)) ,((baseBoardThickness+1) /2) - (smallChipThickness/2)]) cube([smallChipWidth,smallChipHeight,smallChipThickness],center=true);
     }

}



h1 = (baseBoardThickness+1) - (smallChipThickness);

// extended base with two slots for the two additional sensors.
module sensorSpace(){
    
difference(){
    
difference(){
// extended base (to end)
extraBaseExtensions();
    // making slots for two sensors
    makeChipSlot(firstSlot=true);
    makeChipSlot(firstSlot=false);
}

// make four holes for the purpose of mounting two sensors.
#translate([(smallChipWidth/2) - (smallChipHoleRadius), (smallChipHeight / 2)+ (smallChipHeight/2 + ((baseBoardThickness+1)/2) ) - (smallChipHoleRadius), -(h1/2) - (smallChipThickness - ((baseBoardThickness+1) /2))]) cylinder(r=smallChipHoleRadius - 0.5,h=h1,center=true);

#translate([(smallChipWidth/2) - (smallChipHoleRadius), (smallChipHoleRadius) + ((baseBoardThickness+1)/2), -(h1/2) - (smallChipThickness - ((baseBoardThickness+1) /2))]) cylinder(r=smallChipHoleRadius - 0.5,h=h1,center=true);


#translate([(smallChipWidth/2) - (smallChipHoleRadius), -((smallChipHeight / 2)+ (smallChipHeight/2 + ((baseBoardThickness+1)/2) ) - (smallChipHoleRadius) ), -(h1/2) - (smallChipThickness - ((baseBoardThickness+1) /2))]) cylinder(r=smallChipHoleRadius - 0.5,h=h1,center=true);

#translate([(smallChipWidth/2) - (smallChipHoleRadius), -((smallChipHoleRadius) + ((baseBoardThickness+1)/2)), -(h1/2) - (smallChipThickness - ((baseBoardThickness+1) /2))]) cylinder(r=smallChipHoleRadius - 0.5,h=h1,center=true);


}
}


// side walls ( default = [left=1, right=2] )
module makeSideWall(sides=[1,0]){
    height=77.33;
    
    overallWidth=77.33;
    width=72.91;//77.48;
    protrodingWidth=overallWidth - width;
    protrodingThickness=2.2;
    //(lcdWidthForScrewHolder/2 - (squareHeight/2))
    //((baseBoardThickness+1) /2)+(lcdWidth/2)
    //lcdWidth
    newWidth = ((baseBoardThickness+1)/2) + (width/2) - .5;
    if(sides == [1,0]){
        color("red") translate([ -( (lcdHeight/2) +((baseBoardThickness+1)/2) ),0,((newWidth) /2) - ( (baseBoardThickness+1) / 2)]) cube([baseBoardThickness+1,lcdWidth,newWidth],center=true);
            
       }
    if(sides == [0,1]){
        
        color("blue") translate([ (lcdHeight/2) +((baseBoardThickness+1)/2),0, ((newWidth) /2) - ( (baseBoardThickness+1) / 2)]) cube([baseBoardThickness+1,lcdWidth,newWidth],center=true);
    }
}


// cut center of the base for screen
module baseWithScreen(){
difference(){
// base (bottom cover with added length)
makeTopBottomCover(top=0);
//base();
// groove for screen
translate([1.5,-.5,0]) rotate([0,0,90]) cube([screenWidth,screenHeight,(baseBoardThickness+1)],center=true);
}
}

module makePowerSlot(){
slotWidth = 8.35;
slotHeight = 4.2;
slotDepth = baseBoardThickness+1;
slotToEdge = 40.5;
moveZAxis = 5;
color("red") translate([(lcdHeight/2) - ((baseBoardThickness+1)/2) + slotDepth,-screenWidth/2 + (slotWidth/2) + slotToEdge/2 + (5),(slotDepth/2) + (squareThickness/2) + heightToScrew + moveZAxis]) cube([slotDepth+3,slotWidth+7,slotHeight+7],center=true);
}



module makeSlots(){
   difference(){
       makeSideWall();
       color("blue") translate([ -(lcdHeight/2 + 1.5),0 , leftSideInputPortsHeightFromBase + (leftSideInputPortsHeight/2)-3]) cube([baseBoardThickness+1,leftSideInputPortsWidth+5,leftSideInputPortsHeight],center=true);
    
   }
}


module prism(l,w,h,center=true){
    translate_to = center ? [-(l/2),-(w/2),-(h/2)] : [0,0,0];
    translate(translate_to)
    polyhedron(
        points=[[0,0,0],[l,0,0],[l,w,0],[0,w,0],[0,w,h],[l,w,h]],
        faces=[[0,1,2,3],[5,4,3,2],[0,4,5,1],[0,3,4],[5,2,1]]
    );
}


//rotate([0,180,90]) 
triLength = lcdHeight;
triWidth = lcdWidth;
triHeight = baseBoardThickness + 15;
//prism(lcdWidth,(lcdWidth/2) + 30,triHeight);
//translate([0,0,(triHeight/2)+ ( (lcdHeight/2) - ((baseBoardThickness+1)/2) ) ]) 
xx = atan(triHeight/triLength);
yy = 180-90-xx;
zz = 90-yy;
hypo = sqrt( (triLength*triLength) + (triHeight+triHeight) );

//translate([-(lcdHeight/2 + (baseBoardThickness+1) ),0,hypo/2 -1]) rotate([-90-xx,0,-90]) prism(lcdWidth,lcdHeight,triHeight);

//#cube([triLength,triLength,triHeight],center=true);

module makeTriangleWidget(){
translate([-(lcdHeight/2 + (baseBoardThickness+1) ),0,hypo/2 -1]) rotate([-90-xx,0,-90]) difference(){
    prism(lcdWidth,lcdHeight,triHeight);
    cube([triLength,triLength,triHeight],center=true);
}
}
//translate([0,0,(triHeight/2) + (lcdHeight/2) - ((baseBoardThickness+1)/2)]) rotate(-90,0,-90) prism(lcdWidth,lcdHeight,triHeight);
//degreeToTurn = atan( (15) / (lcdWidth/2) );
degreeToTurn = atan((lcdWidth/2) / triHeight);
xDeg = atan((lcdWidth/2) / triHeight);
yDeg = 180 - 90 - xDeg;

//translate([0,0,79.09]) rotate([-degreeToTurn,180,90]) translate([0,0,15/2 + ((lcdHeight/2) - ( (baseBoardThickness+1) / 2))]) prism(lcdWidth,(lcdWidth/2),15);


module tempSupport(){
support_height=27;
support_radius=5;
translate([(lcdHeight+((baseBoardThickness+1) *2))/2 - (support_radius), -58,support_height/2 + (lcdHeight/2)]) cylinder(r=support_radius,h=support_height,center=true);

translate([(lcdHeight+((baseBoardThickness+1) *2))/2 - (support_radius), 58,support_height/2 + (lcdHeight/2)]) cylinder(r=support_radius,h=support_height,center=true);
}

//******************************************//

/*
    Following modules are used to print the individual pieces.
    Note that each individual module should be printed seperated.
*/

//******************************************//


module tempSlot(){
extraZ = 10 -5;
    color("red") translate([0, (lcdWidth/2) + ((baseBoardThickness+1)/2)   ,((lcdHeight/4)/2) + ((baseBoardThickness+1) /2) + 10 + extraZ/2 ]) cube([ (lcdHeight+((baseBoardThickness+1)*30)) / 4 + 12,(baseBoardThickness+1) +10,lcdHeight/4 + extraZ],center=true);
//union(){
//        color("red") translate([0, (lcdWidth/2) + ((baseBoardThickness+1)/2)  ,((lcdHeight/4)/2) + ((baseBoardThickness+1) /2) + 10 + extraZ/2 ]) cube([ (lcdHeight+((baseBoardThickness+1)*30)) / 4 + 15,(baseBoardThickness+1) +10,lcdHeight/4 + extraZ],center=true);
////translate([0, (lcdWidth/2) + ((baseBoardThickness+1)/2) ,((lcdHeight/4)/2) + ((baseBoardThickness+1) /2) + 24])cube([5,(baseBoardThickness+1),5],center=true);
//
//}
}
// putting together two side walls and the base
module mainPiece(){
difference(){
union(){
  #baseWithScreen();
    difference(){
        makeSideWall();
        
//        union(){
//        translate([0,12,10]) makePlateSlot();
//        translate([0,-12,10]) makePlateSlot();
//        }
        
    }
//  difference(){
//  makeSideWall([0,1]);
//  makePowerSlot();
//  }
    difference(){
        makeRearendWall(1);
        tempSlot();

  }
  
  //makeTriangleWidget();
  translate([0,0,-1.5]) makeScrewHolders();

}

}

}




module fontEndWall(){
difference(){

//makeRearendWall(0);
    //protrodingThickness
    translate([0,-(((protrodingThickness) /2)+(lcdWidth/2)),width/2-(baseBoardThickness-1)]) cube([lcdHeight+((baseBoardThickness+1)*2),1,width +3],center=true);
 union(){
    translate([-toTranslateX,-toTranslateYBottom,toTranslateZBottom + heightToScrew]) color("blue") rotate([90,0,0]) cylinder(r=screwInnerRadius,h=depth/2+20,center=true);

translate([toTranslateX,-toTranslateYBottom,toTranslateZBottom + heightToScrew]) color("blue") rotate([90,0,0]) cylinder(r=screwInnerRadius,h=depth/2+20,center=true);
 }
}


}


module topCover(){

difference(){    
makeTopBottomCover(top=true);

union(){
    translate([toTranslateX,-toTranslateY,toTranslateZ]) translate([0,0,(depth/2)/2]) color("blue") cylinder(r=screwInnerRadius,h=depth/2 + 20,center=true);

    translate([-toTranslateX,-toTranslateY,toTranslateZ]) translate([0,0,(depth/2)/2]) color("blue") cylinder(r=screwInnerRadius,h=depth/2 + 20,center=true);
        

    translate([toTranslateX,toTranslateY,toTranslateZ]) translate([0,0,(depth/2)/2]) color("blue") cylinder(r=screwInnerRadius,h=depth/2 + 20,center=true);
        

    translate([-toTranslateX,toTranslateY,toTranslateZ]) translate([0,0,(depth/2)/2]) color("blue") cylinder(r=screwInnerRadius,h=depth/2 + 20,center=true);
}

}

}


//----------------------------------------------------------------------------------
mountDiameter = 2.2;
mountRadius = mountDiameter/2;

mountWidth = 30.1;
mountLength = 69.95;
mountDepth = 1;

mountHoleDepth = 15;
positionThreshold = 0.53;
//translate([0,0,20])
buttonDiameter = 13;
buttonRadius = buttonDiameter/2;
buttonOffset = 4.88;

module placeHoles(){
    color("red") translate([mountLength/2 - mountRadius - positionThreshold,mountWidth/2 - mountRadius - positionThreshold,0]) cylinder(h=mountHoleDepth,r=mountRadius,center=true);

    color("red") translate([mountLength/2 - mountRadius - positionThreshold, - mountWidth/2 + mountRadius + positionThreshold,0]) cylinder(h=mountHoleDepth,r=mountRadius,center=true);


    color("red") translate([-mountLength/2 + mountRadius + positionThreshold, - mountWidth/2 + mountRadius + positionThreshold,0]) cylinder(h=mountHoleDepth,r=mountRadius,center=true);

    color("red") translate([-mountLength/2 + mountRadius + positionThreshold, mountWidth/2 - mountRadius - positionThreshold,0]) cylinder(h=mountHoleDepth,r=mountRadius,center=true);
}

module prototypeBoard(){
    translate([ +mountLength/2 + 5 ,50,mountWidth/2 + 25]) rotate([90,0,90]) 
//    difference(){
//                cube([mountLength,mountWidth,mountDepth],center=true);
    union(){

        translate([-buttonOffset - buttonRadius,0,0]) cylinder(h=mountHoleDepth, r=buttonRadius, center=true);
        
        translate([buttonOffset + buttonRadius,0,0]) cylinder(h=mountHoleDepth, r=buttonRadius, center=true);
            
            placeHoles();
    }
//    }
}


module makePlateSlot(){
    baseX = 2;
baseY = 40;
baseZ = 30+5;

driverX = 1;
driverY = 15.42+.5;
driverZ = 20.46+.5;

toPlaceY = 10;
toPlaceYOffset = 1/2;




screwDiameter = 1.78 * 2;
screwHeight = 11.12;





toPlaceZ = (driverZ / 2) + (screwDiameter/2) + .5;
//translate([baseX / 2 - (driverX/2),toPlaceY-10,0]) 
//    color("blue") cube([driverX,driverY,driverZ],center=true);

translate([-(lcdHeight/2) - (baseX/2),0,baseZ]) 
color("blue")  union(){
    translate([baseX / 2 - (driverX/2) +.000001,toPlaceY-10,0])
    color("blue") cube([driverX,driverY,driverZ],center=true);

    translate([0,-screwDiameter/2 - (driverY/2),0]) union(){
translate([0,toPlaceY + toPlaceYOffset, toPlaceZ]) rotate([0,90,0]) color("blue") cylinder(h=screwHeight,r=screwDiameter/2,center=true);

translate([0,toPlaceY + toPlaceYOffset, -toPlaceZ]) rotate([0,90,0]) color("blue") cylinder(h=screwHeight,r=screwDiameter/2,center=true);
    }
}
}




//prototypeBoard();
// ######### top panel with button slot ##################


//difference(){
//union(){
//mainPiece();  
//  tempHolder();  
//difference(){
//    difference(){
//makeSideWall([0,1]);
//    translate([0,0,-2]) makePowerSlot();
//       }
////translate([0,-55,4]) prototypeBoard();
//}
//
//}
//
//color("red") translate([0,62,3.58 + 5]) cube([6,10,3.58],center=true);
//}





//prototypeBoard();
// ######################################################
//----------------------------------------------------------------------------------


//******************************************//
//******************************************//
/*
    ****** PRINT EACH PART SEPARATELY ******
*/
//******************************************//
//******************************************//


//prototypeBoardHeight = 30.2;
//prototypeBoardWidth = 70.21;
//prototypeBoardThickness = 2;
//
////translate([-(lcdHeight /2) + prototypeBoardThickness/2,0,prototypeBoardHeight/2]) 
//cube([prototypeBoardThickness,prototypeBoardWidth, prototypeBoardHeight], center=true);
//



//fontEndWall();






//union(){
//    
//    difference(){
//        topCover();
//        translate([0,0, 67]) union(){
//            translate([toTranslateX,-toTranslateY,(depth/2)/2]) color("blue") cylinder(r=screwInnerRadius,h=depth/2,center=true);
//            translate([toTranslateX,(lcdWidthForScrewHolder/2 - (squareHeight/2)),(depth/2)/2]) color("blue") cylinder(r=screwInnerRadius,h=depth/2,center=true);
//
//            translate([-toTranslateX,-toTranslateY,(depth/2)/2]) color("blue") cylinder(r=screwInnerRadius,h=depth/2,center=true);
//            translate([-toTranslateX,(lcdWidthForScrewHolder/2 - (squareHeight/2)),(depth/2)/2]) color("blue") cylinder(r=screwInnerRadius,h=depth/2,center=true);
//        }
//    }
//    monitorLegLength=25.5;
//    monitorLegDiameter=10.3;
//
//    translate([width/2 - (monitorLegDiameter),0,0]){
//        translate([0,width/2 + (monitorLegDiameter),(monitorLegLength/2) + (width) - 1.5 ]) rotate([0,0,90]) cylinder(h=monitorLegLength, d=monitorLegDiameter,center=true);
//
//        translate([0,-(width/2 + (monitorLegDiameter)),(monitorLegLength/2) + (width) - 1.5 ]) rotate([0,0,90]) cylinder(h=monitorLegLength, d=monitorLegDiameter,center=true);
//    }
//
//}