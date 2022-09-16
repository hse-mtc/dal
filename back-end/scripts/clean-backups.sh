#!/usr/bin/env bash

find /back-end/backups -mtime +30 -exec rm {} \;
