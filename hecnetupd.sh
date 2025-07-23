#!/bin/bash

# --
# hecnet-nodes-for-pydecnet.sh
# grabs HECnet node list from MIM and produces node names configuration
# file for DECnet/Python
#
# Tested under GNU bash, version 5.0.3(1)-release (arm-unknown-linux-gnueabihf)
#
# Author: Supratim Sanyal - http://tuklusan.decsystem.org
# License: Public domain under Beerware License, Rev 42.
# --

OUTFILE="/home/yourusername/.local/bin/nodenames.conf"
TMPFILE="/tmp/mimnodeslist.txt"

if ! wget -O ${TMPFILE} http://mim.stupi.net/hecnod; then
        echo "$0: error - wget failed"
        exit 1
fi

echo "# HECnet Node List: `date` generated on `hostname`" > ${OUTFILE}
echo "node 1.13  MIM" >> ${OUTFILE}

FOO=`cat ${TMPFILE} | dos2unix | egrep "^[0-9]" | cut -f 1-2 -d " " | sed -re 's/^/node /' | sed -re 's/[(]/ /' | sed -re 's/[)]//' | sed -re 's/Reachable//'`

echo "${FOO}" | while read -r LINE ; do
        if [[ ${LINE} == "node "[0-9]*"  "* ]]; then
                echo "${LINE}" >> ${OUTFILE}
        else
                echo "SKIPPED ${LINE}"
        fi
done

echo "$0: Written ${OUTFILE}"
exit 0