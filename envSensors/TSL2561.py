#!/usr/bin/python

# Python library for the TSL2561 digital luminosity (light) sensors.
# Version 0

# This library is heavily based on the Arduino library for the TSL2561 digital luminosity (light) sensors.
# It is basically a simple translation from C++ to Python.
# The thread on the Adafruit forum helped a lot to do this.
# Thanks to static, huelke, pandring, adafruit_support_rick, scortier, bryand, csalty, lenos and of course to Adafruit
# Source for the Arduino library: https://github.com/adafruit/TSL2561-Arduino-Library
# Adafruit form thread:http://forums.adafruit.com/viewtopic.php?f=8&t=34922&sid=8336d566f2f03c25882aaf34c8a15a92

import time
from Adafruit_I2C import Adafruit_I2C

class Adafruit_TSL2561(Adafruit_I2C):
    TSL2561_VISIBLE           =2       # channel 0 - channel 1
    TSL2561_INFRARED          =1       # channel 1
    TSL2561_FULLSPECTRUM      =0       # channel 0

    # I2C address options
    TSL2561_ADDR_LOW          =0x29
    TSL2561_ADDR_FLOAT        =0x39    # Default address (pin left floating)
    TSL2561_ADDR_HIGH         =0x49

    # Lux calculations differ slightly for CS package
    TSL2561_PACKAGE_CS        =0
    TSL2561_PACKAGE_T_FN_CL   =1

    TSL2561_COMMAND_BIT       =0x80    # Must be 1
    TSL2561_CLEAR_BIT         =0x40    # Clears any pending interrupt (write 1 to clear)
    TSL2561_WORD_BIT          =0x20    # 1 = read/write word (rather than byte)
    TSL2561_BLOCK_BIT         =0x10    # 1 = using block read/write

    TSL2561_CONTROL_POWERON   =0x03
    TSL2561_CONTROL_POWEROFF  =0x00

    TSL2561_LUX_LUXSCALE      =14      # Scale by 2^14
    TSL2561_LUX_RATIOSCALE    =9       # Scale ratio by 2^9
    TSL2561_LUX_CHSCALE       =10      # Scale channel values by 2^10
    TSL2561_LUX_CHSCALE_TINT0 =0x7517  # 322/11 * 2^TSL2561_LUX_CHSCALE
    TSL2561_LUX_CHSCALE_TINT1 =0x0FE7  # 322/81 * 2^TSL2561_LUX_CHSCALE

    # T, FN and CL package values
    TSL2561_LUX_K1T           =0x0040  # 0.125 * 2^RATIO_SCALE
    TSL2561_LUX_B1T           =0x01f2  # 0.0304 * 2^LUX_SCALE
    TSL2561_LUX_M1T           =0x01be  # 0.0272 * 2^LUX_SCALE
    TSL2561_LUX_K2T           =0x0080  # 0.250 * 2^RATIO_SCALE
    TSL2561_LUX_B2T           =0x0214  # 0.0325 * 2^LUX_SCALE
    TSL2561_LUX_M2T           =0x02d1  # 0.0440 * 2^LUX_SCALE
    TSL2561_LUX_K3T           =0x00c0  # 0.375 * 2^RATIO_SCALE
    TSL2561_LUX_B3T           =0x023f  # 0.0351 * 2^LUX_SCALE
    TSL2561_LUX_M3T           =0x037b  # 0.0544 * 2^LUX_SCALE
    TSL2561_LUX_K4T           =0x0100  # 0.50 * 2^RATIO_SCALE
    TSL2561_LUX_B4T           =0x0270  # 0.0381 * 2^LUX_SCALE
    TSL2561_LUX_M4T           =0x03fe  # 0.0624 * 2^LUX_SCALE
    TSL2561_LUX_K5T           =0x0138  # 0.61 * 2^RATIO_SCALE
    TSL2561_LUX_B5T           =0x016f  # 0.0224 * 2^LUX_SCALE
    TSL2561_LUX_M5T           =0x01fc  # 0.0310 * 2^LUX_SCALE
    TSL2561_LUX_K6T           =0x019a  # 0.80 * 2^RATIO_SCALE
    TSL2561_LUX_B6T           =0x00d2  # 0.0128 * 2^LUX_SCALE
    TSL2561_LUX_M6T           =0x00fb  # 0.0153 * 2^LUX_SCALE
    TSL2561_LUX_K7T           =0x029a  # 1.3 * 2^RATIO_SCALE
    TSL2561_LUX_B7T           =0x0018  # 0.00146 * 2^LUX_SCALE
    TSL2561_LUX_M7T           =0x0012  # 0.00112 * 2^LUX_SCALE
    TSL2561_LUX_K8T           =0x029a  # 1.3 * 2^RATIO_SCALE
    TSL2561_LUX_B8T           =0x0000  # 0.000 * 2^LUX_SCALE
    TSL2561_LUX_M8T           =0x0000  # 0.000 * 2^LUX_SCALE
    
    # CS package values
    TSL2561_LUX_K1C           =0x0043  # 0.130 * 2^RATIO_SCALE
    TSL2561_LUX_B1C           =0x0204  # 0.0315 * 2^LUX_SCALE
    TSL2561_LUX_M1C           =0x01ad  # 0.0262 * 2^LUX_SCALE
    TSL2561_LUX_K2C           =0x0085  # 0.260 * 2^RATIO_SCALE
    TSL2561_LUX_B2C           =0x0228  # 0.0337 * 2^LUX_SCALE
    TSL2561_LUX_M2C           =0x02c1  # 0.0430 * 2^LUX_SCALE
    TSL2561_LUX_K3C           =0x00c8  # 0.390 * 2^RATIO_SCALE
    TSL2561_LUX_B3C           =0x0253  # 0.0363 * 2^LUX_SCALE
    TSL2561_LUX_M3C           =0x0363  # 0.0529 * 2^LUX_SCALE
    TSL2561_LUX_K4C           =0x010a  # 0.520 * 2^RATIO_SCALE
    TSL2561_LUX_B4C           =0x0282  # 0.0392 * 2^LUX_SCALE
    TSL2561_LUX_M4C           =0x03df  # 0.0605 * 2^LUX_SCALE
    TSL2561_LUX_K5C           =0x014d  # 0.65 * 2^RATIO_SCALE
    TSL2561_LUX_B5C           =0x0177  # 0.0229 * 2^LUX_SCALE
    TSL2561_LUX_M5C           =0x01dd  # 0.0291 * 2^LUX_SCALE
    TSL2561_LUX_K6C           =0x019a  # 0.80 * 2^RATIO_SCALE
    TSL2561_LUX_B6C           =0x0101  # 0.0157 * 2^LUX_SCALE
    TSL2561_LUX_M6C           =0x0127  # 0.0180 * 2^LUX_SCALE
    TSL2561_LUX_K7C           =0x029a  # 1.3 * 2^RATIO_SCALE
    TSL2561_LUX_B7C           =0x0037  # 0.00338 * 2^LUX_SCALE
    TSL2561_LUX_M7C           =0x002b  # 0.00260 * 2^LUX_SCALE
    TSL2561_LUX_K8C           =0x029a  # 1.3 * 2^RATIO_SCALE
    TSL2561_LUX_B8C           =0x0000  # 0.000 * 2^LUX_SCALE
    TSL2561_LUX_M8C           =0x0000  # 0.000 * 2^LUX_SCALE

    # Auto-gain thresholds
    TSL2561_AGC_THI_13MS      =4850    # Max value at Ti 13ms = 5047
    TSL2561_AGC_TLO_13MS      =100
    TSL2561_AGC_THI_101MS     =36000   # Max value at Ti 101ms = 37177
    TSL2561_AGC_TLO_101MS     =200
    TSL2561_AGC_THI_402MS     =63000   # Max value at Ti 402ms = 65535
    TSL2561_AGC_TLO_402MS     =500

    # Clipping thresholds
    TSL2561_CLIPPING_13MS     =4900
    TSL2561_CLIPPING_101MS    =37000
    TSL2561_CLIPPING_402MS    =65000

    TSL2561_REGISTER_CONTROL          = 0x00
    TSL2561_REGISTER_TIMING           = 0x01
    TSL2561_REGISTER_THRESHHOLDL_LOW  = 0x02
    TSL2561_REGISTER_THRESHHOLDL_HIGH = 0x03
    TSL2561_REGISTER_THRESHHOLDH_LOW  = 0x04
    TSL2561_REGISTER_THRESHHOLDH_HIGH = 0x05
    TSL2561_REGISTER_INTERRUPT        = 0x06
    TSL2561_REGISTER_CRC              = 0x08
    TSL2561_REGISTER_ID               = 0x0A
    TSL2561_REGISTER_CHAN0_LOW        = 0x0C
    TSL2561_REGISTER_CHAN0_HIGH       = 0x0D
    TSL2561_REGISTER_CHAN1_LOW        = 0x0E
    TSL2561_REGISTER_CHAN1_HIGH       = 0x0F
    
    TSL2561_INTEGRATIONTIME_13MS      = 0x00    # 13.7ms
    TSL2561_INTEGRATIONTIME_101MS     = 0x01    # 101ms
    TSL2561_INTEGRATIONTIME_402MS     = 0x02    # 402ms
    
    TSL2561_GAIN_1X                   = 0x00    # No gain
    TSL2561_GAIN_16X                  = 0x10    # 16x gain
    
    
    

#**************************************************************************/
#    Writes a register and an 8 bit value over I2C
#**************************************************************************/
    def write8 (self, reg, value):
        if (self._debug == True): print "write8"
        self._i2c.write8(reg, value)
        if (self._debug == True): print "write8_end"

#**************************************************************************/
#    Reads an 8 bit value over I2C
#**************************************************************************/
    def read8(self, reg):
        if (self._debug == True): print "read8"
        return self._i2c.readS8(reg)
        if (self._debug == True): print "read8_end"

#**************************************************************************/
#   Reads a 16 bit values over I2C
#**************************************************************************/
    def read16(self, reg):
        if (self._debug == True): print "read16"
        return self._i2c.readS16(reg)
        if (self._debug == True): print "read16_end"

#**************************************************************************/
#    Enables the device
#**************************************************************************/
    def enable(self):
        if (self._debug == True): print "enable"
        # Enable the device by setting the control bit to 0x03 */
        self._i2c.write8(self.TSL2561_COMMAND_BIT | self.TSL2561_REGISTER_CONTROL, self.TSL2561_CONTROL_POWERON)
        if (self._debug == True): print "enable_end"

#**************************************************************************/
#   Disables the device (putting it in lower power sleep mode)
#**************************************************************************/
    def disable(self):
        if (self._debug == True): print "disable"
        # Turn the device off to save power */
        self._i2c.write8(self.TSL2561_COMMAND_BIT | self.TSL2561_REGISTER_CONTROL, self.TSL2561_CONTROL_POWEROFF)
        if (self._debug == True): print "disable_end"

#**************************************************************************/
#   Private function to read luminosity on both channels
#**************************************************************************/
    def getData (self):
        if (self._debug == True): print "getData"
        # Enable the device by setting the control bit to 0x03 */
        self.enable();

        # Wait x ms for ADC to complete */
        if self._tsl2561IntegrationTime == self.TSL2561_INTEGRATIONTIME_13MS:
            time.sleep(0.014)
        elif self._tsl2561IntegrationTime == self.TSL2561_INTEGRATIONTIME_101MS:
          time.sleep(0.102)
        else:
          time.sleep(0.403)


        # Reads a two byte value from channel 0 (visible + infrared) */
        self._broadband = self.read16(self.TSL2561_COMMAND_BIT | self.TSL2561_WORD_BIT | self.TSL2561_REGISTER_CHAN0_LOW);

        # Reads a two byte value from channel 1 (infrared) */
        self._ir = self.read16(self.TSL2561_COMMAND_BIT | self.TSL2561_WORD_BIT | self.TSL2561_REGISTER_CHAN1_LOW);

        # Turn the device off to save power */
        self.disable();
        if (self._debug == True): print "getData_end"

#**************************************************************************/
#   Constructor
#**************************************************************************/
    def __init__(self, addr=0x39, debug=False):
        self._debug = debug
        if (self._debug == True): print "__init__"
        self._addr = addr
        self._tsl2561Initialised = False
        self._tsl2561AutoGain = False
        self._tsl2561IntegrationTime = self.TSL2561_INTEGRATIONTIME_13MS
        self._tsl2561Gain = self.TSL2561_GAIN_1X
        self._i2c = Adafruit_I2C(self._addr)
        self._luminosity = 0
        self._broadband = 0
        self._ir = 0
        if (self._debug == True): print "__init___end"

#**************************************************************************/
#   Initializes I2C and configures the sensor (call this function before
#   doing anything else)
#**************************************************************************/
    def begin(self):
        if (self._debug == True): print "begin"
        # Make sure we're actually connected */
        x = self.read8(self.TSL2561_REGISTER_ID);
        if not(x & 0x0A):
            return False
        self._tsl2561Initialised = True

        # Set default integration time and gain */
        self.setIntegrationTime(self._tsl2561IntegrationTime)
        self.setGain(self._tsl2561Gain)

        # Note: by default, the device is in power down mode on bootup */
        self.disable()
        if (self._debug == True): print "begin_end"

        return True
 
#**************************************************************************/
#   Enables or disables the auto-gain settings when reading
#   data from the sensor
#**************************************************************************/
    def enableAutoGain(self, enable):
        if (self._debug == True): print "enableAutoGain"
        self._tsl2561AutoGain = enable if True else False
        if (enable == True):
            self._tsl2561AutoGain = enable
        else:
            self._tsl2561AutoGain = False
        if (self._debug == True): print "enableAutoGain_end"

#**************************************************************************/
#   Sets the integration time for the TSL2561
#**************************************************************************/
    def setIntegrationTime(self, time):
        if (self._debug == True): print "setIntegrationTime"
        if (not self._tsl2561Initialised):
            self.begin()

        # Enable the device by setting the control bit to 0x03 */
        self.enable();

        # Update the timing register */
        self.write8(self.TSL2561_COMMAND_BIT | self.TSL2561_REGISTER_TIMING, time | self._tsl2561Gain)

        # Update value placeholders */
        self._tsl2561IntegrationTime = time

        # Turn the device off to save power */
        self.disable()
        if (self._debug == True): print "setIntegrationTime_end"
 
#**************************************************************************/
#    Adjusts the gain on the TSL2561 (adjusts the sensitivity to light)
#**************************************************************************/
    def setGain(self, gain):
        if (self._debug == True): print "setGain"
        if (not self._tsl2561Initialised):
            begin()

        # Enable the device by setting the control bit to 0x03 */
        self.enable()

        # Update the timing register */
        self.write8(self.TSL2561_COMMAND_BIT | self.TSL2561_REGISTER_TIMING, self._tsl2561IntegrationTime | gain)

        # Update value placeholders */
        self._tsl2561Gain = gain

        # Turn the device off to save power */
        self.disable()
        if (self._debug == True): print "setGain_end"

#**************************************************************************/
#   Gets the broadband (mixed lighting) and IR only values from
#   the TSL2561, adjusting gain if auto-gain is enabled
#**************************************************************************/
    def getLuminosity (self):
        if (self._debug == True): print "getLuminosity"
        valid = False

        if (not self._tsl2561Initialised):
             self.begin()

        # If Auto gain disabled get a single reading and continue */
        if(not self._tsl2561AutoGain):
            self.getData()
            return

        # Read data until we find a valid range */
        _agcCheck = False
        while (not valid):
            _it = self._tsl2561IntegrationTime;

            # Get the hi/low threshold for the current integration time */
            if _it==self.TSL2561_INTEGRATIONTIME_13MS:
                _hi = self.TSL2561_AGC_THI_13MS
                _lo = self.TSL2561_AGC_TLO_13MS
            elif _it==self.TSL2561_INTEGRATIONTIME_101MS:
                _hi = self.TSL2561_AGC_THI_101MS
                _lo = self.TSL2561_AGC_TLO_101MS
            else:
                _hi = self.TSL2561_AGC_THI_402MS
                _lo = self.TSL2561_AGC_TLO_402MS

            self.getData()

            # Run an auto-gain check if we haven't already done so ... */
            if (not _agcCheck):
                if ((self._broadband < _lo) and (self._tsl2561Gain == self.TSL2561_GAIN_1X)):
                    # Increase the gain and try again */
                    self.setGain(self.TSL2561_GAIN_16X)
                    # Drop the previous conversion results */
                    self.getData()
                    # Set a flag to indicate we've adjusted the gain */
                    _agcCheck = True
                elif ((self._broadband > _hi) and (self._tsl2561Gain == self.TSL2561_GAIN_16X)):
                    # Drop gain to 1x and try again */
                    self.setGain(self.TSL2561_GAIN_1X)
                    # Drop the previous conversion results */
                    self.getData()
                    # Set a flag to indicate we've adjusted the gain */
                    _agcCheck = True
                else:
                    # Nothing to look at here, keep moving ....
                    # Reading is either valid, or we're already at the chips limits */
                    valid = True
            else:
                # If we've already adjusted the gain once, just return the new results.
                # This avoids endless loops where a value is at one extreme pre-gain,
                # and the the other extreme post-gain */
                valid = True
        if (self._debug == True): print "getLuminosity_end"
        
#**************************************************************************/
#    Converts the raw sensor values to the standard SI lux equivalent.
#    Returns 0 if the sensor is saturated and the values are unreliable.
#**************************************************************************/
    def calculateLux(self):
        if (self._debug == True): print "calculateLux"
        self.getLuminosity()
        # Make sure the sensor isn't saturated! */
        if (self._tsl2561IntegrationTime == self.TSL2561_INTEGRATIONTIME_13MS):
            clipThreshold = self.TSL2561_CLIPPING_13MS
        elif (self._tsl2561IntegrationTime == self.TSL2561_INTEGRATIONTIME_101MS):
            clipThreshold = self.TSL2561_CLIPPING_101MS
        else:
            clipThreshold = self.TSL2561_CLIPPING_402MS

        # Return 0 lux if the sensor is saturated */
        if ((self._broadband > clipThreshold) or (self._ir > clipThreshold)):
            return 0

        # Get the correct scale depending on the intergration time */
        if (self._tsl2561IntegrationTime ==self.TSL2561_INTEGRATIONTIME_13MS):
            chScale = self.TSL2561_LUX_CHSCALE_TINT0
        elif (self._tsl2561IntegrationTime ==self.TSL2561_INTEGRATIONTIME_101MS):
            chScale = self.TSL2561_LUX_CHSCALE_TINT1
        else:
            chScale = (1 << self.TSL2561_LUX_CHSCALE)

        # Scale for gain (1x or 16x) */
        if (not self._tsl2561Gain): 
            chScale = chScale << 4

        # Scale the channel values */
        channel0 = (self._broadband * chScale) >> self.TSL2561_LUX_CHSCALE
        channel1 = (self._ir * chScale) >> self.TSL2561_LUX_CHSCALE

        # Find the ratio of the channel values (Channel1/Channel0) */
        ratio1 = 0;
        if (channel0 != 0):
            ratio1 = (channel1 << (self.TSL2561_LUX_RATIOSCALE+1)) / channel0

        # round the ratio value */
        ratio = (ratio1 + 1) >> 1

        if (self.TSL2561_PACKAGE_CS == 1):
            if ((ratio >= 0) and (ratio <= self.TSL2561_LUX_K1C)):
                b=self.TSL2561_LUX_B1C
                m=self.TSL2561_LUX_M1C
            elif (ratio <= self.TSL2561_LUX_K2C):
                b=self.TSL2561_LUX_B2C
                m=self.TSL2561_LUX_M2C
            elif (ratio <= self.TSL2561_LUX_K3C):
                b=self.TSL2561_LUX_B3C
                m=self.TSL2561_LUX_M3C
            elif (ratio <= self.TSL2561_LUX_K4C):
                b=self.TSL2561_LUX_B4C
                m=self.TSL2561_LUX_M4C
            elif (ratio <= self.TSL2561_LUX_K5C):
                b=self.TSL2561_LUX_B5C
                m=self.TSL2561_LUX_M5C
            elif (ratio <= self.TSL2561_LUX_K6C):
                b=self.TSL2561_LUX_B6C
                m=self.TSL2561_LUX_M6C
            elif (ratio <= self.TSL2561_LUX_K7C):
                b=self.TSL2561_LUX_B7C
                m=self.TSL2561_LUX_M7C
            elif (ratio > self.TSL2561_LUX_K8C):
                b=self.TSL2561_LUX_B8C
                m=self.TSL2561_LUX_M8C
        elif (self.TSL2561_PACKAGE_T_FN_CL == 1):
            if ((ratio >= 0) and (ratio <= self.TSL2561_LUX_K1T)):
                b=self.TSL2561_LUX_B1T
                m=self.TSL2561_LUX_M1T
            elif (ratio <= self.TSL2561_LUX_K2T):
                b=self.TSL2561_LUX_B2T
                m=self.TSL2561_LUX_M2T
            elif (ratio <= self.TSL2561_LUX_K3T):
                b=self.TSL2561_LUX_B3T
                m=self.TSL2561_LUX_M3T
            elif (ratio <= self.TSL2561_LUX_K4T):
                b=self.TSL2561_LUX_B4T
                m=self.TSL2561_LUX_M4T
            elif (ratio <= self.TSL2561_LUX_K5T):
                b=self.TSL2561_LUX_B5T
                m=self.TSL2561_LUX_M5T
            elif (ratio <= self.TSL2561_LUX_K6T):
                b=self.TSL2561_LUX_B6T
                m=self.TSL2561_LUX_M6T
            elif (ratio <= self.TSL2561_LUX_K7T):
                b=self.TSL2561_LUX_B7T
                m=self.TSL2561_LUX_M7T
            elif (ratio > self.TSL2561_LUX_K8T):
                b=self.TSL2561_LUX_B8T
                m=self.TSL2561_LUX_M8T
        #endif

        temp = ((channel0 * b) - (channel1 * m))

        # Do not allow negative lux value */
        if (temp < 0): 
            temp = 0

        # Round lsb (2^(LUX_SCALE-1)) */
        temp += (1 << (self.TSL2561_LUX_LUXSCALE-1))

        # Strip off fractional portion */
        lux = temp >> self.TSL2561_LUX_LUXSCALE;

        # Signal I2C had no errors */
        if (self._debug == True): print "calculateLux_end"
        return lux

'''
#**************************************************************************/
#   Gets the most recent sensor event
#**************************************************************************/
void Adafruit_TSL2561::getEvent(sensors_event_t *event)
{
  uint16_t broadband, ir;
  
  # Clear the event */
  memset(event, 0, sizeof(sensors_event_t));
  
  event->version   = sizeof(sensors_event_t);
  event->sensor_id = _tsl2561SensorID;
  event->type      = SENSOR_TYPE_LIGHT;
  event->timestamp = 0;

  # Calculate the actual lux value */
  getLuminosity(&broadband, &ir);
  event->light = calculateLux(broadband, ir);
}

#**************************************************************************/
#   Gets the sensor_t data
#**************************************************************************/
void Adafruit_TSL2561::getSensor(sensor_t *sensor)
{
  # Clear the sensor_t object */
  memset(sensor, 0, sizeof(sensor_t));

  # Insert the sensor name in the fixed length char array */
  strncpy (sensor->name, "TSL2561", sizeof(sensor->name) - 1);
  sensor->name[sizeof(sensor->name)- 1] = 0;
  sensor->version     = 1;
  sensor->sensor_id   = _tsl2561SensorID;
  sensor->type        = SENSOR_TYPE_LIGHT;
  sensor->min_delay   = 0;
  sensor->max_value   = 17000.0;  /* Based on trial and error ... confirm! */
  sensor->min_value   = 0.0;
  sensor->resolution  = 1.0;
}
'''

#LightSensor = Adafruit_TSL2561()
#LightSensor.enableAutoGain(True)
#while True:
#    print LightSensor.calculateLux(), " Lux"
    
