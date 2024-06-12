#!/usr/bin/env python3

import subprocess
import argparse
import PIL.Image
import cv2
import sys


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
    

try:
    p = subprocess.run(['psf_estim', '-p', '/workdir/bin/pattern_noise.pgm',
                    '-s', str(args.s), '-k', str(args.k), '-d', 'det_out.ppm', '-t', str(args.t),
                    '-o', 'psf.pgm', 'input_0.pgm', 'psf.txt'])
    im = PIL.Image.open("psf.pgm")
    # re adjust width and height to avoid visualization interpolation
    width = 600
    height = 600
    # interpolate it by neareset neighbor
    im = im.resize((width, height)) 
    im.save("psf.png")

    im = PIL.Image.open("det_out.ppm")
    im.save("det_out.png")

except Exception as e:    
    with open('stdout.txt', 'r') as file:
        stdout_text = file.read()
    if "No pattern was detected." in stdout_text.strip():
        with open('demo_failure.txt', 'w') as f:
            f.write('Pattern Not Found. Are you sure that there is a pattern in the image? It may have not been detected if\
                            the pattern covers only a small part of the image. Crop the image so that the pattern covers at\
                            least half of the image and re-run. Otherwise, upload an image containing a pattern.')
            sys.exit(0)

    elif "More than one pattern was detected." in stdout_text.strip():
        with open('demo_failure.txt', 'w') as f:
            f.write('More than one pattern was detected. Crop the image surounding the\
                        desired pattern and re-run.')
            sys.exit(0)
    else:
        with open('demo_failure.txt', 'w') as f:
            f.write('Unknown Run Time Error')
            sys.exit(0)
