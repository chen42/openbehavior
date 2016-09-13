# Assembling the operant licking device

## 3D printed frame
The frame is printed in two parts and put together using Krazy glue. Because of its size, the results are much better if you print it on a heated platform. You can also printed it as a single piece, but you need to enable 'supports' and clean them up afterwards. 

![] (images/frame0.jpg)

## Switch Board
The switches are used to provide bidirectional manually control of the syringe. 
The board also has two LEDs. The green LED indicates motion events and the red LED indicates licking events. The resisters are  100 ohm. 
The two holes are used for attaching the board to the top cover of the 3D printed frame.
![] (images/switchBoardFront.jpg)

The switch board also provides gound and 5V power to several boards (RFID reader, real time clock, touch sensor).  
![] (images/switchBoardBack.jpg)

The back side of the switch board with wires added. The blue and white wires are for the two switches. The yellow and green wires are for the LEDs.
![] (SwitchBoardBack2.jpg)

## RFID Reader 

Extend the length of the RFID antenna by soldering two segments of wires (approximately 12 inches) between the antenna loop  and the connector. 

![] (images/RFID_antenna.jpg)

Insert the antenna loop into the 3D printed frame (black) and close the gap in the frame with the handle (red).

![] (images/RFID_antenna2.jpg)

Tape the handle and the frame together.

![] (images/RFID_antenna3.jpg)

The RFID board is fixed on the top of the frame by using connection pins. Insert pin headers into the groove in the frame. Glue it.

![] (images/RFID_board1.jpg)
Insert the RFID board.

![] (images/RFID_board2.jpg)

## LCD
The LCD needs a 10 K ohm  potentiometer. Bend the wires as shown. 
![] (images/LCD1.jpg)
Solder it to the LDC. The middle wire of the potentiometer is connected to the 3rd pin of the LCD.  The other two wires are connected to pins 1 and 2. 
![] (images/LCD2.jpg)

## Power

Connect two wires to a micro USB connector.

![] (images/microUSB.jpg)

Cut the connector off a 12 V AC-DC converter (2 Amp). Connect the wires to the input side of a step down voltage converter. Connect the two wires from the micro USB connector to the output end (labeled on the back side of the board). Add two wires with female pins heads to the output side. These have 12 V and are connected to the step motor controller.  

![] (images/voltageConverter.jpg)

## Syringe pump

3D printed parts of the syringe pump.
![] (images/syringePumpPrintedParts.jpg)

The step motor controller needs to have two wires added. 
![] (images/stepMotorBoardBack.jpg)

Extend the length of step motor connection wires to about 30 inch. Add female connection pins to the end of each wire. 

![] (images/stepMotorWires.jpg)

A thin piece of copper is added to make it easier to fasten the threaded rod to the coupler .

![] (images/threadedRod.jpg)

The step motor is connected to a threaded rod via a coupler. 

![] (images/stepMotorShaft.jpg)

The fully assembled syringe pump.

![] (images/SyringePumpAssembled.jpg)

