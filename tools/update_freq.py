# -*- coding: utf-8 -*-
from collections import Counter
import pickle
import argparse
import glob
import os.path as osp

def main():

  parser = argparse.ArgumentParser(description='Genereate Synthetic Scene-Text Images')
  parser.add_argument('--corpusPath',action='store',required=True,dest='corpusPath')
  parser.add_argument('--outputPath',action='store',required=True,dest='outputPath')

  args = parser.parse_args()

  files = glob.glob(osp.join(args.corpusPath,'*.txt'))
  charsCounter = Counter()

  for file in files:
    with open(file,encoding='utf-8') as fr:
        [charsCounter.update(list(line.strip())) for line in fr ]

  totalCharsNum = float(sum(charsCounter.values()))
  ans = {k:v/totalCharsNum for k,v in charsCounter.items()}

  with open(osp.join(args.outputPath,'char_freq.cp'),'wb') as fw:
    pickle.dump(ans,fw)

if __name__ == '__main__':
    main()