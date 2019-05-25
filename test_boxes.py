import os
import glob
import pandas as pd
# import argparse
# import xml.etree.ElementTree as ET
import cv2
path = "/home/vasily/Projects/datasets/arduino_raspberry_metro/yolo"
for xml_file in glob.glob(path + '/*.txt'):
    print(xml_file.split("/")[-1])
    img = cv2.imread(xml_file.split('.')[0] + ".jpg")
    f = open(xml_file, "r")
    boxes = f.read().split("\n")
    H = img.shape[0]
    W = img.shape[1]
    for i in boxes:
        i = i.split(" ")
        if len(i)> 2:
            print()
            x_c = float(i[1])*W
            y_c = float(i[2])*H
            w = float(i[3])*W
            h = float(i[4])*H
            cv2.rectangle(img, (int(x_c - w/2), int(y_c - h/2)), (int(x_c + w/2), int(y_c + h/2)), (0, 255, 0), 3)
    cv2.imshow("i", img)
    cv2.waitKey(0)