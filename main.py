#! /usr/bin/env python
#coding=utf-8
# -*- coding: utf-8 -*-

"""
功能：自动下载vr 

"""
import os
from Cjx.http import httpCient

__author__ = u'appie'
http = None
downloadspath='downloads'

def list(url_="https://xhamster.com/channels/new-vr-%d.html", page_=1):
    url = url_ % page_
    print 'start get content:%s'%url
    body = http.urlcontent(url)
    l = None
    try:
        l = http.itemlist(body, '<div\ class=\"video\"><a\ href=\"(.*?)\"\ class=\"hRotator\">')
    except Exception, e:
        print 'get list body failure:%s'%url
        return None
    if not l:
        return None
    print 'finished,find video:%d'%len(l['list'])
    return l['list']

def detail(url_):
    print 'start get downloadUrl:%s'%url_
    body = http.urlcontent(url_)
    s = None
    try:
        s = http.itemDetail(body,{"url":'1440p\.mp4\"\,\"downloadUrl\"\:\"(.*?)\"\}','id':'\"video_id\":(.*?)\,'})
    except Exception, e:
        print 'get downloadUrl failure:%s'%url_
        return None
    if not s:
        return None
    print 'finished,video_id:%s'%(s['id'])
    s['url'] = s['url'].replace('\\/','/')
    return s
    #s = s.repalce('\\/','/')


def main():
    global http,totalAddNum
    root = os.path.split(os.path.realpath(__file__))[0]
   
    totalAddNum = 0
    http = httpCient()
    if not os.path.exists(downloadspath):
        os.mkdir(downloadspath)

    l = list()
    if l:
        for r in l:
            s = detail(r)
            if s:
                name = s['id']+'_1440p.mp4'
                fullpath = os.path.join(downloadspath, name)
                if os.path.exists(fullpath):
                    print 'file is exists,skip'
                    continue
                cmd = 'wget -P %s %s'%(downloadspath, s['url'])
                os.system(cmd)
    #r = os.system(cmd)
    #print r
   # print s



if __name__ == '__main__':
    main()

