

## demo

### 执行js脚本插入多条数据

执行 mongo test.js

test.js:

``` js
db = connect("localhost:27017/admin");

db.auth('root','root');

var cursor = db.namespace.findOne();

printjson(cursor)

var dataTemp = {
    "action": "Allow",
    "annotations": { },
    "logsenabled": false,
    "metadata": [ ],
    "name": "testqqqqq",
    "namespace": "/",
    "normalizedtags": [
        "$identity=networkaccesspolicy",
        "$type=Network"
    ],
    "object": [
        [
            "$name=debian-wy"
        ]
    ],
    "observationenabled": false,
    "observedtrafficaction": "Continue",
    "ports": [
        "tcp/80"
    ],
    "updatetime": ISODate("2020-12-22T11:37:51.868Z")
}

var data=new Array()
var name="TTEST"

for (var i=0;i<10;i++)
{
    var temp = JSON.parse(JSON.stringify(dataTemp));
    temp.name = name + i.toString();
    data.push(temp);

}

try {
    //db.networkaccesspolicy.insertOne(dataTemp)
    db.networkaccesspolicy.insertMany(data)
} catch (e) {
    print (e);
};

```



文档：https://docs.mongodb.com/manual/reference/method/