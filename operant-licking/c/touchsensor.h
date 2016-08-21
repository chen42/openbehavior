/*
 * Header for interfacing with MPR121 capacitive touch sensor IC
 * 
 */
 #ifndef TOUCHSENSOR_H_
 #define TOUCHSENSOR_H_
 
 // Register addresses
 #define MPR121_I2CADDR_DEFAULT  0x5A
#define MPR121_TOUCHSTATUS_L    0x00
#define MPR121_TOUCHSTATUS_H    0x01
#define MPR121_FILTDATA_0L      0x04
#define MPR121_FILTDATA_0H      0x05
#define MPR121_BASELINE_0       0x1E
#define MPR121_MHDR             0x2B
#define MPR121_NHDR             0x2C
#define MPR121_NCLR             0x2D
#define MPR121_FDLR             0x2E
#define MPR121_MHDF             0x2F
#define MPR121_NHDF             0x30
#define MPR121_NCLF             0x31
#define MPR121_FDLF             0x32
#define MPR121_NHDT             0x33
#define MPR121_NCLT             0x34
#define MPR121_FDLT             0x35
#define MPR121_TOUCHTH_0        0x41
#define MPR121_RELEASETH_0      0x42
#define MPR121_DEBOUNCE         0x5B
#define MPR121_CONFIG1          0x5C
#define MPR121_CONFIG2          0x5D
#define MPR121_CHARGECURR_0     0x5F
#define MPR121_CHARGETIME_1     0x6C
#define MPR121_ECR              0x5E
#define MPR121_AUTOCONFIG0      0x7B
#define MPR121_AUTOCONFIG1      0x7C
#define MPR121_UPLIMIT          0x7D
#define MPR121_LOWLIMIT         0x7E
#define MPR121_TARGETLIMIT      0x7F
#define MPR121_GPIODIR          0x76
#define MPR121_GPIOEN           0x77
#define MPR121_GPIOSET          0x78
#define MPR121_GPIOCLR          0x79
#define MPR121_GPIOTOGGLE       0x7A
#define MPR121_SOFTRESET        0x80
 
 
 
 #endif	// end of touchsensor.h
