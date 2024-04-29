#!/bin/sh -e

HERE=$(dirname $(readlink -f $0))
checkscript=$(readlink -f $HERE/check-urls.py)
logfile=$(readlink -f $HERE/logfile.txt)

# Leave a timestamp
touch $logfile

(
$checkscript | sendteams.py -t "URL Checker" 2>&1 
) | tee -a $logfile

exit 0
