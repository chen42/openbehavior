init_rtc_device()
{
  [ -e /dev/rtc0 ] && return 0;

  # load i2c and RTC kernel modules
  modprobe i2c-dev
  modprobe rtc-ds1307

  # iterate over every i2c bus as we're supporting Raspberry Pi rev. 1 and 2
  # (different I2C busses on GPIO header!)
  for bus in $(ls -d /sys/bus/i2c/devices/i2c-*);
  do
    echo ds1307 0x68 >> $bus/new_device;
    if [ -e /dev/rtc0 ];
    then
      log_action_msg "RTC found on bus `cat $bus/name`";
      break; # RTC found, bail out of the loop
    else
      echo 0x68 >> $bus/delete_device
    fi
  done
}
