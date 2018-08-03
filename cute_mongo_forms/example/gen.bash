#!/bin/bash
files="*.svg"
for f in $files
do
    convert -background none $f -resize 1000x1000 $f.png
done
