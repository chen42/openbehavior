$fn=50;

// define global variables (measurments, unit = mm)
lcdWidth = 121.4 + 25;
lcdWidthForScrewHolder = 121.4;
lcdThickness = 7.91;
lcdHeight = 76.80;
baseBoardThickness = 3;


squareHeight=7.5;
squareWidth=7.5;
squareThickness=2.5;

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


module base(){
rotate([0,90,0]) color("red") cube([baseBoardThickness+1, lcdWidth, lcdHeight], center=true);
}

module makeRearendWall(head=1){
    // front wall
    if(head ==  1){
        translate([0,((baseBoardThickness+1) /2)+(lcdWidth/2),(lcdHeight/2)/2 - ((baseBoardThickness+1) /2)]) cube([lcdHeight+((baseBoardThickness+1)*2),baseBoardThickness+1,lcdHeight/2],center=true);    
    }
    
    // end wall
    if(head == 0){
//        translate([0,-(((baseBoardThickness+1) /2)+(lcdWidth/2)),(lcdHeight/2)/2 - ((baseBoardThickness+1) /2) + ((baseBoardThickness+1) /2 )]) cube([lcdHeight+((baseBoardThickness+1)*2),baseBoardThickness+1,lcdHeight/2 - (baseBoardThickness+1) ],center=true);    
                translate([0,-(((baseBoardThickness+1) /2)+(lcdWidth/2)),((lcdHeight/2) /2 -((baseBoardThickness+1)/2))]) cube([lcdHeight+((baseBoardThickness+1)*2),baseBoardThickness+1,lcdHeight/2 ],center=true);
    }
    
    //lcdHeight/2
}

//color("red") translate([0, (lcdWidth/2) + ((baseBoardThickness+1)/2) ,((lcdHeight/6)/2) + ((baseBoardThickness+1) /2)]) cube([ (lcdHeight+((baseBoardThickness+1)*2)) / 4 ,(baseBoardThickness+1),lcdHeight/6],center=true);
//makeTopBottomCover(top=false);
//makeRearendWall(head=1);

module makeTopBottomCover(top=true){
   if(top){
   // + ((baseBoardThickness+1) *2)
   translate([0,0,lcdHeight/2]) cube([lcdHeight+((baseBoardThickness+1) *2), (lcdWidth) +(baseBoardThickness+1)*2 , baseBoardThickness+1],center=true);    
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
module placeScrewHolder(x=(lcdHeight/2 - (squareWidth/2)) , y=(lcdWidthForScrewHolder/2 - (squareHeight/2)) , z=((baseBoardThickness+1)/2) + (squareThickness/2) + heightToScrew) {
    translate([x,y,z])
    difference(){
            cube([squareWidth,squareHeight,squareThickness],center=true);
            color("blue") cylinder(r=screwInnerRadius,h=squareThickness,center=true);
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
toTranslateZ = (lcdHeight/2) - ((baseBoardThickness+1)/2) - (depth/2);

toTranslateYBottom = ( (lcdWidth/2) - (depth/2));
toTranslateZBottom =   (squareHeight/2) + ( (baseBoardThickness+1) / 2);
module makeScrewHolders(){
placeScrewHolder();

placeScrewHolder(x=-(lcdHeight/2 - (squareWidth/2)));

placeScrewHolder(y= -(lcdWidthForScrewHolder/2 - (squareHeight/2) ) );
//placeScrewHolder(y=-(lcdWidth/2 - (squareHeight/2)));

placeScrewHolder(x=-(lcdHeight/2 - (squareWidth/2)),y=-(lcdWidthForScrewHolder/2 - (squareHeight/2)));

// top four screw holder
placeCornerScrewHolder(x=toTranslateX,y=-toTranslateY,z=toTranslateZ);
placeCornerScrewHolder(x=-toTranslateX,y=-toTranslateY,z=toTranslateZ);        
 
placeCornerScrewHolder(x=toTranslateX,y=toTranslateY,z=toTranslateZ);
placeCornerScrewHolder(x=-toTranslateX,y=toTranslateY,z=toTranslateZ); 
    
// 

translate([toTranslateX,-toTranslateYBottom, toTranslateZBottom + heightToScrew]) rotate([90,0,0]) placeCornerScrewHolder();
translate([-toTranslateX,-toTranslateYBottom,toTranslateZBottom + heightToScrew]) rotate([90,0,0]) placeCornerScrewHolder();
       
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
    if(sides == [1,0]){
            color("red") translate([ -( (lcdHeight/2) +((baseBoardThickness+1)/2) ),0,(lcdHeight/2)/2 - ( (baseBoardThickness+1) / 2)]) cube([baseBoardThickness+1,lcdWidth,lcdHeight/2],center=true);
        }
    if(sides == [0,1]){
        color("blue") translate([ (lcdHeight/2) +((baseBoardThickness+1)/2),0,(lcdHeight/2)/2 - ( (baseBoardThickness+1) / 2)]) cube([baseBoardThickness+1,lcdWidth,lcdHeight/2],center=true);
    }
}


// cut center of the base for screen
module baseWithScreen(){
difference(){
// base (bottom cover with added length)
makeTopBottomCover(top=0);
//base();
// groove for screen
rotate([0,0,90]) cube([screenWidth,screenHeight,(baseBoardThickness+1)],center=true);
}
}

// 40.5;
// 8.35
// 4.2

//- ( (lcdWidth/2)-(screenWidth/2) + (5.88/2) )
//color("red") translate([(lcdHeight/2) , -screenWidth/2 + (8.35/2) + 40.5/2 ,0]) 

module makePowerSlot(){
slotWidth = 8.35;
slotHeight = 4.2;
slotDepth = baseBoardThickness+1;
slotToEdge = 40.5;
color("red") translate([(lcdHeight/2) - ((baseBoardThickness+1)/2) + slotDepth,-screenWidth/2 + (slotWidth/2) + slotToEdge/2 + (5),(slotDepth/2) + (squareThickness/2) + heightToScrew]) cube([slotDepth+3,slotWidth+3,slotHeight+3],center=true);
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
support_height=13;
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
union(){
        color("red") translate([0, (lcdWidth/2) + ((baseBoardThickness+1)/2) ,((lcdHeight/4)/2) + ((baseBoardThickness+1) /2) + 10]) cube([ (lcdHeight+((baseBoardThickness+1)*30)) / 4 + 15,(baseBoardThickness+1),lcdHeight/4],center=true);
translate([0, (lcdWidth/2) + ((baseBoardThickness+1)/2) ,((lcdHeight/4)/2) + ((baseBoardThickness+1) /2) + 24])cube([5,(baseBoardThickness+1),5],center=true);

}
}
// putting together two side walls and the base
module mainPiece(){
difference(){
union(){
  baseWithScreen();
  
  makeSideWall();
  //makeRearendWall(1);
  
  difference(){
  makeSideWall([0,1]);
  makePowerSlot();
  }
    difference(){
        #makeRearendWall(1);
        tempSlot();
//        color("red") translate([0, (lcdWidth/2) + ((baseBoardThickness+1)/2) ,((lcdHeight/4)/2) + ((baseBoardThickness+1) /2) + 10]) cube([ (lcdHeight+((baseBoardThickness+1)*30)) / 4 + 15,(baseBoardThickness+1),lcdHeight/4],center=true);
  }
  
  //makeTriangleWidget();
  makeScrewHolders();
  // move the sensor space to the rear-end
  //translate([0,(extraBoardHeight/2) + (lcdWidth/2) + (baseBoardThickness+1),0]) rotate([0,0,90]) sensorSpace();
}
//#fourVerticalPoles(topPoles=true, head=false);
//#fourVerticalPoles(topPoles=false);
}

}
//mainPiece();


module fontEndWall(){
difference(){

#makeRearendWall(0);
    
//union(){
//#fourVerticalPoles(topPoles=true);    
//#fourVerticalPoles(topPoles=false);
//}
    
    translate([-toTranslateX,-toTranslateYBottom,toTranslateZBottom + heightToScrew]) color("blue") rotate([90,0,0]) cylinder(r=screwInnerRadius,h=depth/2+20,center=true);

translate([toTranslateX,-toTranslateYBottom,toTranslateZBottom + heightToScrew]) color("blue") rotate([90,0,0]) cylinder(r=screwInnerRadius,h=depth/2+20,center=true);
}


}

//fontEndWall();

module topCover(){
    

//placeCornerScrewHolder(x=toTranslateX,y=-toTranslateY,z=toTranslateZ);
//placeCornerScrewHolder(x=-toTranslateX,y=-toTranslateY,z=toTranslateZ);        
// 
//placeCornerScrewHolder(x=toTranslateX,y=toTranslateY,z=toTranslateZ);
//placeCornerScrewHolder(x=-toTranslateX,y=toTranslateY,z=toTranslateZ); 

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

//******************************************//
//******************************************//
/*
    ****** PRINT EACH PART SEPARATELY ******
*/
//******************************************//
//******************************************//



mainPiece();
fontEndWall();

union(){
tempSupport();
topCover();
}


