## Python 测试

### 测试代码的必要性

* 在预期状态下工作
* 确保对代码的改动
* 良好的测试需要业务代码模块化， 代码耦合度低。





### 内置测试模块

#### unittest



#### doctest



### 三方测试工具

#### py.test

##### TestCase

先来熟悉一个单词： assert：断言

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