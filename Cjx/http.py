#! /usr/bin/env python
#coding=utf-8
# -*- coding: utf-8 -*-
#date 14-3-17

import urllib,urllib2,re
import string,time,random,cookielib

#上传文件
import MultipartPostHandler

class httpCient:

    def __init__(self, autosleep=False, charset=None, proxy=None):
        """
        charset 编码
        proxy 代理字符串 如"192.168.1.1:8080"
        autoSleep 是否自动睡绵0-2秒 防止被封
        """
        self.proxy = proxy
        self.charset = charset
        self.auto_sleep = autosleep;
        self.cj = cookielib.CookieJar();
        print "init httpClient,proxy:", self.proxy, ",charset:", self.charset

    def cleanCookie(self):
        self.cj = cookielib.CookieJar();
        #self.cj.clear_session_cookies()

    def urlcontent(self, url, para=None, header={}):
        """
        获取地址的源代码
        url 要获取的网址
        header 头部设置
            """
        #print "start get url:%s" % url
        if self.auto_sleep:
            sleep_time = random.random()*2
            time.sleep(sleep_time)

        #设置代理 只设置http和https代理
        # if self.proxy:
        #     opener = urllib2.build_opener()
        #     urllib2.install_opener(opener)
        opener = None
        if self.proxy:
            opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(self.cj), urllib2.ProxyHandler({'http': self.proxy, 'https' : self.proxy}))
        else:
            opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(self.cj))
        urllib2.install_opener(opener)

        #设置post参数
        params = None
        if para:
            params = urllib.urlencode(para)
        #创建请求
        request = urllib2.Request(url, params, header)
        try:
            #发送请求
            response = urllib2.urlopen(request)
            content = response.read()
            #设置了编码
            if self.charset:
                content = content.encode(self.charset)
            #for index, cookie in enumerate(self.cj):
            #    print '[',index, ']',cookie;
            #print content
            return content
        except:
            #print 'get url content failed:', url
            return None

    def upload(self,url,params):
        #print "start get url:%s" % url
        if self.proxy:
            opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(self.cj), MultipartPostHandler.MultipartPostHandler, urllib2.ProxyHandler({'http': self.proxy, 'https' : self.proxy}))
        else:
            opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(self.cj), MultipartPostHandler.MultipartPostHandler)
        #try:
            #发送请求
        response = opener.open(url, params)
        content = response.read()
        #设置了编码
        if self.charset:
            content = content.encode(self.charset)
        #for index, cookie in enumerate(self.cj):
        #    print '[',index, ']',cookie;
        #print content
        return content
        #except:
            #print 'get url content failed:', url
            #return None
    def categroyList(self, content, caterepx):
        """读取所有分类信息
        content 已读取的分类信息内容
        caterepx 匹配分类的正则字符串
        返回匹配的数组"""
        list = self.itemlist(content, caterepx)
        return list['list']

    def itemlist(self, content, itemRepxStr, pagecount=0, pagecountrepx=""):
        """读取所有项列表信息
        content 获取项列表的地址
        itemRepx 匹配项的正则字符串
        pagecount 是否获取产品分页总数 如果pagecount=0时，表示要获取
        pagecountrepx 匹配产品分页总数的正则 只有pagecount=0时才有效
        返回{list:[<列表>],pagecount:<分页总数>,page:<当前分页>}
        """
        itemRepx = re.compile(itemRepxStr, re.I | re.S | re.X)

        list = itemRepx.findall(content)

        if pagecount == 0 and pagecountrepx != "":
            repx = re.compile(pagecountrepx, re.I | re.S | re.X)
            pagecounteResult = repx.findall(content)
            if len(pagecounteResult)>0:
                pagecount = pagecounteResult[0]
            else:
                print 'get pagecount failed!'
        result = {'list' : list, 'pagecount' : pagecount}
        return result

    def itemDetail(self, itemcontent, item={}):
        """
        获取产品的详细信息
        productcontent为产品内容 包括了产品的所有详细的源代码内容
        item为名称键值以及正则值 如 {"title":"title:\"(.*?)\"","url":"\"(.*?)"}
        返回键值对 如{“title”:"abc","url":"http://www.163.com"}
        """
        result = {}
        for k in item:
            repx = re.compile(item[k], re.I | re.S | re.X)
            repxList = repx.findall(itemcontent)
            if len(repxList) > 0:
                result[k] = repxList[0]
            else:
                print "get item detail key:", k, " failed!"
                result[k] = ""
        return result

    def lspacetrim(self, str):
        """
        去掉左边的空白字符
        """
        content = re.sub("^(\s|&nbsp;)+", "", str)
        return content

    def rspacetrim(self, str):
        """
        去掉右边的空白字符
        """
        content = re.sub("(\s|&nbsp;)+$", "", str)
        return content

    def spacetrim(self, str):
        """
        """
        content = re.sub("^(\s|&nbsp;)+|(\s|&nbsp;)+$", "", str)
        return content

    def allspacetrim(self, str):
        """
        """
        content = re.sub("(\s|&nbsp;)+", "", str)
        return content

    def trimHtmlChar(self, str):
        """
        删除所有html符号包含的字符
        """
        content = re.sub("<(.*?)>|&#60;(.*?)&#62;|&lt;(.*?)&gt;", "", str)
        return content

    def alltrim(self, str):
        """
        去掉所有html字符和空白字符
        """
        content = self.trimHtmlChar(str)
        content = self.allspacetrim(content)
        return content
