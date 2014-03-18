#!/usr/bin/env python
#encoding:utf-8
from multiprocessing import Pool
from time import sleep
from datetime import datetime


def foo(name):
    print 'hello world {}'.format(name)
    sleep(5)
    print 'nice to meet you. {}'.format(name)


def run():
    pool = Pool(processes=8)
    names = range(1000)
    pool.map(foo,names)


if __name__ == "__main__":
    start = datetime.now()
    run()
    stop = datetime.now()
    print stop - start