# -*- coding: utf8 -*-

import datetime
import docopt
import os
import re
import sys
import time
from PIL import Image
from PIL.ExifTags import TAGS

__doc__ = '''{0}: ファイルのタイムスタンプをexifやファイル名に従って更新する

Usage:
    {0} <fnames>...
    {0} --version

Options:
    <fnames>     : filenames
    -h --help    : show this message
    --version    : show version

'''.format(__file__)

__version__ = '0.1.0'

def get_file_datetime(fname):
    # ctimeはWindowsでは作成日時．linuxでは最終修正日時なので注意
    createdate = os.stat(fname).st_ctime
    cdt = datetime.datetime(*time.localtime(createdate)[:6])
    return cdt

def get_exif_datetime(fname):
    try:
        img = Image.open(fname)
    except:
        print('error',fname)
        return
    exif = img._getexif()
    try:
        for id,val in exif.items():
            tg = TAGS.get(id,id)
            if tg == "DateTimeOriginal":
                img.close()
                dt=val.split(' ')
                return datetime.datetime(*(list(map(int,dt[0].split(':') + dt[1].split(':')))))
    except AttributeError:
        img.close()
        return None
    img.close()
    return None

dt_pat = re.compile('.*/[^/\d]*(\d{14})[^/\d][^/]*jpg')
d_t_pat  = re.compile('.*/[^/\d]*(\d{8})[^/\d]*(\d{6})[^/]*jpg')
t_pat  = re.compile('.*/[^/\d]*(\d{6})[^/\d][^/]*jpg')
def get_name_datetime(f):
    dt_mat = dt_pat.search(f)
    if dt_mat:
        dt_str = dt_mat.group(1)
        print([dt_str[:4],dt_str[4:6],dt_str[6:8],dt_str[8:10],dt_str[10:12],dt_str[12:]])
    else:
        d_t_mat = d_t_pat.search(f)
        if d_t_mat is None:
            return None
        else:
            d_str,t_str = d_t_mat.groups()
            return datetime.datetime(*(list(map(int,[d_str[:4],d_str[4:6],d_str[6:],t_str[:2],t_str[2:4],t_str[4:]]))))
        return None

def main(fnames):
    for f in fnames:
        fstat_dt = get_file_datetime(f)
        exif_dt  = get_exif_datetime(f)
        if exif_dt is None:
            exif_dt = get_name_datetime(f)
            if exif_dt is None:
                continue
        if fstat_dt > exif_dt:
            os.utime(f,(exif_dt.timestamp(),exif_dt.timestamp()))

if __name__ == '__main__':
    args = docopt.docopt(__doc__, version=__version__)
    main(args['<fnames>'])
