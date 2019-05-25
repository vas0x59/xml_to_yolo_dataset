import os
import glob
import pandas as pd
import argparse
import xml.etree.ElementTree as ET
import cv2

def xml_to_txt(path, classes):
    xml_list = []
    for xml_file in glob.glob(path + '/*.xml'):
        tree = ET.parse(xml_file)
        root = tree.getroot()
        v = {"file":xml_file.split("/")[-1], "data":[]}
        for member in root.findall('object'):
            # value = (root.find('filename').text,
            #         int(root.find('size')[0].text),
            #         int(root.find('size')[1].text),
            #         member[0].text,
            #         int(member[4][0].text),
            #         int(member[4][1].text),
            #         int(member[4][2].text),
            #         int(member[4][3].text)
            #         )
            xmin = int(member[4][0].text)
            ymin = int(member[4][1].text)
            xmax = int(member[4][2].text)
            ymax = int(member[4][3].text)
            width = int(root.find('size')[0].text)
            height = int(root.find('size')[1].text)
            val = [
                classes.index(member[0].text), 
                str(round((xmax+xmin)/2/width, 4)), 
                str(round((ymax+ymin)/2/height, 4)),
                str(round((xmax-xmin)/width, 4)), 
                str(round((ymax-ymin)/height, 4)),
                root.find('filename').text
            ]
            v["data"].append(val)
        xml_list.append(v)
    # column_name = ['filename', 'width', 'height',
    #             'class', 'xmin', 'ymin', 'xmax', 'ymax']
    # xml_df = pd.DataFrame(xml_list, columns=column_name)
    # return xml_df
    return xml_list


def main():
    # Initiate argument parser
    parser = argparse.ArgumentParser(
        description="Sample TensorFlow XML-to-CSV converter")
    parser.add_argument("-i",
                        "--inputDir",
                        help="Path to the folder where the input .xml files are stored",
                        type=str)
    parser.add_argument("-c",
                        "--classes",
                        help="classes",
                        type=str)
    parser.add_argument("-o",
                        "--outputDir",
                        help="Name of output .csv file (including path)", type=str)
    args = parser.parse_args()

    if(args.inputDir is None):
        args.inputDir = os.getcwd()
    # if(args.outputFile is None):
    #     args.outputFile = args.inputDir + "/labels.csv"

    assert(os.path.isdir(args.inputDir))
    f = open(args.classes, "r")
    classes = f.read().split()
    f.close()
    xml_df = xml_to_txt(args.inputDir, classes)
    for i in xml_df:
        img = cv2.imread(args.inputDir+"/"+i["file"].split('.')[0]+".png")
        cv2.imwrite(args.outputDir+"/"+i["file"].split('.')[0]+".jpg", img)
        f = open(args.outputDir+"/"+i["file"].split('.')[0]+".txt", "w+")
        st = ""
        for j in i["data"]:
            for q in j[:-1]:
                st+=str(q)
                st+=" "
            st+="\n"
        print(st)
        f.write(st)
        f.close()
        
        
    # xml_df.to_csv(
        # args.outputFile, index=None)
    print('Successfully converted xml to txts')


if __name__ == '__main__':
    main()