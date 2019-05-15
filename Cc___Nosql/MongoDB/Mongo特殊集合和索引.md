Tags:[nosql, database, mongodb]

### 固定集合

固定集合需要预先创建好，而且它的大小是固定的。

如果数据满了，再插入会把最老的文档删除掉释放空间，类似于队列。

可以用来放日志，前排名等。

需要显式创建：

`db.createCollection("mycol", {"capped": true, "size": 100000})`

创建了一个大小为100000字节的mycol集合。

指定文档数量： `("mycol", {"capped": true, "size": 100000}, "max": 100)`

#### 自然排序

对于固定文档来说，插入顺序就是拿出的顺序，因为文档大小不会改变

如果需要逆序：`db.mycol.find().sort({"$natural": -1})`



### TIL 索引

Time-to-live index, 具有生命周期的索引.

这种索引允许为每一个文档设置一个超时时间， 过时间后会自动删除，常用于会话。

`db.ttl.ensureIndex({"Date": 1}, {expireAfterSeconds: 300})`

当date服务器时间比Date晚300秒时就会删掉这个值，

为此，我们在用这个会话时可以更新这个值，防止被删除。

但是mongo后台设置每一分钟对TIL索引进行删除，所以这个清除的时间有时会有误差。



* 一个特定集合可以有很多TIL索引
* TIL索引不能是符合索引



### 全文本索引

对集合所有文本字段进行索引，会有较大的性能问题。pass.



### 地理空间索引

pass



### GridFS

GridFS 是 MongoDB的一种存储机制，用来存储大型二进制文件。

它的理念是将大文件分割，每个块（默认256KB）作为独立的文档进行存储。



使用场景：

* 如果您的文件系统在一个目录中存储的文件的数量有限，你可以使用GridFS存储尽可能多的文件。

* 当你想访问大型文件的部分信息，却不想加载整个文件到内存时，您可以使用GridFS存储文件，并读取文件部分信息，而不需要加载整个文件到内存。

* 当你想让你的文件和元数据自动同步并部署在多个系统和设施，你可以使用GridFS实现分布式文件存储。



#### mongofiles

比较简单的是使用mongofiles工具。

用mongofiles —help就可以看使用方式。

* put, `mongofiles put foo.txt`
* list, `mongofiles list`
* get, `mongofiles get foo.txt`
* search
* delete



#### 在pymongo中使用GridFS

```python
import gridfs
from pymongo import MongoClient
db = MongoClient().text
fs = gridfs.GridFS(db)
file_id = fs.put("hello world", filename="foo.txt")
fs.list()
[u'foo.txt']
fs.get(file_id).read()
'hello world'
```



### fs.chunks 和 fs.files

除了将文件的每一个块单独存储之外，还有一个文档用于将这些块组织在一起并存储该文件的元信息。

fs.chunks集合, 存储块：

```
{
    "_id": ObjectId("..."),
    "n": 0, #块在文件中的相对位置
    "data": BinData("..."), # 包含的二进制数据
    "files_id": ObjectId("...") #所属文件的元信息
}
```

fs.files 集合， 文件的元信息，下面是必有字段，可添加用户自定义字段：

```
{
    _id,
    length, # 文件所包含的字节数
    chunkSize, # 组成每个块的大小，单位是字节，默认是256KB，可以在需要时调整
    uploadDate, # 上传日期
    md5 #md5
}
```



