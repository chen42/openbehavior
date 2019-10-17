$fn=50;
lcdWidth = 121.4;
lcdThickness = 7.91;
lcdHeight = 76.80;
baseBoardThickness = 4;


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
    if(head ==  1){
        translate([0,((baseBoardThickness+1) /2)+(lcdWidth/2),(lcdHeight/2)/2 - ((baseBoardThickness+1) /2)]) cube([lcdHeight+((baseBoardThickness+1)*2),baseBoardThickness+1,lcdHeight/2],center=true);    
    }
    
    if(head == 0){
        translate([0,-(((baseBoardThickness+1) /2)+(lcdWidth/2)),(lcdHeight/2)/2 - ((baseBoardThickness+1) /2)]) cube([lcdHeight+((baseBoardThickness+1)*2),baseBoardThickness+1,lcdHeight/2],center=true);    
    }
}


makeRearendWall(1);
//makeRearendWall(0);


module makeTopCover(){
   translate([0,0,lcdHeight/2]) cube([lcdHeight+((baseBoardThickness+1) *2), (lcdWidth + ((baseBoardThickness+1) *2)) ,baseBoardThickness+1],center=true);
}

//rotate([-45,0,0]) translate([(lcdHeight/2 +(baseBoardThickness/2)) + 0.5,-( (lcdWidth/2) + (baseBoardThickness/2)),0]) 


cutoff1 = (lcdHeight/2) + (baseBoardThickness/2);
translate([( (lcdHeight/2) + (baseBoardThickness/2) ) + ( ( (lcdHeight+((baseBoardThickness+1)*2)) )/2 - (cutoff1+ (baseBoardThickness/2) ) ) /2,-( (lcdWidth/2) + ((baseBoardThickness/2)) + ( ((baseBoardThickness+1)/2) - (baseBoardThickness/2) ) ), 40]) cylinder(r=baseBoardThickness/2,h=20,center=true);

union(){
  #makeRearendWall(0);
  #makeTopCover();
}



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



module makeChipSlot(){
cube([smallChipWidth+1.3,smallChipHeight+1.3,smallChipThickness],center=true);
    
//difference(){
//cube([smallChipWidth+1.3,smallChipHeight+1.3,smallChipThickness],center=true);
//color("blue") translate([smallChipWidth/2 - smallChipHoleRadius,smallChipHeight/2 - smallChipHoleRadius,-(1.5 - (smallChipThickness/2))]) cylinder(r=smallChipHoleRadius,h=smallChipThickness,center=true);
//color("blue") translate([smallChipWidth/2 - smallChipHoleRadius, -(smallChipHeight/2 - smallChipHoleRadius),-(1.5 - (smallChipThickness/2))]) cylinder(r=smallChipHoleRadius,h=smallChipThickness,center=true);
//}
}

h1 = (baseBoardThickness+1) - (smallChipThickness);
//smallChipThickness-(smallChipThickness/2);
translate([50,5, -(h1/2) - (smallChipThickness - ((baseBoardThickness+1) /2))]) cylinder(r=smallChipHoleRadius,h=h1,center=true);

module sensorSpace(){
    
difference(){
extraBaseExtensions();
    translate([0,(smallChipHeight/2 + ((baseBoardThickness+1)/2) ),((baseBoardThickness+1) /2)- (smallChipThickness/2)]) cube([smallChipWidth,smallChipHeight,smallChipThickness],center=true);
   translate([0,-(smallChipHeight/2 +((baseBoardThickness+1)/2)) ,((baseBoardThickness+1) /2) - (smallChipThickness/2)]) cube([smallChipWidth,smallChipHeight,smallChipThickness],center=true);
}
}

module makeSideWall(sides=[1,0]){ // sides default = [left=1,right=0]
    if(sides == [1,0]){
            color("red") translate([ -( (lcdHeight/2) +((baseBoardThickness+1)/2) ),0,(lcdHeight/2)/2 - ( (baseBoardThickness+1) / 2)]) cube([baseBoardThickness+1,lcdWidth,lcdHeight/2],center=true);
        }
    if(sides == [0,1]){
        color("blue") translate([ (lcdHeight/2) +((baseBoardThickness+1)/2),0,(lcdHeight/2)/2 - ( (baseBoardThickness+1) / 2)]) cube([baseBoardThickness+1,lcdWidth,lcdHeight/2],center=true);
    }
}


module baseWithScreen(){
difference(){
    base();
rotate([0,0,90]) cube([screenWidth,screenHeight,(baseBoardThickness+1)],center=true);
}
}


module makeSlots(){
    
   difference(){
       makeSideWall();
       color("blue") translate([ -(lcdHeight/2 + 1.5),0 , leftSideInputPortsHeightFromBase + (leftSideInputPortsHeight/2)-3]) cube([baseBoardThickness+1,leftSideInputPortsWidth+5,leftSideInputPortsHeight],center=true);
    
   }
}


//extraBaseExtensions();

translate([0,(extraBoardHeight/2) + (lcdWidth/2) + (baseBoardThickness+1),0]) rotate([0,0,90]) sensorSpace();
makeSideWall([0,1]);

makeSideWall();
//makeSlots();

baseWithScreen();

makeScrewHolders();