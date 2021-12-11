#!/usr/bin/env bash

set -e -x

for i in "$@"; do
  case $1 in
    -c | --check)
    check="--check"
    shift
    ;;

    *)
    echo "Unknown option: ${i}"
    exit 1
  esac
done

black \
  --verbose \
  ${check} \
  src
