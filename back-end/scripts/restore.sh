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

    -y|--yes)
    NO_INPUT=true
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

if [ "$NO_INPUT" ]; then
  ARGUMENTS+=("--noinput")
fi

if [ "$DATABASE" ]; then
  python manage.py dbrestore "${ARGUMENTS[@]}"
else
  echo "[INFO] database restore was not requested (-d | --database)"
fi

if [ "$MEDIA" ]; then
  python manage.py mediarestore "${ARGUMENTS[@]}"
else
  echo "[INFO] media files restore was not requested (-m | --media)"
fi
