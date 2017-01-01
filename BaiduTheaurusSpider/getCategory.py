# -*- coding: utf-8 -*-
# @Author: LC
# @Date:   2016-03-26 22:42:39
# @Last modified by:   WuLC
# @Last Modified time: 2017-01-01 09:56:23
# @Email: liangchaowu5@gmail.com

# 功能：获取百度词库的分类

import urllib2
import re

def getBaiduDictCate():
    """
    功能：得到百度词库的分类，有三级分类，因为三级分类太细而且较少，所以将三级分类纳入其二级分类
    :return:两个词典，第一个词典记录大类的ID和内容的对应关系，第二个词典记录了第一个词典中每一类大类下的所有分类
    """
    bigCateDict = {}
    smallCateDict ={}
    """旧版网页url，已失效
    initPageURL = r'http://shurufa.baidu.com/dict.html'
    cateBaseURL = r'http://shurufa.baidu.com/dict-list.html?cid='
    """
    initPageURL = r'https://shurufa.baidu.com/dict'
    cateBaseURL = r'https://shurufa.baidu.com/dict_list?cid='
    try:
        response = urllib2.urlopen(initPageURL)
        data = response.read()
    except urllib2.HTTPError, e:
        print e.code

    # 换行正则匹配,需要对url中的?做转义,即使加r也不行
    bigCatePattern = re.compile(r'cid=(\d+).*?category1(.|\n)*?<span>(.*?)</span>')
    result = re.findall(bigCatePattern, data)
    for i in result:
        bigCateDict[i[0]] = i[2]  # 一个大类
        #print i[0], i[2]

        # 抓取大类下对应的小类
        smallCateDict[i[0]] = {}
        smallCateURL = cateBaseURL+i[0]
        try:
            smallResponse = urllib2.urlopen(smallCateURL)
            smallData = smallResponse.read()
        except urllib2.HTTPError, e:
            print e.code
        """旧版url解析,已失效
        if i[0] == '157':          # 表示城市地区的网页很特殊，需要特殊处理
            specialSmallPattern = re.compile(r'<a  href="dict-list.html\?cid=(\d+).*?category1" >(.*?)</a>')
            smallResult = re.findall(specialSmallPattern, smallData)
        else:
            smallCatePattern = re.compile(r'[^?]cid=(\d+).*?category[23]" ?>(.*?)</a>') # 将三级分类一并归到二级分类
            smallResult = re.findall(smallCatePattern,smallData)
        for j in smallResult:
            smallCateDict[i[0]][j[0]] = j[1]
            #print i[0], j[0], j[1]
        """
        smallCatePattern = re.compile(r'<a href=.*?dict-id="(\d+)"\n.*?>(.*?)</a>') # 将三级分类一并归到二级分类
        smallResult = re.findall(smallCatePattern,smallData)
        for j in smallResult:
            smallCateDict[i[0]][j[0]] = j[1]
            #print i[0], j[0], j[1]
    return bigCateDict, smallCateDict


if __name__ == '__main__':
    bigCateDict, smallCateDict = getBaiduDictCate()
    for i in bigCateDict:
        for j in smallCateDict[i]:
            print i, bigCateDict[i], j, smallCateDict[i][j]



