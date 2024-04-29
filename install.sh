#!/bin/sh -e

HERE=$(dirname $(readlink -f $0))
cronscript=$(readlink -f $HERE/check-urls-and-report.sh)

tmpfile=$(mktemp)
finish() {
	rm -f $tmpfile
}
trap finish EXIT

crontab -l > $tmpfile || true

if grep -q $cronscript $tmpfile; then
	echo "Cronjob is already installed"
	exit 0
fi

echo "@hourly $cronscript" >> $tmpfile

echo "Installing cronjob"
crontab $tmpfile

exit 0
