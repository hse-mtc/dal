#!/usr/bin/env bash

for i in "$@"; do
  case $1 in
    -d|--database)
    DATABASE=true
    shift
    ;;

    -m|--media)
    MEDIA=true
    shift
    ;;

    *)
    echo "Unknown option: ${i}"
    exit 1
  esac
done

ARGUMENTS=(
  "--verbosity" 3
  "--force-color"
)

if [ "$DATABASE" ]; then
  python manage.py dbbackup "${ARGUMENTS[@]}"
else
  echo "[INFO] database backup was not requested (-d | --database)"
fi

if [ "$MEDIA" ]; then
  python manage.py mediabackup "${ARGUMENTS[@]}"
else
  echo "[INFO] media files backup was not requested (-m | --media)"
fi
