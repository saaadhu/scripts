#! /bin/bash
LAST_WINDOW=
IDLE=
while :
do
    LAST_IDLE=$IDLE
    [[ `xprintidle` -ge 14000 ]] && CURR_WINDOW="[Idle]" || CURR_WINDOW="$(wmctrl -lp | grep `xprop -root | grep _NET_ACTIVE_WINDOW | head -1 | awk '{print $5}' | sed 's/,//' | sed 's/^0x/0x0/'` | cut -d' ' -f6-)"
    [[ "$CURR_WINDOW" = "$LAST_WINDOW" ]] || (echo -n `date` >> /scratch/timelog && echo -n "    " >> /scratch/timelog && echo "$CURR_WINDOW" >> /scratch/timelog)
    LAST_WINDOW=$CURR_WINDOW
    sleep 15 
done

