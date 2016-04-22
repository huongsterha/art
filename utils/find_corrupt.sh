#!/usr/bin/env sh

DATA_ROOT='/Volumes/data/art'

# make log file if it doesn't already exist
if [ ! -a '../logs/corrupt_image_files.log' ]; then
    touch '../logs/corrupt_image_files.log'
fi

# write the errors
find $DATA_ROOT -iname "*.jpg" -print0 | \
xargs -0 jpeginfo -c | \
grep -e WARNING -e ERROR > \
'../logs/corrupt_image_files.log'