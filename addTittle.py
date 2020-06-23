# coding:utf-8
# python3
import os, sys
import time, datetime
import subprocess, pipes

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
    timeString = timeString.split("+")[0][:-1]  # 2019-09-29 19:24:41
    t = datetime.strptime(timeString, "%Y-%m-%d %H:%M:%S")

    t8 = (t + datetime.timedelta(hours=8)).strftime("%Y-%m-%d %H:%M:%S")  # 加8小时
    print(t8)
    return(t8)


def createTittle(filename):
    old_filename=filename
    # 处理文件名转义
    filename = pipes.quote(filename)
    s = 'git log --pretty="format:%ci" {}'.format(filename)
   
    child1 = subprocess.Popen(s, shell=True, stdout=subprocess.PIPE, universal_newlines=True)
    all_commit_time = child1.stdout.read()

    first_commit_time = all_commit_time.split("\n")[-1]  # 2019-09-29 19:24:41 +0800
    # first_commit_time = timeTransform(first_commit_time)

    last_commit_time = all_commit_time.split("\n")[0]
    # last_commit_time = timeTransform(last_commit_time)


    old_filename = old_filename.split("/")[-1]
    
    print(old_filename, first_commit_time, last_commit_time)
    return title % (old_filename, first_commit_time, last_commit_time)



def forf():
    # 只是本地路径
    for dirpath, dirnames, filenames in os.walk("./"):
        for filename in filenames :
            if filename.endswith('.md'):
                content = ""
                f = os.path.join(dirpath, filename)
                print(f)
                with open(f, "r") as f1:
                    content = f1.read()
                tittle = createTittle(f)
                with open(f, "w") as f2:
                    content = tittle + content
                    f2.write(content)



if __name__ == "__main__":
    if len(sys.argv) > 1 :
        print(sys.argv[1])
        createTittle(sys.argv[1])
    #forf()
    # createTittle("README.md")
