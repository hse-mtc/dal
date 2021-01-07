#!/usr/bin/env bash

for i in "$@"; do
  case $1 in
    -i | --in-place)
    inplace="--in-place"
    shift
    ;;

    *)
    echo "Unknown option: ${i}"
    exit 1
  esac
done

yapf \
  --recursive \
  --exclude="*migrations*" \
  --verbose \
  ${inplace:- "--diff"} \
  conf auth common dms lms tgbot
