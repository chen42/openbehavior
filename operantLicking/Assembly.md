# Assembling the operant licking device

## 3D printed frame
The frame is printed in two parts and put together using superglue. Because of its size, the results are much better if you print it on a heated platform. You can also print it as a single piece, but you need to enable 'supports' and remove them afterwards. 
![] (images/frame0.jpg)


Use sand paper to clean a small area of a spout. Then older a segment of solid core hookup wire to a spout with the help of one drop of stainless steel Flux (see parts list).  
![] (images/spout.jpg)

Solder one 100 ohm resister to a 5 mm LED (clear). Cover it with a short segment of heat shrink tubing.  
![] (images/cuelight.jpg)

Insert the LED into the cue light slot. Fix it in place using the small piece.  
Add a hex nut to the small opening on the spout holder. Use a thumbscrew to hold the spout (not shown) in place.
![] (images/cuelight2.jpg)

## Switch Board
The switches are used to provide bidirectional manual control of the syringe. 
The board also has two LEDs. The green LED indicates motion events and the red LED indicates licking events. The resistors are 100 ohm. 
The two holes are used for attaching the board to the top cover of the 3D printed frame.
![] (images/switchBoardFront.jpg)

The switch board also provides ground and 5V power to several boards (RFID reader, real time clock, touch sensor).  
![] (images/switchBoardBack.jpg)

The back side of the switch board with wires added. The blue and white wires are for the two switches. The yellow and green wires are for the LEDs. Solid core hook-up wired were used here but soldered header pins also work, as shown in the assembled model.  
![] (images/SwitchBoardBack2.jpg)

## RFID Reader 

Extend the length of the RFID antenna by soldering two segments of wires (approximately 12 inches) between the antenna loop  and the connector. 

![] (images/RFID_antenna.jpg)

Place the antenna loop next to the 3D printed handle, tape the wire to the handle. Then insert the antenna loop into the 3D printed frame (below). 

![] (images/RFID_antenna2.jpg)

Tape the handle and the frame together.

![] (images/RFID_antenna3.jpg)

The RFID board is fixed on top of the frame by using connection pins. Insert pin headers into the openings in the frame. Glue it.

![] (images/RFID_board1.jpg)
Insert the RFID board.

![] (images/RFID_board2.jpg)

Push three pins out of the header and use the remaining to fasten the RFID board in place. Connect the RFID antenna.
![] (images/rfid2.jpg)

# Motion Sensor
Bend the three pins on the motion sensor one by one to 90 degrees. Use two screws to hold the sensor on the frame.
![] (images/motion_sensor.jpg)

## LCD
The LCD needs a 10 K ohm potentiometer. Bend the wires as shown. 
![] (images/LCD1.jpg)
Solder it to the LDC. The middle wire of the potentiometer is connected to the 3rd pin of the LCD.  The other two wires are connected to pins 1 and 2. 
![] (images/LCD2.jpg)

Connect the LCD to the RPi. Note you can use seven ribbon pins because the other end of the pins are next to each other on the RPi. You can adjust the potentiometer to obtain optimal contrast.   

![] (images/LCD_connections.jpg)


## Power

Connect two wires to a micro USB connector.

![] (images/microUSB.jpg)

Cut the connector off a 12 V AC-DC converter (2 Amp). Connect the wires to the input side of a step down voltage converter. Connect the two wires from the micro USB connector to the output end (labeled on the back side of the board). Add two wires with female pins heads to the output side. These have 12 V and are connected to the stepper motor controller.  

![] (images/voltageConverter.jpg)

## Syringe pump

Insert a ball bearing into the 3D printed syringe end. 
![] (images/syringEnd.jpg)

Insert two linear bearings into the 3D printed syringe carrier. The syringe carrier must be printed precisely so that the linear bearing fit tightly alone its long axis but still has a little room to move in the other two dimensions. 

![] (images/syringCarrier.jpg)

The step motor controller needs to have two wires added. One connects ENABLE and GROUND, the other connects VDD and REST. 

![] (images/stepMotorBoardBack.jpg)

Extend the length of step motor connection wires to about 30 inches. Add female connection pins to the end of each wire. 

![] (images/stepMotorWires.jpg)

A thin piece of copper is added to make it easier to fasten the threaded rod to the coupler .

![] (images/threadedRod.jpg)

The stepper motor is connected to a threaded rod via a coupler. 

![] (images/stepMotorShaft.jpg)

The fully assembled syringe pump.  (The stainless steel rods were cut into 5.5 inch segments.)

![] (images/syringPumbAssembled.jpg)


## Final assembly

Print out a [RPi pin number label] (../RPI.PinLables.pdf). Cut the middle grey area and put it around the pins on the RPi to help you identify the pins. Connect the parts following  the [ wiring table]  (wiring_tables.ods)
![] (images/Rpi_pins.jpg)

All wires are connected.
![] (images/wires.jpg)

The fully assembled device. The RFID antenna can be placed on its holder on the right side.  The spouts can be disconnected for cleaning purpose. The LCD shows the following info:

*B07S14*: Box 7, session 14

*26A1*: the last four characters of the RFID

*54Le*: 54 minutes left

*a1i1r0vr10*: Active lick = 1, inactive lick = 1, reward = 0, Variable ratio 10 


![] (images/assembled.jpg)

A syringe is loaded in the pump. A rubber band is used to hold the syringe in place.  The pump can be placed on top of a rat cage.  The rest of the device can be placed inside the cage. Both spouts are connected. A PE tubing directs the liquid in the syringe to the active spout. 

![] (images/syrngeLoaded.jpg)

The entire assembled device can be placed in the rat cage. A filtered cover  can be placed on the top (not shown). 
![] (images/inRatCage.jpg)

