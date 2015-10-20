#!/bin/sh

# obtained the script from 
#https://nowhere.dk/articles/installing-and-running-copy-com-agent-on-a-headless-ubuntudebian-linux
#place in /etc/init.d

CC='/home/pi/copy/CopyConsole'
HOME='/home/pi/'
RUN_AS='pi'

start() {
echo "Starting CopyConsole..."
if [ -x $CC ]; then
start-stop-daemon -b -o -c $RUN_AS -S -u $RUN_AS -x $CC -- -daemon
fi
}

stop() {
echo "Stopping CopyConsole..."
if [ -x $CC ]; then
start-stop-daemon -o -c $RUN_AS -K -u $RUN_AS -x $CC
fi
}

status() {
dbpid=`pgrep -u $RUN_AS CopyConsole`
if [ -z $dbpid ] ; then
echo "CopyConsole for user $RUN_AS: not running."
else
echo "CopyConsole for user $RUN_AS: running (pid $dbpid)"
fi
}

case "$1" in

start)
start
;;
stop)
stop
;;
restart|reload|force-reload)
stop
start
;;
status)
status
;;
*)
echo "Usage: /etc/init.d/copy {start|stop|reload|force-reload|restart|status}"
exit 1

esac

exit 0

