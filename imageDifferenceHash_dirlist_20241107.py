#!/usr/bin/python3

# by Antonio "Visi@n" Broi antonio@tsurugi-linux.org
# https://tsurugi-linux.org
# 20241107

# LICENSE M.I.T. https://opensource.org/licenses/MIT

from PIL import Image, UnidentifiedImageError
import imagehash
import argparse
import os
from datetime import datetime
import time
import psutil
import webbrowser
import subprocess
import platform

# Determine the correct open command based on the OS
open_command = "xdg-open" if platform.system() == "Linux" else "open"
sound_command = "paplay" if platform.system() == "Linux" else "afplay"

# construct the argument parse and parse the arguments
ap = argparse.ArgumentParser()
ap.add_argument("-i", "--inputimage", required=True, 
    help="first image to compare")
ap.add_argument("-o", "--outputdirectory", required=True,
    help="directory images to compare")

args = vars(ap.parse_args())

# Recursive function to get all images in a directory and its subdirectories
def get_images(directory):
    images = []
    for root, _, files in os.walk(directory):
        for file in files:
            file_path = os.path.join(root, file)
            images.append(file_path)
    return images

# make a list of all available images 
images = get_images(args["outputdirectory"])

# Load input image and calculate hashes
try:
    first_image = Image.open(args["inputimage"])
    first_image_path = os.path.abspath(args["inputimage"])
    hash_first_image = {
        'average': imagehash.average_hash(first_image),
        'phash': imagehash.phash(first_image),
        'dhash': imagehash.dhash(first_image),
        'whash': imagehash.whash(first_image)
    }
except UnidentifiedImageError:
    print("Input image is corrupted or not an image.")
    exit(1)

# Define directories and HTML report paths
directories = ['average', 'phash', 'dhash', 'whash']
html_files = {}

for dir_name in directories:
    if not os.path.exists(dir_name):
        os.makedirs(dir_name)
    html_files[dir_name] = os.path.join(dir_name, "report.html")

# Create HTML files for each hash type
for hash_type in html_files:
    with open(html_files[hash_type], "w") as html_file:
        html_file.write(f"<html><head><title>Report - {hash_type}</title></head><body>\n")
        html_file.write(f"<h2>Report for {hash_type} hash matching</h2>\n")
        html_file.write(f"<h3>Input Image:</h3>")
        html_file.write(f"<a href='file://{first_image_path}' target='_blank'>")
        html_file.write(f"<img src='file://{first_image_path}' alt='Input Image' width='200'></a><br>")
        html_file.write(f"<p>Path: {first_image_path}</p><br>")

# Iterate over all images and compare hashes
for image_path in images:
    try:
        second_image = Image.open(image_path)
        hash_second_image = {
            'average': imagehash.average_hash(second_image),
            'phash': imagehash.phash(second_image),
            'dhash': imagehash.dhash(second_image),
            'whash': imagehash.whash(second_image)
        }

        # Comparison across all hash types
        for hash_type in hash_first_image:
            if hash_first_image[hash_type] == hash_second_image[hash_type]:
                abs_image_path = os.path.abspath(image_path)
                with open(html_files[hash_type], "a") as html_file:
                    html_file.write(f"<h4>Match found for {hash_type} hash</h4>\n")
                    html_file.write(f"<a href='file://{abs_image_path}' target='_blank'>")
                    html_file.write(f"<img src='file://{abs_image_path}' alt='Matched Image' width='150'></a><br>\n")
                    html_file.write(f"<p>Path: {abs_image_path}</p><br>\n")

                # Open matching images and play a sound
                subprocess.Popen([open_command, abs_image_path])
                subprocess.Popen([sound_command, "/System/Library/Sounds/Glass.aiff"])

                time.sleep(2)

    except UnidentifiedImageError:
        print(f"Skipping corrupted or non-image file: {image_path}")
    finally:
        for proc in psutil.process_iter():
            if proc.name() == "display":
                proc.kill()

# Finalize HTML files and open reports in a browser
for hash_type, html_file in html_files.items():
    with open(html_file, "a") as file:
        file.write("</body></html>")
    webbrowser.open(f"file://{os.path.abspath(html_file)}")

# Open input image at the beginning
subprocess.Popen([open_command, first_image_path])
