#!/bin/bash

SOURCE="./rajasthan/"
lang=eng
set -- "$SOURCE"*.jpg
for img_file; do
    echo -e  "\r\n File: $img_file"
    OMP_THREAD_LIMIT=1 tesseract "${img_file}" "${img_file%.*}"  --psm 6  --oem 1  -l $lang -c page_separator='' hocr
    PYTHONIOENCODING=UTF-8 hocr-extract-images -b $SOURCE -p "${img_file%.*}"-%03d.tif  "${img_file%.*}".hocr
done
