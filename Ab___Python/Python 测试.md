Tags:[python]

## Python 测试

### 测试代码的必要性

* 在预期状态下工作
* 确保对代码的改动
* 良好的测试需要业务代码模块化， 代码耦合度低。



####  assert：断言

判断 语句后面是否True，否者抛出AssertionError异常

```python
>>> assert 1>2
Traceback (most recent call last):
  File "<stdin>", line 1, in <module>
AssertionError
```

可自定义具体错误信息：

```python
>>> assert isinstance(a,(unicode)), 'hhhhhhhh'
Traceback (most recent call last):
  File "<stdin>", line 1, in <module>
AssertionError: hhhhhhhh
```





### 内置测试模块

#### unittest

##### 结构

库的整体结构：

unittest库提供了test cases, test suites, test fixtures，test runner：

1. **test case** ：通过继承TestCase类，我们可以创建一个test，或者一组tests，包括测试前准备环境的搭建(setUp)，执行测试代码(run)，以及测试后环境的还原(tearDown)。
2. **test suites** ： 测试套件,多个测试用例集合在一起,TestSuite也可以嵌套TestSuite。
3. **test fixtures** ： setup + test case + teardown结构
4. **TestLoader**:用来加载TestCase到TestSuite中，其中的方法从各个地方寻找TestCase，创建它们的实例，然后add到TestSuite中，返回一个TestSuite实例。
5. **test runner**：执行测试用例，其中的run()会执行TestSuite/TestCase。
6. **TextTestResult**：测试的结果会保存到TextTestResult实例中，包括运行用例数，成功数，失败数。



写好TestCase  --> 由TestLoader加载TestCase到TestSuite --> 由TextTestRunner来运行TestSuite

运行的结果保存在TextTestResult中，整个过程集成在unittest.main模块中。





##### 断言方法

assertEqual(a,b，[msg]):               断言a和b是否相等，相等则测试用例通过。

assertNotEqual(a,b，[msg]):         断言a和b是否相等，不相等则测试用例通过。

assertTrue(x，[msg])：                  断言x是否True，是True则测试用例通过。

assertFalse(x，[msg])：                 断言x是否False，是False则测试用例通过。

assertIs(a,b，[msg]):                      断言a是否是b，是则测试用例通过。

assertNotIs(a,b，[msg]):               断言a是否是b，不是则测试用例通过。

assertIsNone(x，[msg])：             断言x是否None，是None则测试用例通过。

assertIsNotNone(x，[msg])：      断言x是否None，不是None则测试用例通过。

assertIn(a,b，[msg])：                   断言a是否在b中，在b中则测试用例通过。

assertNotIn(a,b，[msg])：            断言a是否在b中，不在b中则测试用例通过。

assertIsInstance(a,b，[msg])：    断言a是是b的一个实例，是则测试用例通过。

assertNotIsInstance(a,b，[msg])：断言a是是b的一个实例，不是则测试用例通过。



msg=’测试失败时打印的信息’



##### 执行结果

```
.
----------------------------------------------------------------------
Ran 1 test in 0.000s

OK
```

一个点表示一个用例执行通过

OK 表示测试通过

FAIL 表示测试不通过，控制台输出断言异常信息

ERROR 表示测试异常





##### TestCase

```python
import unittest
class TestStringMethods(unittest.TestCase):
    """初始化和清理测试环境，比如创建临时的数据库，文件和目录等，其中 setUp() 和    		setDown() 是最常用的方法, 会自动执行。
    """
    def setUp(self):
        # Do something to initiate the test environment here.
        pass

    def tearDown(self):
        # Do something to clear the test environment here.
        pass
    @unittest.skip('先不执行')  # 忽略某个测试函数装饰器
    def test_upper(self):
        self.assertEqual('foo'.upper(),'FOO')
    def test_isupper(self):
        self.assertEqualTure('FOO'.isupper())
        self.assertFalse('Foo'.isupper())
    def test_split(self):
        s = 'hello world'
        self.assertEqual(s.split(),['hello','world'])
        with self.assertEqualRaise(TypeError):
            s.slipt(2)
if __name__ == '__main__': #unittest.main：为测试提供了入口。
    unittest.main() 
```

**所有的测试函数以test开头，test_XXX**

`unittest.skip()`: 装饰器，当运行用例时，有些用例可能不想执行等，可用装饰器暂时屏蔽该条测试用例。一种常见的用法就是比如说想调试某一个测试用例，想先屏蔽其他用例就可以用装饰器屏蔽。

* `@unittest.skip(reason): skip(reason)`装饰器：

  无条件跳过装饰的测试，并说明跳过测试的原因。

* `@unittest.skipIf(reason): skipIf(condition,reason)`装饰器：

  条件为真时，跳过装饰的测试，并说明跳过测试的原因。

* `@unittest.skipUnless(reason): skipUnless(condition,reason)`装饰器：

  条件为假时，跳过装饰的测试，并说明跳过测试的原因。

* `@unittest.expectedFailure(): expectedFailure()`测试标记为失败。





##### TestSuite

组织多个测试套件：

```python
import unittest
from test_case import test_baidu
from test_case import test_youdao

#构造测试集
suite = unittest.TestSuite()
suite.addTest(test_baidu.BaiduTest('test_baidu'))
suite.addTest(test_youdao.YoudaoTest('test_youdao'))

if __name__=='__main__':
    #执行测试
    runner = unittest.TextTestRunner()
    runner.run(suite)
```

构造测试集：

```python
 test_dir = './'
 discover = unittest.defaultTestLoader.discover(test_dir, pattern='test_*.py')
 runner=unittest.TextTestRunner()
 #使用run()方法运行测试套件（即运行测试套件中的所有用例）
 runner.run(discover)   
```





##### unittest命令

```
使用方法
python -m unittest 选项

示例,查看帮助信息
python -m unittest -h

-v, --verbose 查完整的测试结果输出信息
-q, --quiet 查看最小测试结果输出信息
-f, --failfast 在第一次遇到失败时，停止测试
-c, --catch 捕获control-C并显示结果
-b, --buffer 将stdout, stderr信息输出到buffer中
```

执行 testdemo.py 文件所有的测试用例：

```
$ python -m unittest testdemo
```

执行 testdemo.py 文件的 TestStringMethods 类的所有测试用例：

```
$ python -m unittest test_demo.TestStringMethods
```

执行 testdemo.py 文件 TestStringMethods 类的 test_upper：

```
$ python -m unittest test_demo.TestStringMethods.test_upper
```



Test  Discovery

nittest 提供了自动匹配发现并执行测试用例的功能，随着项目代码结构越发庞大，势必有多个测试文件，自动匹配发现并测试用例的功能在此就显得非常有用，只要满足 [load_tests protocol](https://docs.python.org/2/library/unittest.html#load-tests-protocol) 的测试用例都会被 unittest 发现并执行，测试用例文件的默认匹配规则为 test*.py

```
python -m unittest discover
```

参数如下：

```
-v, --verbose
Verbose output

-s, --start-directory directory
Directory to start discovery (. default)

-p, --pattern pattern
Pattern to match test files (test*.py default)

-t, --top-level-directory directory
Top level directory of project (defaults to start directory)
```

假设现在要被测试的代码目录如下：

```
$ tree demo
demo
├── testdemo.py
└── testdemo1.py
$ python -m unittest discover -s demo -v
test_isupper (testdemo.TestStringMethods) ... ok
test_upper (testdemo.TestStringMethods) ... ok
test_is_not_prime (testdemo1.TestPrimerMethods) ... ok
test_is_prime (testdemo1.TestPrimerMethods) ... ok

----------------------------------------------------------------------
Ran 4 tests in 0.001s

OK
```





#### doctest







### 三方测试工具

#### py.test

##### TestCase

```python
import unittest

from collections import Counter

class TestCounter(unittest.TestCase):
    def setUp(self):
        self.c = Counter('abcdaba')
        print 'setUp starting.....'

    def test_basics(self):
        c = self.c
        self.assertEqual(c, Counter(a=3, b=2, c=1, d=1))
        self.assertIsInstance(c, dict)
        self.assertEqual(len(c), 4)
        self.assertIn('a', c)
        self.assertNotIn('f', c)
        self.assertRaises(TypeError, hash, c)

    def test_update(self):
        c = self.c
        c.update( f=1 )
        self.assertEqual(c, Counter(a=3, b=2, c=1, d=1, f=1))
        c.update(a=10)
        self.assertEqual(c, Counter(a=13, b=2, c=1, d=1, f=1))

    def tearDown(self):
        print 'tearDown starting...'

if __name__ == '__main__':
    unittest.main()
```



* setUp , 测试前的准备工作，常用来做一些初始化, 非必须方法。
* tearDown,  测试后的销毁工作， 非必训方法。
* unittest.TestCase, 顾名思义，测试用例。
* test_xxx,  每个测试用例都有很多测试方法，要以test_开头。
* self.assertXXX ,  断言，如果为Ture，测试通过，False抛出AssertionError异常,测试框架就认为此测试用例失败。

运行结果：

```
setUp starting.....
tearDown starting...
.setUp starting.....
tearDown starting...
.
----------------------------------------------------------------------
Ran 2 tests in 0.001s

OK
```



注意： 每次运行test_方法时前后都要运行setUp和tearDown,

如果测试不通过，会提示具体出现异常位置的信息。



##### TestSuite

另一个常用的功能是测试套件 unittest.TestSuite(),  将一组测试用例作为一个测试对象：

ut_suite.py:

```python
接上：
if __name__ == '__main__':
    #unittest.main()
    suite = unittest.TestSuite()
    # suite.addTest(TestCounter()) 添加实例
    # 更细粒度的划分：
    suite.addTest(TestCounter('test_basics'))
    suite.addTest(TestCounter('test_update'))
    runner = unittest.TextTestRunner()
    runner.run(suite)
```






#### doctest

查找代码文件里文档字符串的交互式会话部分，执行那些验证代码工作是否正常：





### 自动化测试

#### Robot Framework

TDD模式： Test  Driven Development ， 测试驱动开发。

ATDD模式： Acceptance Test Driven Development ,  验收测试驱动开发。



TDD只涉及到Developer（开发者），只能算个人工作方式的改变。而现代软件开发，往往都是“产品经理（或业务）、测试人员（或QA）、开发人员”三者合作的成果，如果开发人员对业务需求理解的不正确，那么写出的测试用例也是错的，这个问题是TDD解决不了的。



整个团队（包括上面提到的三方成员）在开发工作开始之前，一起讨论、制定每个任务（或者用户故事）的验收标准，并提取出一组验收测试用例。这么做好处在于：

1. 大家一起讨论验收标准和测试用例保证了对业务需求一致的理解。（这一点实际是所有开发环节中都需要关注的问题）
2. 通过形成测试用例，使标准成为可执行的内容，而不是虚的指标。

国内公司一般项目开发进度很紧，大部分公司开发和测试工作由不同的人来负责，完全照搬TDD流程来开发成本过高。我更建议开发人员使用自动化测试技术编写验收测试用例，只要验收测试用例能够跑通了，就可以提交测试。



robot 则是ATDD模式。