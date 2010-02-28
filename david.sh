#!/bin/bash
outdir=${TMPDIR:-$HOME/tmp}
specfile=$(grep -o '\<[a-zA-Z][-_+a-zA-Z0-9]*\.spec\>' <<<"$@" \
           || { echo "No spec file" 1>&2; exit 1; } | tail -n 1)
spectool -g -R -D "$@"
log="$outdir/rpmbuild-$specfile-$$.log"
if rpmbuild "$@" &>"$log"; then
  echo Logfile: "$log"
  sed 's/^Wrote: //;t;d' "$log"
#  rm "$log"
else
  cat "$log" 1>&2
  echo Logfile: "$log"
fi
