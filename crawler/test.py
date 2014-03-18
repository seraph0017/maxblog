#!/usr/bin/env python
#encoding:utf-8
from webanan.models import Site,Category,Author,Article,Domain,Keyword

def get_author_list():
    author_list = []
    authors = Author.objects().all()
    for author in authors:
        author_list.append(author.name)
    print len(author_list)
    author_list = list(set(author_list))
    print len(author_list)
    return author_list


def xxx(authors):
    author_dict = {}
    for author in authors:
        author_object = Author.objects(name=author).first()
        author_objects = Author.objects(name=author).all()
        author_dict[author_object] = author_objects
    return author_dict



def run():
    authors = get_author_list()
    author_dict = xxx(authors)
    yyy(author_dict)
    delete_other(authors)



def yyy(author_objects):
    for k,v in author_objects.iteritems():
        for author in v:
            print k
            article = Article.objects(author=author).first()
            if article:
                article.author = k
                article.save()


def delete_other(authors):
    for author in authors:
        author_objects = Author.objects(name=author).all()
        if len(author_objects) > 1:
            for author in author_objects[1:]:
                author.delete()



def test():
    author_objects = Author.objects(name='JOJO').all()
    test1 = author_objects[1]
    test1_id = test1.id
    test1.delete()
    print Author.objects(id=test1_id).first()


    print test1_id

HEADER = '\033[95m'
OKBLUE = '\033[94m'
OKGREEN = '\033[92m'
WARNING = '\033[93m'
FAIL = '\033[91m'
ENDC = '\033[0m'



import os,sys,string   
import time

  
def view_bar(num=1, sum=100, bar_word="+"):   
    rate = float(num) / float(sum)   
    rate_num = int(rate * 100)   
    print '\r%d%% :' %(rate_num),   
    for i in range(0, rate_num):   
        os.write(1, bar_word)   
    sys.stdout.flush()   
  
if __name__ == '__main__':   
    for i in range(0, 14000):   
        time.sleep(0.1)   
        view_bar(i, 14000,OKGREEN+'∆'+'\033[0m')  

