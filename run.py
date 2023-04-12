#!/usr/bin/env python3

import subprocess
import argparse
import PIL.Image
import cv2


# parse the arguments
ap = argparse.ArgumentParser()
ap.add_argument("s", type=int)
ap.add_argument("k", type=int)
ap.add_argument("t", type=int)
args = ap.parse_args()

#convert input image into pgm
im = cv2.imread("input_0.png")
img = cv2.cvtColor(im, cv2.COLOR_BGR2GRAY)
cv2.imwrite("input_0.pgm",img)
    
p = subprocess.run(['psf_estim', '-p', 'pattern_noise.pgm',
                    '-s', str(args.s), '-k', str(args.k), '-d', 'det_out.ppm', '-t', str(args.t),
                    '-o', 'psf.pgm', 'input_0.pgm', 'psf.txt'])

im = PIL.Image.open("psf.pgm")
# re adjust width and height to avoid visualization interpolation
width = 600
height = 600
# interpolate it by neareset neighbor
im = im.resize((width, height), "nearest") 
im.save("psf.png")

im = PIL.Image.open("det_out.ppm")
im.save("det_out.png")


