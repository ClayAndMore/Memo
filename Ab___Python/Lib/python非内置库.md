Tags:[python, py_lib]

## 非内置

### rsa

git: `https://github.com/sybrenstuvel/python-rsa`

说明：`https://stuvel.eu/python-rsa-doc/usage.html`

#### 生成秘钥

rsa.newkeys()

```python
>>> import rsa
>>> (pubkey, privkey) = rsa.newkeys(512)
>> pubkey
PublicKey(114015180291009189880751287724398507755979872951682778251118140252600017917610469, 65537)
```

返回值是公私钥对象。

512 必传参数， 指定位数， 位数多安全，但生成时间会变慢。

（512，0.11s),  (1024, 0.79s), (20148, 6s) ， 该时间是在单核单线程下。

可选参数：poolsize

加速密钥生成过程的另一种方法是并行使用多个进程来加速密钥生成。使用不超过机器可以并行运行的进程数; 双核机器应该使用`poolsize=2`; 一个四核超线程机器可以在每个核心上运行两个线程，因此可以使用`poolsize=8`。 

`(pubkey, privkey) = rsa.newkeys(512, poolsize=8)`



#### 导入秘钥

 `rsa.PrivateKey.load_pkcs1()`and `rsa.PublicKey.load_pkcs1()` 从文件中导入公私钥：

```
>>> import rsa
>>> with open('private.pem', mode='rb') as privatefile:
...     keydata = privatefile.read()
>>> privkey = rsa.PrivateKey.load_pkcs1(keydata)
```

或者可以直接从写死在程序里导入字符串变量。



#### 加密和解密

```python
>>> import rsa
>>> message = 'hello Bob!'.encode('utf8') 
>>> crypto = rsa.encrypt(message, bob_pub) # 加密， crypre字符也要处理，一般base64
>>> message = rsa.decrypt(crypto, privkey)
>>> message.decode('utf8')
hello Bob!
```

这里用了enconde, 一般我们爱用base64, 防止非法字符的扰乱。



#### 签证和确认

 ```python
signature = rsa.sign(message, privkey, 'SHA-1') # 这里signature也是字符，也要处理
算法可选：  ‘MD5’, ‘SHA-1’, ‘SHA-256’, ‘SHA-384’ or ‘SHA-512’.
rsa.verify(message, signature, pubkey)
True
如果message被串改， 则报：
rsa.pkcs1.VerificationError: Verification failed
 ```







### psutil

 psutil是一个跨平台库，能够轻松实现获取系统运行的进程和系统利用率（包括CPU、内存、磁盘、网络等）信息。它主要应用于系统监控，分析和限制系统资源及进程的管理。



### chardet

只支持python2.7 和 python3+

有时我们不知道某字符串是什么编码，我们可以用这个模块检测，带有概率的检测：

```python
import chardet  
import urllib  
  
#可根据需要，选择不同的数据  
TestData = urllib.urlopen('http://www.baidu.com/').read()  
print chardet.detect(TestData)  
  
运行结果：  
{'confidence': 0.99, 'encoding': 'GB2312'}  
```

运行结果表示有99%的概率认为这段代码是GB2312编码方式。

```python 
import urllib  
from chardet.universaldetector import UniversalDetector  
usock = urllib.urlopen('http://www.baidu.com/')  
#创建一个检测对象  
detector = UniversalDetector()  
for line in usock.readlines():  
    #分块进行测试，直到达到阈值  
    detector.feed(line)  
    if detector.done: break  
#关闭检测对象  
detector.close()  
usock.close()  
#输出检测结果  
print detector.result  
  
运行结果：  
{'confidence': 0.99, 'encoding': 'GB2312'}  
```

应用背景，如果要对一个大文件进行编码识别，使用这种高级的方法，可以只读一部，去判别编码方式从而提高检测速度。



一般使用：

chardet.detect() 参数只接受  type 字节数组，否侧：

`TypeError: Expected object of type bytes or bytearray, got: <type 'unicode'>`



这就要根据python版本来区分了， 在python2中str(默认字符类型）为字节数组， 和字符前加b是等效的：

```python
>>> chardet.detect('hello')
{'confidence': 1.0, 'language': '', 'encoding': 'ascii'}
>>> chardet.detect(b'hello')
{'confidence': 1.0, 'language': '', 'encoding': 'ascii'}
>>> chardet.detect('天王盖地虎')
{'confidence': 0.0, 'language': None, 'encoding': None}
>>> chardet.detect('天王盖地虎'.decode('gbk').encode('utf-8'))
{'confidence': 0.9690625, 'language': '', 'encoding': 'utf-8'}
```



而python3中默认字符类型是str(unicode), 需要转换成字节数组：

```python
>>> chardet.detect('hello')
Traceback (most recent call last):
  File "<stdin>", line 1, in <module>
  File "F:\Anaconda\lib\site-packages\chardet\__init__.py", line 34, in detect
    '{0}'.format(type(byte_str)))
TypeError: Expected object of type bytes or bytearray, got: <class 'str'>
>>> chardet.detect(b'hello')
{'encoding': 'ascii', 'confidence': 1.0, 'language': ''}
>>> chardet.detect(b'hello')
{'encoding': 'ascii', 'confidence': 1.0, 'language': ''}
>>> chardet.detect(b'宝塔镇河妖')
  File "<stdin>", line 1
SyntaxError: bytes can only contain ASCII literal characters.
>>> chardet.detect('宝塔镇河妖'.encode('gbk'))
{'encoding': None, 'confidence': 0.0, 'language': None}
>>> chardet.detect('天王k盖地虎,宝塔镇河妖'.encode('gbk'))
{'encoding': 'GB2312', 'confidence': 0.99, 'language': 'Chinese'}
```

当然字符长度长一些时才能更精准的识别。





### msgpack

安装：`pip install msgpack`

MessagePack 是一个高效的二进制序列化格式。它让你像 JSON 一样可以在各种语言之间交换数据。但是它比 JSON 更快、更小。小的整数会被编码成一个字节，短的字符串仅仅只需要比它的长度多一字节的大小。

主要思想就是将json中一些重复出现的符号（如括号、冒号、逗号等）用更精简的方式来表示。

```python
>>> msgpack.unpackb([1,2,3])
>>> msgpack.unpackb(_)
[1, 2, 3]
>>> msgpack.unpackb(_).decode('utf-8')
u'\u4e2d\u6587'
```



