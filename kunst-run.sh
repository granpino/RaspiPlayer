#!/bin/bash
### BEGIN INIT INFO
# Provides:          kunst
# Required-Start:    $network $remote_fs
# Required-Stop:     $network $remote_fs
# Default-Start:     2 3 4 5
# Default-Stop:      0 1 6
# Short-Description: Start kunst
# Description:       album art retriever
### END INIT INFO


#kunst.sh


sudo kunst --music_dir /mnt/usbdrive/

