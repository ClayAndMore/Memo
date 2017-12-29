## CURL





`-d = --data`

post 参数

`curl -d "user=xx&password=12345" url`

or:

`curl -d '{"username":"xyz","password":"xyz"}' url`

json 参数需要单引号括起来



post json文件

`curl --data @curl_post_apsc.json http://192.168.122.1/cloud3`



https

`curl --insecure https://localhost/your_site/login_page  `