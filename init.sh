#!/bin/sh
# see http://heirloom.sourceforge.net/sh/sh.1.html#12

killall() {
    echo "Killing..."
    kill -s KILL ${last_background_proc_id}
}

trap killall SIGINT SIGTERM

# exec as background
python3 manage.py migrate
python3 manage.py runserver 0.0.0.0:8080 &

last_background_proc_id=$!

wait