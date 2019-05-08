Tags:[linux, linux_software]

## nginx

### 常用操作

* ngxin  -v  查看版本
* nginx    启动ngxin
* `nginx -s reload`    修改配置后重启加载生效， 这种方法重启，nginx在重启的时候不会中断服务，因为  nginx在启动后，会有一个master进程和多个worker进程，重启是会先生成新的worker进程去接受reload命令，等老的worker进程执行完毕，master进程在关闭他们，所以服务器不会中断。
* `nginx -s stop`   快速停止nginx 
* `ningx -s quit`   完整有序的停止nginx
* `ningx -t `   测试当前配置文件是正确

### 配置文件

井号注释

指令是以一个变量名开头(例如，worker_processes或pid),然后包含参数

所有指令以 ; 结尾

子指令以花括号包含

* daemon off|on  是否以守护进程的方式启动nginx，定位问题时设为off，正常环境为on

* worker_processes Nginx开启的进程数 
  
  * `worker_processes  1;`
  * `#worker_processes auto;`
  * 以下参数指定了哪个cpu分配给哪个进程，一般来说不用特殊指定。如果一定要设的话，用0和1指定分配方式。这样设就是给1-4个进程分配单独的核来运行，出现第5个进程是就是随机分配了.eg:
  * `#worker_processes 4     #4核CPU `
  * `#worker_cpu_affinity 0001 0010 0100 1000`

* worker_cpu_affinity  nginx 默认没有开启利用多核cpu配置的。需要此参数来充分利用多核cpu.
  
  ```nginx
  # 两核cpu，开启两个进程，
  # 01 10;表示开启两个进程，第一个进程对应着第一个CPU内核，第二个进程对应着第二个CPU内核。
  worker_processes     2;
  worker_cpu_affinity 01 10;
  
  worker_processes     4;
  worker_cpu_affinity 0001 0010 0100 1000;
  
  # 4核CPU, 开启两个进程
  # 0101表示开启第一个和第三个内核，1010表示开启第二个和第四个内核
  worker_processes     2;
  worker_cpu_affinity 0101 1010;
  ```

* worker_rlimit_nofile

* pid

#### 默认配置





#### 全局配置

```nginx

```

### 其他

#### 跨域

```
location / {
     add_header Access-Control-Allow-Origin https://192.168.18.58;
}
```

允许192.168.18.58 向本机访问。

#### 打印

在nginx中要想打印某个值，完全可以实现直接打印的效果，用不着借助第三方扩展，直接返回结果就好：

```nginx
server    {
    listen 80;
    server_name tmp.kaibuy.cn;
    index index.php;
    root  /home/web/blog/public/www;
    #error_page   404   /404.html;
    location / {
        default_type  text/plain;   
        set $str "This Host : ";
        return 200 "$str $http_host";
    }

    access_log off;
}
```

是指定以文本方式打印，如果不加这句，搞不好会以下载文件的方式出现。当然也可以指定为HTML。

`set $str "This Host : ";`设定一个变量

如果变量内容是单词，

也可以：`set $str MyValue;`，这种不带引号时，中间不能有空格即可。 

`return 200 "$str $http_host";`返回内容体，前面200是状态码，可以是任意符合HTML状态码的代码，这任意。
后面引号里的是两个变量，`$str`是刚才定义的变量，`$http_host`是nginx系统变量。

这儿也可以写成`return 200 $str$http_host;`

也就是不带引号，但变量之间要是连续的，不能有空格。

#### 获取cookie
