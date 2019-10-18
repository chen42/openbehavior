$fn=50;

// define global variables (measurments, unit = mm)
lcdWidth = 121.4;
lcdThickness = 7.91;
lcdHeight = 76.80;
baseBoardThickness = 3;


squareHeight=7.5;
squareWidth=7.5;
squareThickness=2.5;

screwInnerRadius = 2.56;
smallChipWidth = 19.18;
smallChipHeight = 33.32;

heightToScrew = 12.88;

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
        translate([0,-(((baseBoardThickness+1) /2)+(lcdWidth/2)),(lcdHeight/2)/2 - ((baseBoardThickness+1) /2) + ((baseBoardThickness+1) /2 )]) cube([lcdHeight+((baseBoardThickness+1)*2),baseBoardThickness+1,lcdHeight/2 - (baseBoardThickness+1) ],center=true);    
    }
}


// top cover
module makeTopBottomCover(top=true){
   if(top){
   translate([0,0,lcdHeight/2]) cube([lcdHeight+((baseBoardThickness+1) *2), (lcdWidth + ((baseBoardThickness+1) *2)) ,baseBoardThickness+1],center=true);    
   }
   
   if(!top){
       cube([lcdHeight+((baseBoardThickness+1) *2), (lcdWidth + ((baseBoardThickness+1) *2)) ,baseBoardThickness+1],center=true);
   }
   
}

cutoff1 = (lcdHeight/2) + (baseBoardThickness/2);
xTempVar = ( (lcdHeight/2) + (baseBoardThickness/2) ) + ( ( (lcdHeight+((baseBoardThickness+1)*2)) )/2 - (cutoff1+ (baseBoardThickness/2) ) ) /2;
yTempVar = -( (lcdWidth/2) + ((baseBoardThickness/2)) + ( ((baseBoardThickness+1)/2) - (baseBoardThickness/2) ) );
zTempVar = 40;

module fourVerticalPoles(topPoles=true, head=true){
    
if(topPoles){

if(head){
color("red") translate([xTempVar, yTempVar, zTempVar]) cylinder(r=baseBoardThickness/2,h=20,center=true);
color("red") translate([-xTempVar, yTempVar, zTempVar]) cylinder(r=baseBoardThickness/2,h=20,center=true);
}
else{
color("red") translate([xTempVar, -yTempVar, zTempVar]) cylinder(r=baseBoardThickness/2,h=20,center=true);
color("red") translate([-xTempVar, -yTempVar, zTempVar]) cylinder(r=baseBoardThickness/2,h=20,center=true);
}

}

if(!topPoles){
color("red") translate([xTempVar,yTempVar,0]) cylinder(r=baseBoardThickness/2,h=20,center=true);
color("red") translate([-xTempVar,yTempVar,0]) cylinder(r=baseBoardThickness/2,h=20,center=true);
}

}

//color("blue") cube([lcdHeight+((baseBoardThickness+1) *2), (lcdWidth + ((baseBoardThickness+1) *2)) ,baseBoardThickness+1],center=true);


module placeScrewHolder(x=(lcdHeight/2 - (squareWidth/2)) , y=(lcdWidth/2 - (squareHeight/2)) , z=((baseBoardThickness+1)/2) + (squareThickness/2) + heightToScrew) {
    translate([x,y,z])
    difference(){
            cube([squareWidth,squareHeight,squareThickness],center=true);
            color("blue") cylinder(r=screwInnerRadius,h=squareThickness,center=true);
    }
}

//placeScrewHolder(x=(lcdHeight/2 - (squareWidth/2)),y=(lcdWidth/2 - (squareHeight/2)),z=((baseBoardThickness+1)/2) + (squareThickness/2) + heightToScrew);

module makeScrewHolders(){
placeScrewHolder();

placeScrewHolder(x=-(lcdHeight/2 - (squareWidth/2)));

placeScrewHolder(y=-(lcdWidth/2 - (squareHeight/2)));

placeScrewHolder(x=-(lcdHeight/2 - (squareWidth/2)),y=-(lcdWidth/2 - (squareHeight/2)));

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


module makeSlots(){
   difference(){
       makeSideWall();
       color("blue") translate([ -(lcdHeight/2 + 1.5),0 , leftSideInputPortsHeightFromBase + (leftSideInputPortsHeight/2)-3]) cube([baseBoardThickness+1,leftSideInputPortsWidth+5,leftSideInputPortsHeight],center=true);
    
   }
}



//******************************************//

/*
    Following modules are used to print the individual pieces.
    Note that each individual module should be printed seperated.
*/

//******************************************//



// putting together two side walls and the base
module mainPiece(){
difference(){
union(){
  baseWithScreen();
  makeSideWall([0,1]);
  makeSideWall();
  makeRearendWall(1);
  makeScrewHolders();
  // move the sensor space to the rear-end
  translate([0,(extraBoardHeight/2) + (lcdWidth/2) + (baseBoardThickness+1),0]) rotate([0,0,90]) sensorSpace();
}
#fourVerticalPoles(topPoles=true, head=false);
#fourVerticalPoles(topPoles=false);
}

}

mainPiece();


module fontEndWall(){
difference(){

#makeRearendWall(0);
union(){
#fourVerticalPoles(topPoles=true);    
#fourVerticalPoles(topPoles=false);
}
}
}

fontEndWall();

module topCover(){
difference(){
    
makeTopBottomCover(top=true);

#fourVerticalPoles(topPoles=true,head=false);
#fourVerticalPoles(topPoels=true);    

}
}

topCover();


