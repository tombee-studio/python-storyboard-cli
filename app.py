from PIL import Image, ImageDraw, ImageFont

import cv2
import glob
import tqdm
import argparse
import numpy as np
import pandas as pd

import os
import re


def pil2cv(imgPIL):
    imgCV_RGB = np.array(imgPIL, dtype = np.uint8)
    imgCV_BGR = np.array(imgPIL)[:, :, ::-1]
    return imgCV_BGR


def cv2pil(imgCV):
    imgCV_RGB = imgCV[:, :, ::-1]
    imgPIL = Image.fromarray(imgCV_RGB)
    return imgPIL


def cv2_putText(img, text, org, fontFace, fontScale, color):
    x, y = org
    b, g, r = color
    colorRGB = (r, g, b)
    imgPIL = cv2pil(img)
    draw = ImageDraw.Draw(imgPIL)
    fontPIL = ImageFont.truetype(font=fontFace, size=fontScale)
    draw.text(xy = (x, y), text = text, fill = colorRGB, font = fontPIL)
    imgCV = pil2cv(imgPIL)
    return imgCV


def atoi(text):
    return int(text) if text.isdigit() else text


def natural_keys(text):
    return [ atoi(c) for c in re.split(r'(\d+)', text) ]


def get_filename_without_ext(filepath):
    return os.path.splitext(os.path.basename(filepath))[0]


def NPR(src):
    # o = cv2.edgePreservingFilter(src, flags=1, sigma_s=60, sigma_r=0.7)
    o = cv2.stylization(src)
    return o


def get_pic2npr(out, excel_file, is_webcam, pic, dir="HarryPotter/", seconds=4, framerate=24.0):
    fourcc = cv2.VideoWriter_fourcc('m','p','4', 'v')  # コーデックの指定
    video  = cv2.VideoWriter('movie.mp4', fourcc, framerate, (640, int(640 * (1964 / 3024))))
    df = pd.read_excel(excel_file, sheet_name="ハリーポッター", index_col=0, header=2)
    for [description, file] in tqdm.tqdm(df[["イベント名", "ファイル"]].values):
        img = cv2.imread(f"{dir}{file}", cv2.IMREAD_COLOR)
        o = cv2.resize(NPR(img), (640, int(640 * (1964 / 3024))))
        for _ in range(int(seconds * framerate)):
            fontPIL = "YuGothic-Bold.otf"
            o = cv2_putText(o, 
                '\n'.join([description[i:i + 24] for i in range(0, len(description), 24)]), 
                org=(100, 300),
                fontFace=fontPIL,
                fontScale=16,
                color=(255, 255, 255))
            video.write(o)
    video.release()


def main():
    parser = argparse.ArgumentParser(description='python+opencv_npr')
    parser.add_argument('--in_pic','-i',default='sample.png',help='input_picture_name')
    parser.add_argument('--out','-o',default='./',help='output_dir')
    parser.add_argument('--is_webcam',action='store_true',help='use webwebcam_or_pic2npr')
    args = parser.parse_args()
    get_pic2npr(args.out, "タイムスタンプ付あらすじ文_ハリーポッター.xlsx", args.is_webcam, args.in_pic)


if __name__ == "__main__":
    main()