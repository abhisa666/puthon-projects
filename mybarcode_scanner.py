# USAGE
# python barcode_scanner.py
from imutils.video import VideoStream
from pyzbar import pyzbar
import argparse
import datetime
from datetime import datetime
import imutils
import time
import cv2
import winsound
import requests
frequency = 2500  # Set Frequency To 2500 Hertz
duration = 800  # Set Duration To 1000 ms == 1 second

apikey="BF80058AAD7EE72C2230D2D600C933DF"

def UPC_lookup(apikey,upc):
    print(upc)
    url = "https://api.upcdatabase.org/product/%s?apikey=%s" % (upc, apikey)
    response = requests.get(url)
    res_jason = response.json()
    print(res_jason["description"]+" :----\n")
    for key, value in res_jason.items():
        print(key, ":", value)
    print("\n\n")



ap = argparse.ArgumentParser()
ap.add_argument("-o", "--output", type=str, default="barcodesData.csv",
    help="path to output CSV file ")
args = vars(ap.parse_args())


print("Starting webcam")


vs = VideoStream(src=0).start()
time.sleep(2.0)
csvWrite = open(args["output"], "w")

found = set()
while True:
    frameData = vs.read()
    frameData = imutils.resize(frameData, width=600)
    barcodes = pyzbar.decode(frameData) 
    
    for barcode in barcodes:
        (x, y, width, height) = barcode.rect
        cv2.rectangle(frameData, (x, y), (x + width, y + height), (0, 0, 255), 2)
        barcodeData = barcode.data.decode("utf-8")
        barcodeType = barcode.type
        textData = "{} ({})".format(barcodeData, barcodeType)
        cv2.putText(frameData, textData, (x, y - 10),
            cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 2)
            
        if barcodeData not in found:
            csvWrite.write("{}\n".format(str(barcodeData)))
            csvWrite.flush()
            found.add(barcodeData)
            winsound.Beep(frequency, duration)

            
                
    cv2.imshow("Barcode Scanner", frameData)
    key = cv2.waitKey(1) & 0xFF
    if key == ord("e"):
         break

    # UPC_lookup(apikey,barcodeData)
    # close the output CSV file do a bit of cleanup
csvWrite.close()
cv2.destroyAllWindows()
vs.stop()    

import numpy as np
import pandas as pd
from datetime import datetime
import re
import time


data = pd.read_csv('barcodesData.csv', names = ['UPC'] ,dtype=str)
upcs = data['UPC']
# print(upcs)
for upc in upcs:
     # upc_s = str(upc)
    # upc_zero = upc_s.rjust(2 + len(upc_s), '0')
    UPC_lookup(apikey,upc)



# from tkinter import *
# from tkinter import ttk
# window = Tk()
# window.wm_title("Barcode Scanner")

# window.geometry("1000x700")
# tv = ttk.Treeview(window,height=17)
# tv.heading("#0",text="Barcode No.")
# tv["columns"] = ("description")
# tv.column("description",width=650)
# # tv.column("description",width=450)
# tv.heading("description",text="Description")
# tv.grid(row=0,column=0)
# b1=Button(window,text="Start Scanning",width=50,command=read_barcode)
# b1.grid(row=1,column=0)

# window.mainloop()
