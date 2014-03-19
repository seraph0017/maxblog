#!/usr/bin/env python
#encoding:utf-8


import logging

logger = logging.getLogger('__file__')
formatter = logging.Formatter('%(asctime)s %(levelname)s %(message)s')
hd = logging.StreamHandler()
hd.setFormatter(formatter)
logger.addHandler(hd)
logger.setLevel(logging.NOTSET)


def run():
    for i in range(100):
        # print i
        logger.info('hello {}'.format(i))



if __name__ == "__main__":
    run()