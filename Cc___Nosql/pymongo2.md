### 聚合









### statistics

```python
from pymongo import MongoClient

client = MongoClient()
db = client.test

# print collection statistics
print db.command("collstats", "col_name") 

# print database statistics
print db.command("dbstats")
```

上述打印出来的大小单位为Bytes

