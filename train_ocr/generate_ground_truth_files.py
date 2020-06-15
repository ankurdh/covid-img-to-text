#
# Once we have the preprocessed images, we need them to be split into individual
# lines and their corresponding ground truth text files that we can use to train
# tesseract
#

import glob
import ntpath
import os
import pathlib
import pytesseract
import shutil

state = 'rajasthan'

# Step 1. Fetch all the processed files
data_dir = os.path.join('data', state)
dst_dir = os.path.join('processed_files', state)

pwd = pathlib.Path(__file__).parent.absolute()
dst_dir = os.path.join(pwd, dst_dir)
pathlib.Path(dst_dir).mkdir(parents=True, exist_ok=True)

f = glob.glob(os.path.join(data_dir, '*_processed*'))
for processed_file in f:
    f_name = ntpath.basename(processed_file)
    shutil.copyfile(processed_file, os.path.join(dst_dir, f_name))

    # Step 2: Now that we have all our processed files, lets build hocr
    #         files from them using tesseract

    hocr = pytesseract.image_to_pdf_or_hocr(processed_file, extension='hocr')
    hocr_f_name = f_name.replace('.jpg', '.hocr')
    with open(os.path.join(dst_dir, hocr_f_name), 'wb') as f:
        f.write(hocr)
