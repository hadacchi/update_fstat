# -*- coding: utf8 -*-

import datetime
import docopt
import os
import time
from PIL import Image
from PIL.ExifTags import TAGS

__doc__ = '''{0}: ファイルのタイムスタンプをexifやファイル名に従って更新する

Usage:
    {0} <fnames>...

Options:
    <fnames>    : filenames

'''.format(__file__)

__version__ = '0.0.1'

def update_filetimestamp(fname):
    return

def get_file_timestamp(fname):
    createdate = os.stat(fname).st_ctime
    cdt = datetime.datetime(*time.localtime(createdate)[:6])
    return cdt

def get_exif_timestamp(fname):
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

def main(fnames):
    for f in fnames:
        print(get_file_timestamp(f),get_exif_timestamp(f))

if __name__ == '__main__':
    args = docopt.docopt(__doc__, version=__version__)
    main(args['<fnames>'])
