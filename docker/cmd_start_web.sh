#!/bin/sh
sleep 5
exec uv run gunicorn _project.wsgi:application --bind 0.0.0.0:8000
