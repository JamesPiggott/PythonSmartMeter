#! /bin/sh

### BEGIN INIT INFO
# Provides:          SmartMeterScript
# Required-Start:    $remote_fs $syslog
# Required-Stop:     $remote_fs $syslog
# Default-Start:     2 3 4 5
# Default-Stop:      0 1 6
# Short-Description: This script starts the smart meter reading script
# Description:       This script starts the smart meter reading script
### END INIT INFO
 
case "$1" in
  start)
    echo "Starting SmartMeter"
    # Start the application
    python /home/debian/ebalance/smart/SmartMeterScript.py &
    ;;
  stop)
    echo "Stopping SmartMeter"
    # Kill the application
    kill $(ps aux | grep 'python /home/debian/ebalance/smart/SmartMeterScript.py' | awk '{print $2}') &
    ;;
  *)
    echo "Usage: /etc/init.d/SmartMeter.sh {start|stop}"
    exit 1
    ;;
esac
 
exit 0

 
