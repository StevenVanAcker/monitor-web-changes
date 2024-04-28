#!/bin/sh -e

HERE=$(dirname $(readlink -f $0))
checkscript=$(readlink -f $HERE/check-urls.py)
logfile=$(readlink -f $HERE/logfile.txt)

(
$checkscript | sendteams.py -t "URL Checker" 2>&1 
) | tee -a $logfile

exit 0
