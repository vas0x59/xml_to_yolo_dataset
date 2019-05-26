import os
import glob
import pandas as pd
import argparse
import xml.etree.ElementTree as ET
import cv2

def simplify_class(cl_int, CLASSES, SIMPLE_CLASSES):
    simple_cl = ""
    cl_str = CLASSES[int(cl_int)]
    for i in SIMPLE_CLASSES:
        if i in cl_str:
            simple_cl = i
            break
    return SIMPLE_CLASSES.index(simple_cl)

def main():
    # Initiate argument parser
    parser = argparse.ArgumentParser(
        description="Sample TensorFlow XML-to-CSV converter")
    parser.add_argument("-i",
                        "--inputDir",
                        help="Path to the folder where the input .xml files are stored",
                        type=str)
    parser.add_argument("-o",
                        "--outputDir",
                        help="Path to the folder where the input .xml files are stored",
                        type=str)
    parser.add_argument("-c",
                        "--classes",
                        help="classes",
                        type=str)
    parser.add_argument("-s",
                        "--simpleClasses",
                        help="simpleClasses",
                        type=str)

    args = parser.parse_args()

    if(args.inputDir is None):
        args.inputDir = os.getcwd()
    # if(args.outputFile is None):
    #     args.outputFile = args.inputDir + "/labels.csv"
    CLASSES = open(args.classes, 'r').read().split('\n')
    SIMPLE_CLASSES = open(args.classes, 'r').read().split('\n')
    assert(os.path.isdir(args.inputDir))
    for txt_file in glob.glob(args.inputDir + '/*.txt'):
        file_lines = open(txt_file, "r").readlines()
        file_lines_towrite = []
        for i in file_lines:
            data = i.split(" ")[:-1]
            # print(data)
            full_class = data[0]
            data[0] = simplify_class(full_class, CLASSES, SIMPLE_CLASSES)
            data_str = ""
            for q in data:
                data_str+=str(q)
                data_str+=" "
            data_str = data_str + '\n'
            print(data_str)
            file_lines_towrite.append(data_str)
        open(args.outputDir+'/'+txt_file.split('/')[-1], 'w+').writelines(file_lines_towrite)


if __name__ == '__main__':
    main()