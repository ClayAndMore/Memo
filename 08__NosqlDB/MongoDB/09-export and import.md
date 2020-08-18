---
title: "09-export and import.md"
date: 2019-09-29 17:53:13 +0800
lastmod: 2019-09-29 17:53:13 +0800
draft: false
tags: ["Mongodb"]
categories: ["Nosql"]
author: "Claymore"

---


### Mongo Export

mongoexport -h, 几个有用的参数:

```shell
Export MongoDB data to CSV, TSV or JSON files.

options:
  -h [ --host ] arg                     mongo host to connect to ( <set 
                                        name>/s1,s2 for sets)
  --port arg                            server port. Can also use --host 
                                        hostname:port
  -u [ --username ] arg                 username
  -p [ --password ] arg                 password

  -d [ --db ] arg                       database to use
  -c [ --collection ] arg               collection to use (some commands)
  -f [ --fields ] arg                   comma separated list of field names 
                                        e.g. -f name,age
  --fieldFile arg                       file with fields names - 1 per line
  -q [ --query ] arg                    query filter, as a JSON string
  --csv                                 export to csv instead of json
  -o [ --out ] arg                      output file; if not specified, stdout 
                                        is used
  --jsonArray                           output to a json array rather than one 
                                        object per line
  -k [ --slaveOk ] arg (=1)             use secondaries for export if 
                                        available, default 
```

默认导出json格式

eg:

`/ng8w/opt/tokumx/bin/mongoexport -d file -c info --fields name,address -out %s.json --query "{'_id':'%s'}"`







### Mongo Import

待补充：

https://docs.mongodb.com/manual/reference/program/mongoimport/

`mongoimport --db users --collection contacts --file contacts.json`



导出全库：

```
mongodump -d <database_name> -o <directory_backup>

mongorestore -d <database_name> <directory_backup> # or <directory_backup/dbname>
```

