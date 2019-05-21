#!/bin/bash

echo "Hello world"

# Configs
in_dir="/home/vasily/Projects/datasets/arduino_raspberry_metro/train"
classes="/home/vasily/Projects/datasets/arduino_raspberry_metro/names.names"
out_dir="/home/vasily/Projects/datasets/arduino_raspberry_metro/yolo"
python ./converter.py -i $in_dir -c $classes -o $out_dir