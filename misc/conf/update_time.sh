# lock in time

#!/bin/sh

TZ='ZONE=Asia/Shanghai'
NTPSERVER='192.168.1.61'
CLOCK_FILE='/etc/sysconfig/clock'

#step pre: update time with ntp server
echo "Update time with NTP server: $NTPSERVER"
`ntpdate $NTPSERVER`

#step 1: change timezone
echo "Change timezone to: $TZ"
echo $TZ > $CLOCK_FILE

#step 2: sync hwclock & clock
echo "SYNC clock with hw clock"
`hwclock --systohc`

#step 3: clear etc/localtime, link to new zone time
echo "Update local time clock"
`rm -rf /etc/localtime` >/dev/null 2>&1
`ln -sf /usr/share/zoneinfo/Asia/Shanghai /etc/localtime` >/dev/null 2>&1

# Show time
echo "Now time is:  "`date`
