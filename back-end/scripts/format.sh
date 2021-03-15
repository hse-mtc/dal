#!/usr/bin/env bash

for i in "$@"; do
  case $1 in
    -d | --diff)
    diff="--diff"
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
  ${diff:- "--in-place"} \
  src
