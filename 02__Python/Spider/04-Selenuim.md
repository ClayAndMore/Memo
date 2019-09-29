Tags:[python, spider]

### Ajax 数据爬取

直接模拟请求就可以



### 动态渲染页爬取

有些网站不只是有ajax, 或者ajax有很多加密参数。

我们为对于这种可以直接用模拟浏览器的方式来实现。



### Selenuim

自动化测试工具，模拟浏览器执行。

需要安装ChromeDriver, 其他浏览器需要其他的driver.

```python
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait

browser = webdriver.Chrome()
try:
    browser.get("https://www.baidu.com") #跳到百度
    input = browser.find_element_by_id('kw')
    input.send_keys('python') # 搜索python
    input.send_keys(Keys.ENTER) # 回车键
    wait = WebDriverWait(browser, 10)
    wait.until(EC.presence_of_element_located((By.ID, "content_left")))
    # 输出当前URL，当前的Cookies和网页源代码
    print(browser.current_url)
    print(browser.get_cookies())
    print(browser.page_source)
finally:
    browser.close()
```



#### 声明浏览器对象

Selenium支持非常多的浏览器，Chrome,Firefox, Edge等， 还有Android,BlackBerry等手机浏览器，

还支持无界面浏览器PhantomJS.

```python
from selenium import webdriver
browser = webdriver.Chrome()
browser = webdriver.Firefox()
browser = webdirver.Edge()
browser = webdirver.PhantomJS()
browser = webdirver.Safari()
```



#### 查找节点

单个节点：

```python
find_element_by_id
find_element_by_name
find_element_by_xpath # eg: find_element_by_xpath('//*[@id="q"]'), id = 'q'
find_element_by_link_text
find_element_by_tag_name
find_element_by_class_name
find_element_by_css_selector # eg:find_element_by_css_selector("#q"), id = 'q'
find_element_by_partial_link_text
```

上述通用方法： `find_element(查找方式By, value)`

eg: `find_element_by_id(id)` => `find_element(By.ID, id)`  

这种方式参数灵活，变动时不用改方法名。



多个节点：

上述单节点中所有方法名element -> elements,

 eg: `find_elements()`

eg: `find_elements(By.CSS_SELECTOR, '.service-bd li')`

返回的是一个对象列表.



如果查找不到节点的话会抛出NoSuchElementException异常。



#### 节点交互

让浏览器执行一些动作

send_keys() 输入文字

clear() 清空文字

click() 点击按钮

```python
# 打开淘宝，在搜索框输入iphone, 清空， 再输入ipad, 点击按钮搜索
from selenium import webdriver
import time
browser = webdriver.Chrome()
browser.get("https://www.taobao.com")
input = browser.find_element_by_id('q')
input.send_keys('iPhone')
time.sleep(1)
input.clear()
input.send_keys('iPad')
button = browser.find_element_by_class_name("btn-search")
button.click()
```



#### 动作链

有些动作没有特定的执行对象，如鼠标拖拽，键盘按键等，用另一种方式来执行，这就是动作链。





#### 执行js

某些操作，selenium API没有提供， 比如下拉进度条， 但它可以直接模拟运行js,

```python
from selenium import webdriver
browser = webdriver.Chrome()
browser.get("https://www.zhihu.com/explore")
browser.execute_script("window.scrollTo(0, document.body.scrollHeight)")
browser.execute_script('alert("To Bottom")')

```



#### 获取节点信息

Page_source属性可以获取网页的源代码，接着可以用解析库(Beautiful Soup 正则)等来获取信息。

但是selenium提供了自己的方式，也很方便：

* 获取属性

  get_attribute()来获取节点属性，前提是先选中这个节点。

  ```python
  logo = browser.find_element_by_id('zh-top-link-logo')
  print(logo.get_attribute('class'))
  ```

* 获取文本值 , 节点都有text属性。, 接上： logo.text

* id, logo.id

* location. 获取该节点在页面中的相对位置。

* tag_name, 标签名称 

* size, 获取节点大小，也就是宽高。



#### 切换Frame

有一种节点是iframe,是网页的子页面。 结构和外部的网页结构一致。

selenium默认是不能到子Frame获取节点的， 需要使用`switch_to.frame(id等)`来切换Frame.

切换到父Frame: `browser.switch_to.parent_frame()`



#### 延迟等待

页面的Ajax请求可能会很慢，导致页面没有完全加载出来，这时我们需要等待页面加载再获取节点。

* 隐式等待

  如果没有找到节点，超出设定时间后，抛出找不到节点的异常

  `browser.implicitly_wait(10)`,  默认为0s.

* 显式等待

  它指定了要查找的节点

  ```python
  from selenium.webdriver.support import expected_conditions
  wait = WebDriverWait(browser, 10)
  wait.until(expected_conditions.presence_of_element_located(By.ID, 'q'))
  ```

   等待条件

  | expected_conditions 条件    | 含义                   |
  | --------------------------- | ---------------------- |
  | presence_of_element_located | 节点出现，出入定位元组 |



#### 前进后退

Browser.back()

Browser.forward()



#### Cookies

* Browser.get_cookies()
* Browser.add_cookies({name: aaa, domain: zhihu})
* Browser.delete_all_cookies()



#### 选项卡

```python
import time
from selenium import webdriver
browser = webdriver.Chrome()
browser.get('http://www.baidu.com')
browser.execute_script('window.open()') # 开启一个新选项卡
print(browser.window_handles)
browser.switch_to_window(browser.window_handles[1]) #切换到新选项卡
browser.get('https://www.taobao.com')
time.sleep(1)
browser.switch_to_window(browser.window_handles[0]) # 回到原来的选项卡
```



api文档： https://selenium-python.readthedocs.io/





### phantomjs

PhantomJS 是一个无界面 、可脚本编程的 WebKit 浏览器引擎，它原生支持多 Web 标准 DOM
操作、 css 选择器、 JSON Canvas 以及 SVG

但是最新的selenium上已经警告要不支持phantomjs了，我们取而代之的是使用chrome的headless。



### 使用Headless Chrome

```python
#!/usr/bin/env python
# -*- coding:utf-8 -*-

from selenium import webdriver
from selenium.webdriver.chrome.options import Options

chrome_options = Options()
chrome_options.add_argument('--headless')
# --disable-gpu only on Windows
chrome_options.add_argument('--disable-gpu')
chrome_options.add_argument("window-size=1024,768")
# 解决：selenium.common.exceptions.WebDriverException: Message: unknown error: Chrome failed to start: exited abnormally
chrome_options.add_argument("--no-sandbox")

#chrome_options.add_argument('--disable-dev-shm-usage')  目前不明， 可以尝试加上

driver = webdriver.Chrome(chrome_options=chrome_options)
```





### 问题

centos7:

####  安装Chrome

`curl https://intoli.com/install-google-chrome.sh | bash`

https://intoli.com/blog/installing-google-chrome-on-centos/



#### cannot find Chrome binary

确认下载 chrome,和chromedirver

`driver = webdriver.Chrome(executable_path=/path/chromedirver)`



### failed to start: exited abnormally

`chrome_options.add_argument("--no-sandbox")`