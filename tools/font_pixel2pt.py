# -*- coding: utf-8 -*-
import pickle
import argparse
import glob
import os.path as osp

import pygame
from pygame import freetype
import numpy as np


def main():
    parser = argparse.ArgumentParser(description='')
    parser.add_argument('--fontDirPath', action='store',required=True, help="")
    parser.add_argument('--outputPath', action='store',required=True, help="")
    args = parser.parse_args()

    pygame.init()
    models = {}
    xs = []
    ys = np.arange(8,200)
    A = np.c_[ys, np.ones_like(ys)]

    fontFiles = glob.glob(osp.join(args.fontDirPath,'*.ttf'))
    for fontFile in fontFiles:
        print('current font file:',fontFile)
        font = freetype.Font(fontFile,size=12)
        height = [font.get_sized_glyph_height(float(y)) for y in ys]
        height = np.array(height)
        m,_,_,_ = np.linalg.lstsq(A,height)
        models[font.name] = m
        xs.append(height)

    with open(osp.join(args.outputPath,'font_px2pt.cp'),'wb') as fw:
        pickle.dump(models,fw)

if __name__ == '__main__':
    main()