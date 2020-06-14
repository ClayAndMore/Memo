# coding:utf-8
import os,time, datetime
import subprocess

title = """
---
title: "%s"
date: %s
lastmod: %s
draft: false
tags: [""]
categories: [""]
author: "Claymore"
---
"""

def timeTransform(timeString):
    """
    2019-09-29 19:24:41 +0800 -> 
    """
    timeString = timeString.split("+")[0][:-1] # 2019-09-29 19:24:41
    t = datetime.datetime.strptime(timeString, "%Y-%m-%d %H:%M:%S")
    t8 = (t + datetime.timedelta(hours=8)).strftime("%Y-%m-%d %H:%M:%S") # 加8小时
    print t8
    return t8


def createTittle(filename):
    s = 'git log --pretty="format:%ci" ' + filename
    child1 = subprocess.Popen(s, shell=True,stdout=subprocess.PIPE)
    all_commit_time = child1.stdout.read()

    first_commit_time = all_commit_time.split("\n")[-1] #2019-09-29 19:24:41 +0800
    first_commit_time = timeTransform(first_commit_time)

    last_commit_time = all_commit_time.split("\n")[0]
    last_commit_time = timeTransform(last_commit_time)
    
    
    print title%(filename, first_commit_time, last_commit_time)

def forf():
    # 只是本地路径
    for dirpath, dirnames, filenames in os.walk("./"):
        for filename in filenames :
            if filename.endswith('.md'):
                f = os.path.join(dirpath, filename)
                print f

if __name__ == "__main__":
    forf()
    # createTittle("README.md")
