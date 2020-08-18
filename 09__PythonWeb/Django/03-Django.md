---
title: "03-Django.md"
date: 2017-07-03 17:53:13 +0800
lastmod: 2019-09-29 17:53:13 +0800
draft: false
tags: ["Django"]
categories: ["python web"]
author: "Claymore"

---


### 上传文件

#### 基本形式

```python
	
    myFile = request.FILES.get("myfile", None)
    if not myFile:
        return render_ack(success=False, data="没有文件上传"), False
    # 通过后缀看上传文件是否是excel文件
    if 'xls' not in str(myFile):
        return render_ack(success=False, data='您上传的不是excel文件'), False
    # 限制文件大小。要求少于20兆
    if myFile.size > 20000000:
        return render_ack(success=False, data='上传文件要求小于20M'), False
    # 根据时间命名文件名，前缀要加上传者的内网账号
    file_name = user_name + datetime.datetime.now().strftime('%Y-%m-%d_%H:%M:%S')
    # 打开文件，并存到相关目录。
    with open(os.path.join('/usr/data/uploadUserInfo', file_name), 'w') as f:
        for chunk in myFile.chunks():  # 分块写人文件。
            f.write(chunk)
    # 通过mimetype 来看是否是excel文件。
    file_magic = magic.Magic(mime=True, uncompress=True)
    magic_str = file_magic.from_file('/usr/data/uploadUserInfo/'+file_name) # 正确格式application/xml 
    if magic_str != 'application/xml':
        return render_ack(success=False, data='您上传的不是excel文件'), False
```

s

#### 文件限制

判断文件格式，简单的判断后缀名是不严谨的，应该用`python-magic` 来判断（判断其MIME TYPE）。

上传的文件在linux下设置权限不可执行。

