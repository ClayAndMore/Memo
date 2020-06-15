
---
title: "15_HBase伪分布.md"
date: 2019-09-29 17:53:13 +0800
lastmod: 2019-09-29 17:53:13 +0800
draft: false
tags: [""]
categories: [""]
author: "Claymore"

---


https://hbase.apache.org/book.html#quickstart



JDK



### 准备

选个镜像下载，最好是stable版：http://apache.cs.utah.edu/hbase/stable/

```sh
[root@10.250.123.10 hadoop]#down http://apache.cs.utah.edu/hbase/stable/hbase-1.4.10-bin.tar.gz
  % Total    % Received % Xferd  Average Speed   Time    Time     Time  Current
                                 Dload  Upload   Total   Spent    Left  Speed
100  108M  100  108M    0     0  3857k      0  0:00:28  0:00:28 --:--:-- 12.1M 
[root@10.250.123.10 hadoop]#tar zfx hbase-1.4.10-bin.tar.gz 
[root@10.250.123.10 hadoop]#ls
hbase-1.4.10  hbase-1.4.10-bin.tar.gz 
```

配置环境变量：

```sh
[root@10.250.123.10 hbase-1.4.10]#pwd
/disk/hadoop/hbase-1.4.10

vi /etc/profile
export JAVA_HOME=/disk/jre1.8.0_211
export HADOOP_HOME=/disk/hadoop/hadoop-2.9.2
export HBASE_HOME=/disk/hadoop/hbase-1.4.10
export PATH=$PATH:$JAVA_HOME/bin:$HADOOP_HOME/bin:$HADOOP_HOME/sbin:$HBASE_HOME/bin

source /etc/profile
```



### 配置文件

改 java_home: vim  conf/hbase-env.sh

```
# Tell HBase whether it should manage it's own instance of Zookeeper or not.
# export HBASE_MANAGES_ZK=true
```

注意其中有： HABSE_MANAGES_ZK=true,    **Hbase内置了zk** 

改conf/hbase-site.xml：

```xml
<configuration>
  <property>
    <name>hbase.rootdir</name>
    <value>file:///disk/hadoop/hbase/rootdir</value>
  </property>
  <property>
    <name>hbase.zookeeper.property.dataDir</name>
    <value>/disk/hadoop/hbase/zookeeper</value>
  </property>
</configuration>
```

定义文件夹拖写Hbase和Zookeeper的数据。不需要自己去手动创建目录，Hbase会自动为你创建。

`file://` 象征着本地文件系统



开始运行：

```sh
[root@10.250.123.10 hbase-1.4.10]#bin/start-hbase.sh 
running master, logging to /disk/hadoop/hbase-1.4.10/logs/hbase-root-master-10.250.123.10.out
Java HotSpot(TM) 64-Bit Server VM warning: ignoring option PermSize=128m; support was removed in 8.0
Java HotSpot(TM) 64-Bit Server VM warning: ignoring option MaxPermSize=128m; support was removed in 8.0
SLF4J: Class path contains multiple SLF4J bindings.
SLF4J: Found binding in [jar:file:/disk/hadoop/hbase-1.4.10/lib/slf4j-log4j12-1.7.10.jar!/org/slf4j/impl/StaticLoggerBinder.class]
SLF4J: Found binding in [jar:file:/disk/hadoop/hadoop-2.9.2/share/hadoop/common/lib/slf4j-log4j12-1.7.25.jar!/org/slf4j/impl/StaticLoggerBinder.class]
SLF4J: See http://www.slf4j.org/codes.html#multiple_bindings for an explanation.
SLF4J: Actual binding is of type [org.slf4j.impl.Log4jLoggerFactory]
```

jps:

```
[root@10.250.123.10 hbase-1.4.10]#jps
31974 Jps
31559 HMaster
```





### hbase shell

```sh
root@10.250.123.10 hbase-1.4.10]#hbase shell
HBase Shell
Use "help" to get list of supported commands.
Use "exit" to quit this interactive shell.
Version 1.4.10, r76ab087819fe82ccf6f531096e18ad1bed079651, Wed Jun  5 16:48:11 PDT 2019

hbase(main):001:0> help  # 执行help看下
HBase Shell, version 1.4.10, r76ab087819fe82ccf6f531096e18ad1bed079651, Wed Jun  5 16:48:11 PDT 2019
Type 'help "COMMAND"', (e.g. 'help "get"' -- the quotes are necessary) for help on a specific command.
Commands are grouped. Type 'help "COMMAND_GROUP"', (e.g. 'help "general"') for help on a command group.
# 命令被分组

COMMAND GROUPS:
  Group name: general
  Commands: processlist, status, table_help, version, whoami

  Group name: ddl
  Commands: alter, alter_async, alter_status, create, describe, disable, disable_all, drop, drop_all, enable, enable_all, exists, get_table, is_disabled, is_enabled, list, list_regions, locate_region, show_filters

  Group name: namespace
  Commands: alter_namespace, create_namespace, describe_namespace, drop_namespace, list_namespace, list_namespace_tables

  Group name: dml
  Commands: append, count, delete, deleteall, get, get_counter, get_splits, incr, put, scan, truncate, truncate_preserve

  Group name: tools
  Commands: assign, balance_switch, balancer, balancer_enabled, catalogjanitor_enabled, catalogjanitor_run, catalogjanitor_switch, cleaner_chore_enabled, cleaner_chore_run, cleaner_chore_switch, clear_deadservers, close_region, compact, compact_rs, compaction_state, flush, is_in_maintenance_mode, list_deadservers, major_compact, merge_region, move, normalize, normalizer_enabled, normalizer_switch, split, splitormerge_enabled, splitormerge_switch, trace, unassign, wal_roll, zk_dump

  Group name: replication
  Commands: add_peer, append_peer_tableCFs, disable_peer, disable_table_replication, enable_peer, enable_table_replication, get_peer_config, list_peer_configs, list_peers, list_replicated_tables, remove_peer, remove_peer_tableCFs, set_peer_bandwidth, set_peer_tableCFs, show_peer_tableCFs, update_peer_config

  Group name: snapshots
  Commands: clone_snapshot, delete_all_snapshot, delete_snapshot, delete_table_snapshots, list_snapshots, list_table_snapshots, restore_snapshot, snapshot

  Group name: configuration
  Commands: update_all_config, update_config

  Group name: quotas
  Commands: list_quotas, set_quota

  Group name: security
  Commands: grant, list_security_capabilities, revoke, user_permission

  Group name: procedures
  Commands: abort_procedure, list_procedures

  Group name: visibility labels
  Commands: add_labels, clear_auths, get_auths, list_labels, set_auths, set_visibility

  Group name: rsgroup
  Commands: add_rsgroup, balance_rsgroup, get_rsgroup, get_server_rsgroup, get_table_rsgroup, list_rsgroups, move_servers_rsgroup, move_servers_tables_rsgroup, move_tables_rsgroup, remove_rsgroup, remove_servers_rsgroup

SHELL USAGE:
Quote all names in HBase Shell such as table and column names.  Commas delimit
command parameters.  Type <RETURN> after entering a command to run it.
Dictionaries of configuration used in the creation and alteration of tables are
Ruby Hashes. They look like this:

  {'key1' => 'value1', 'key2' => 'value2', ...}

and are opened and closed with curley-braces.  Key/values are delimited by the
'=>' character combination.  Usually keys are predefined constants such as
NAME, VERSIONS, COMPRESSION, etc.  Constants do not need to be quoted.  Type
'Object.constants' to see a (messy) list of all constants in the environment.

If you are using binary keys or values and need to enter them in the shell, use
double-quote'd hexadecimal representation. For example:

  hbase> get 't1', "key\x03\x3f\xcd"
  hbase> get 't1', "key\003\023\011"
  hbase> put 't1', "test\xef\xff", 'f1:', "\x01\x33\x40"

The HBase shell is the (J)Ruby IRB with the above HBase-specific commands added.
For more on the HBase Shell, see http://hbase.apache.org/book.html
hbase(main):002:0> status # 执行status
1 active master, 0 backup masters, 1 servers, 0 dead, 2.0000 average load

hbase(main):003:0> whoami # 执行whoami
root (auth:SIMPLE)
    groups: root, libvirt

hbase(main):004:0> list  # list
TABLE                                                                                   
0 row(s) in 0.0450 seconds

=> []
hbase(main):005:0> create # 建表，不会时，可以直接打 它会提示

ERROR: wrong number of arguments (0 for 1)

Here is some help for this command:
Creates a table. Pass a table name, and a set of column family
specifications (at least one), and, optionally, table configuration.
Column specification can be a simple string (name), or a dictionary
(dictionaries are described below in main help output), necessarily 
including NAME attribute. 
Examples:

Create a table with namespace=ns1 and table qualifier=t1
  hbase> create 'ns1:t1', {NAME => 'f1', VERSIONS => 5}

Create a table with namespace=default and table qualifier=t1
  hbase> create 't1', {NAME => 'f1'}, {NAME => 'f2'}, {NAME => 'f3'}
  hbase> # The above in shorthand would be the following:
  hbase> create 't1', 'f1', 'f2', 'f3'
  hbase> create 't1', {NAME => 'f1', VERSIONS => 1, TTL => 2592000, BLOCKCACHE => true}
  hbase> create 't1', {NAME => 'f1', CONFIGURATION => {'hbase.hstore.blockingStoreFiles' => '10'}}
  
Table configuration options can be put at the end.
Examples:

  hbase> create 'ns1:t1', 'f1', SPLITS => ['10', '20', '30', '40']
  hbase> create 't1', 'f1', SPLITS => ['10', '20', '30', '40']
  hbase> create 't1', 'f1', SPLITS_FILE => 'splits.txt', OWNER => 'johndoe'
  hbase> create 't1', {NAME => 'f1', VERSIONS => 5}, METADATA => { 'mykey' => 'myvalue' }
  hbase> # Optionally pre-split the table into NUMREGIONS, using
  hbase> # SPLITALGO ("HexStringSplit", "UniformSplit" or classname)
  hbase> create 't1', 'f1', {NUMREGIONS => 15, SPLITALGO => 'HexStringSplit'}
  hbase> create 't1', 'f1', {NUMREGIONS => 15, SPLITALGO => 'HexStringSplit', REGION_REPLICATION => 2, CONFIGURATION => {'hbase.hregion.scan.loadColumnFamiliesOnDemand' => 'true'}}
  hbase> create 't1', {NAME => 'f1', DFS_REPLICATION => 1}

You can also keep around a reference to the created table:

  hbase> t1 = create 't1', 'f1'

Which gives you a reference to the table named 't1', on which you can then
call methods.


hbase(main):006:0> create 'psn', 'f1'   # 建表 psn， 列族为f1
0 row(s) in 1.3760 seconds

=> Hbase::Table - psn
hbase(main):007:0> describe 'psn' # 看下表的描述
Table psn is ENABLED                                                                    
psn                                                                                     
COLUMN FAMILIES DESCRIPTION  # 列族描述                                                           
{NAME => 'f1', BLOOMFILTER => 'ROW', VERSIONS => '1', IN_MEMORY => 'false', KEEP_DELETED
_CELLS => 'FALSE', DATA_BLOCK_ENCODING => 'NONE', TTL => 'FOREVER', COMPRESSION => 'NONE
', MIN_VERSIONS => '0', BLOCKCACHE => 'true', BLOCKSIZE => '65536', REPLICATION_SCOPE =>
 '0'}                                                                                   
1 row(s) in 0.0470 seconds

hbase(main):008:0> 

```

列族描述： version, 版本号， TTL(time to live), 存活时间， BLCOCKCACEH 缓存，IN_MEMORY是否在内存，BLOCKSIZE 缓存块大小。

注意这个shell里删除要按住ctril+delete



####  Group name: dml
  Commands: append, count, delete, deleteall, get, get_counter, get_splits, incr, put, scan, truncate, truncate_preserve

delete 和 truncate的区别，delete 删除 可以事务回滚，truncate不可以。

```sh
# put
hbase(main):010:0> put 'psn', '11111','f1:name','xianming'
0 row(s) in 0.1020 seconds
hbase(main):011:0> put 'psn','22222','f1:name','xiaohong'
0 row(s) in 0.0120 seconds

# get
hbase(main):012:0> get 'psn','11111'
COLUMN                  CELL                                                            
 f1:name                timestamp=1596617518938, value=xianming                         
1 row(s) in 0.0230 seconds

hbase(main):013:0> put 'psn', '11111','f1:age','12'
0 row(s) in 0.0110 seconds
hbase(main):014:0> get 'psn','11111'
COLUMN                  CELL                                                            
 f1:age                 timestamp=1596617633337, value=12                               
 f1:name                timestamp=1596617518938, value=xianming                         
1 row(s) in 0.0050 seconds
hbase(main):015:0> get 'psn','22222'
COLUMN                  CELL                                                            
 f1:name                timestamp=1596617547009, value=xiaohong                         
1 row(s) in 0.0110 seconds

# scan
hbase(main):017:0> scan 'psn'
ROW                     COLUMN+CELL                                                     
 11111                  column=f1:age, timestamp=1596617633337, value=12                
 11111                  column=f1:name, timestamp=1596617518938, value=xianming         
 22222                  column=f1:name, timestamp=1596617547009, value=xiaohong         
2 row(s) in 0.0170 seconds # 注意是两行数据

# put 覆盖
hbase(main):018:0> put 'psn','22222','f1:name', 'zhiling'
0 row(s) in 0.0100 seconds

hbase(main):020:0> scan 'psn'
ROW                     COLUMN+CELL                                                     
 11111                  column=f1:age, timestamp=1596617633337, value=12                
 11111                  column=f1:name, timestamp=1596617518938, value=xianming         
 22222                  column=f1:name, timestamp=1596617715991, value=zhiling          
2 row(s) in 0.0080 seconds

# delete 删除
hbase(main):024:0> delete 'psn','22222','f1:name'
0 row(s) in 0.0050 seconds

hbase(main):025:0> scan 'psn'
ROW                     COLUMN+CELL                                                     
 11111                  column=f1:age, timestamp=1596617633337, value=12                
 11111                  column=f1:name, timestamp=1596617518938, value=xianming         
 22222                  column=f1:name, timestamp=1596617547009, value=xiaohong   #注意这里是xiaohong
2 row(s) in 0.0120 seconds

hbase(main):026:0> delete 'psn','22222','f1:name'

# truncate 'psn 删除整个表
```



####  Group name: namespace
  Commands: alter_namespace, create_namespace, describe_namespace, drop_namespace, list_namespace, list_namespace_tables

类似于库名

```sh
hbase(main):026:0> list_namespace
NAMESPACE                                                                               
default                                                                                 
hbase                                                                                   
2 row(s) in 0.0430 seconds

hbase(main):027:0> 
```

