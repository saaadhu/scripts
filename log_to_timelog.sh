#!/bin/sh
# Drop this /usr/lib/systemd/system-sleep
case $1/$2 in
  pre/*)
    echo -n `date` >> /scratch/timelog && echo "    [Suspended]" >> /scratch/timelog
    ;;
  post/*)
    echo -n `date` >> /scratch/timelog && echo "    [Woke]" >> /scratch/timelog
    ;;
esac
