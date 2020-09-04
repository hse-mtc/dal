#!/usr/bin/env bash

while [[ "$#" -gt 0 ]]; do
  case $1 in
  -i | --in-place)
    inplace="--in-place"
    shift
    ;;
  *)
    echo "Unknown parameter passed: $1"
    exit 1
    ;;
  esac
  shift
done

yapf \
  --recursive \
  --exclude="*migrations*" \
  --verbose \
  ${inplace:- "--diff"} \
  backend dms mil_lms_backend
