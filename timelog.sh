#! /bin/bash
LAST_WINDOW=
while :
do
CURR_WINDOW="$(wmctrl -lp | grep `xprop -root | grep _NET_ACTIVE_WINDOW | head -1 | awk '{print $5}' | sed 's/,//' | sed 's/^0x/0x0/'` | cut -d' ' -f6-)"
[[ "$CURR_WINDOW" = "$LAST_WINDOW" ]] || (echo -n `date` >> /scratch/timelog && echo -n "    " >> /scratch/timelog && echo "$CURR_WINDOW" >> /scratch/timelog)
LAST_WINDOW=$CURR_WINDOW
sleep 15 
done

