https://ts.xcatliu.com/basics/primitive-data-types.html



TypeScript是微软公司开发的一款开源的JavaScript超集语言，任何JavaScript都是合法的TypeScript代码！

意思就是TypeScript的语法中包含了当前所有的JavaScript语法。



### 安装

```text
npm i typescript -g
```

以上命令会在全局环境下安装 `tsc` 命令，安装完成之后，我们就可以在任何地方执行 `tsc` 命令了。

编译一个 TypeScript 文件很简单：

```bash
tsc hello.ts
# helloworld.ts => helloworld.js
```

我们约定使用 TypeScript 编写的文件以 `.ts` 为后缀，用 TypeScript 编写 React 时，以 `.tsx` 为后缀。



### 数据类型

JavaScript 的类型分为两种：原始数据类型（[Primitive data types](https://developer.mozilla.org/en-US/docs/Glossary/Primitive)）和对象类型（Object types）。

原始数据类型包括：布尔值、数值、字符串、`null`、`undefined` 以及 ES6 中的新类型 [`Symbol`](http://es6.ruanyifeng.com/#docs/symbol) 和 [`BigInt`](https://developer.mozilla.org/zh-CN/docs/Web/JavaScript/Reference/Global_Objects/BigInt)。

```
let a: number = 10;  
let b: number = NaN;  
let c: number = Infinity;
let d: number = 0xA12;   //十六进制数字 
let e: number = 0b1010101;  //二进制数字
let f: number = 0o75;  //八进制数字

```



