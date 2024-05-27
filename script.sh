#!/bin/bash

uvicorn user_service:main_service_app &
UVICORN_PID=$!
sleep 2
python subscriber.py &
SUBSCRIBER_PID=$!
python publisher.py &
PUBLISHER_PID=$!

sleep 16

kill $UVICORN_PID
kill $SUBSCRIBER_PID
kill $PUBLISHER_PID

sleep 2

echo "Все процессы завершены"

