import cv2 
import pytesseract

pytesseract.pytesseract.tesseract_cmd = 'C:\\Program Files\\Tesseract-OCR\\tesseract.exe'

import os

directory = 'downloads'
failure = []

# BEFORE RUNNING THIS MAKE SURE TO DOWNLOAD AND RENAME THE SCREENSHOT IMAGES FROM GOOGLE FORMS

for filename in os.listdir(directory):
    f = os.path.join(directory, filename)
    if "vol" in f or "gen" in f:
        pass
    elif os.path.isfile(f):
        img = cv2.imread(f)
        try:
            txt = pytesseract.image_to_string(img).lower()
        except:
            print("FAILURE3", f)
            failure.append(f)

        if 'bhavana' in txt or '7007593153' in txt:
            if '200' not in txt and '199' not in txt: 
                failure.append(f)
                print("FAILURE1", f)
            else:
                print("PASSED", f)
        else:
            failure.append(f)
            print("FAILURE2", f)

print(failure)

with open('failure.txt', 'w') as f:
    for i in failure:
        f.write(f"{i}\n")
