#!/usr/bin/python3

import re
import sys
import csv
import time
import datetime
import pandas as pd
from retrying import retry
from shutil import copyfile
from stravalib.client import Client
from WarReportLogger import main_logger

def main(argv):
    timeframe = None
    segoutput = 'segoutput.csv'
    if len(argv) > 1:
        timeframe = argv[1]
        segoutput = 'segoutput_' + argv[1] + '.csv'

    print('read ' + segoutput)
    df1 = pd.read_csv(segoutput, index_col=False)
    df1 = df1.set_index(['segment_id'])

    #read newly created segoutput.csv (df2) and compare it to original (df1):
    # time.sleep(5)
    df2 = pd.read_csv(segoutput, index_col=False)
    df2 = df2.set_index(['segment_id'])
    # try:
    main_logger(df2, df1, timeframe)
    # except Exception as e:
        # print('Error: ', str(e))
        # pass

if __name__ == "__main__":
  main(sys.argv)
