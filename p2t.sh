#!/usr/bin/env bash
DEBUG=${DEBUG-}
bsn=$(basename $1 .pdf)
$DEBUG pdftohtml -skipinvisible  $1 $bsn.htmldir
$DEBUG python $(dirname "${BASH_SOURCE[0]}")/p2t.py -o $bsn.txt $bsn.htmldir/page*.html
if [[ "$SAY" != '' ]]; then
	say -o $bsn.m4a -f $bsn.txt
fi
