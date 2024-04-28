#!/bin/sh -e

HERE=$(dirname $(readlink -f $0))
checkscript=$(readlink -f $HERE/check-urls.py)
logfile=$(readlink -f $HERE/logfile.txt)

$checkscript 2>&1 > $logfile

exit 0
