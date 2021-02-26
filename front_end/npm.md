## npm

https://www.npmjs.cn/getting-started/what-is-npm/

npm是一个是开发者共享和管理模块（或者包）的命令行工具, 它由 JavaScript 代码编写，`npm` 是 Node.js 标准的软件包管理器。



###  安装和更新

去这里 https://nodejs.org/en/download/ 下载nodejs, 安装nodes时， npm会自动安装。

但是，npm比Node更新得更频繁。因此，请确保您拥有最新的版本。

再运行 `npm install npm@latest -g`. 更新最新的稳定版本。



### package.json

当开始一个新的项目时，npm 会生成一个`package.json`文件。

这个文件列出了你项目的包依赖。由于 npm 的包更新很频繁，`package.json`文件允许你指定依赖的版本。这样就能保证包的升级不会破坏你的项目。

npm 把包保存在一个名为`nodemodules`文件夹里。这些包可以通过两种方式安装：

1. *安装在全局的 root `node`*`modules`文件夹下，可以被所有的项目访问。
2. 安装在项目自己的`node_modules`文件夹下，只能被自己访问。


大部分开发者会倾向于后者，这样每一个项目都有一个完整的依赖库。



package.json 是任何 Node.js 项目或 npm 包的中心。

一个最小的 package.json 文件至少包含两个必须字段：name 和 version

``` json
{
	"name": "fcc-learn-npm-package-json",
    "version": "1.2",
	"author": "claymore",
	"description": "A project that does something awesome",
	"keywords": [ "descriptive", "related", "words" ],
    "license": "MIT",
	"dependencies": {
		"express": "^4.14.0"
	},
	"main": "server.js",
	"scripts": {
		"start": "node server.js"
	},
	"repository": {
		"type": "git",
		"url": "https://idontknow/todo.git"
	}
}
```

* author 指定了作者， description 指定了描述信息 。

* keywords 字段中使用相关的关键字描述项目。

* license 字段是你告知用户允许他们拿这个项目干什么的地方。 常见的开源协议是 MIT 和 BSD。如果你想了解更多适合你项目的许可证的信息，那么 http://choosealicense.com 是一个不错的网站。

* dependencies  则是管理依赖，“包名”：“版本”。

* 版本推荐使用语义化版本号：版本格式：`主版本号.次版本号.修订号`

  * 主版本号：当你做了不向下兼容的公共 API 修改，
  * 次版本号：当你添加了向下兼容的新功能，
  * 修订号：当你做了向下兼容的问题修正。

* 为了让 npm 依赖项更新到最新的修订版，你可以在依赖包的版本号前加一个波浪符号（~）。在 package.json 中，我们当前的 moment 依赖包更新规则是：仅使用特定版本（2.10.2），但我们想用它最新的 2.10.x 版本。

  例子：

  ```
  "some-package-name": "~1.3.8" 定义这个包允许使用的版本为 1.3.x。
  ```

* 如果使用插入符号（^）来替换版本号的前缀，那么 npm 可以安装的版本则是 2.x.x。

  例子：

  ```
  "some-package-name": "^1.3.8" 定义这个包允许使用的版本为 1.x.x。
  ```



#### 创建

有两种方式创建 package.json 文件：

``` sh
1. npm init
# 该命令会在当前目录创建一个package.json, 并以命令行的方式询问你所要补充的内容：
package name: (test)
version: (1.0.0)
description:
entry point: (index.js)
test command:
git repository:
keywords:
author:
license: (ISC)
About to write to E:\gitMyself\test\package.json:

{
  "name": "test",
  "version": "1.0.0",
  "description": "",
  "main": "index.js",
  "scripts": {
    "test": "echo \"Error: no test specified\" && exit 1"
  },
  "author": "",
  "license": "ISC"
}

2.  npm init -y 
# 该命令会创建一个默认的package.json: 
Wrote to E:\gitMyself\test\package.json:

{
  "name": "test",
  "version": "1.0.0",
  "description": "",
  "main": "index.js",
  "scripts": {
    "test": "echo \"Error: no test specified\" && exit 1"
  },
  "keywords": [],
  "author": "",
  "license": "ISC"
}

```



可以通过声明配置项来填写永久的配置：

```sh
npm set init.author.email "wombat@npmjs.com"
npm set init.author.name "ag_dubs"
npm set init.license "MIT"
```

描述字段：

如果包中没有描述字段，npm使用README的第一行，description可以帮助人们在搜索npm时找到你的包，所以在包中定制一个description绝对是非常有用的。



#### dependencies

除了dependencies属性还有devDependencies属性，如果不开发公用库包，这两个没有区别



#### 入口文件

 "main": "index.js",



#### scripts

可以定义一组可以运行的 node 脚本。

示例：

```json
"scripts": {
  "dev": "webpack-dev-server --inline --progress --config build/webpack.dev.conf.js",
  "start": "npm run dev",
  "unit": "jest --config test/unit/jest.conf.js --coverage",
  "test": "npm run unit",
  "lint": "eslint --ext .js,.vue src test/unit",
  "build": "node build/build.js"
}
```

这些脚本是命令行应用程序。 可以通过调用 `npm run XXXX` 或 `yarn XXXX` 来运行它们，其中 `XXXX` 是命令的名称。 例如：`npm run dev`。

可以为命令使用任何的名称，脚本也可以是任何操作。



### package-lock.json

node_modules 文件夹一般是不上传到git的，一般使用pacakge.json中规定版本，但是package.json的版本是模糊的，比如~0.13.0， ^0.13。

**原始的项目和新初始化的项目实际上是不同的。 即使补丁版本或次版本不应该引入重大的更改，但还是可能引入缺陷。**

所以使用`package-lock.json` 会固化当前安装的每个软件包的版本，解决上述问题。

**当运行 `npm install`时，`npm` 会使用这些确切的版本。**， 如果没有package-lock.json, npm install的时候则会生成一份。

`package-lock.json` 文件需要被提交到 Git 仓库，以便被其他人获取（如果项目是公开的或有合作者，或者将 Git 作为部署源）。





### 安装包

` npm install <package_name>`

安装指定版本：

```css
npm install xxx@1.2.0
```

上述命令执行之后将会在当前的目录下创建一个 `node_modules` 的目录（如果不存在的话），然后将下载的包保存到这个目录下。

如果存在 `package.json` 文件，则会在 `package.json` 文件中查找针对这个包所约定的[语义化版本规则]，然后安装符合此规则的最新版本。**但不会更改 package.json文件。**注意，会从 dependencies 和 devDependencies 中的依赖下载包。

在本地目录中如果没有 `package.json` 这个文件的话，那么最新版本的包会被安装。

#### --save

``` sh
npm install <package_name> --save 
# 会添加该包的信息到 package.json的dependencies,  --save 可以简写为 -S

npm install <package_name> --save-dev 
# 会到 devDependencies, 简写为 -D
```

安装后，就可以用 require 来 导入到程序中：

``` js
const _ = require('lodash')
```

若要查看所有已安装的 npm 软件包（包括它们的依赖包）的最新版本，则：

```bash
npm list
```

安装时显示进度 

npm i -d
npm i -dd
npm i -ddd



#### 全局包

npm install -g <package_name>

如果你想将其作为一个命令行工具，那么你应该将其安装到全局。这种安装方式后可以让你在任何目录下使用这个包。比如 grunt 就应该以这种方式安装。

查看全局包：

```cpp
npm list -g --depth 0
```

全局的位置到底在哪里？

`npm root -g` 命令会告知其在计算机上的确切位置。



#### 更新

在 `package.json` 文件所在的目录中执行 `npm update` 命令，则已安装的版本会被更新，并且 `package-lock.json` 文件会被新版本填充, **`package.json` 则保持不变。**



若要发觉软件包的新版本，则运行 `npm outdated`。

更新当前可更新的包可以用 `npm outdated` 命令。

``` sh
npm outdated
# 执行以上命令，可以看到所有可以更新的模块。
# 然后我们先更显 package.json 文件，需要安装"npm-check-updates"模块
npm install -g npm-check-updates
# 安装后，可以执行
ncu # npm-check-updates 
# ncu 会检测可更新的模块，然后执行
ncu -u  # 这会升级 package.json 文件的 dependencies 和 devDependencies 
npm update 
```

如果只是下载了项目还没有 `node_modules` 依赖包，并且想先安装新的版本，则运行：

```bash
npm install
```



#### 卸载

如需删除 node_modules 目录下面的包（package），请执行：

`npm uninstall <package>`:

```
npm uninstall lodash
```

如需从 `package.json` 文件中删除依赖，需要在命令后添加参数 `--save`:

```sh
npm uninstall --save lodash
```

注意：如果你将安装的包作为 "devDependency"（也就是通过 `--save-dev` 参数保存的），那么 `--save` 无法将其从 `package.json` 文件中删除。所以必须通过 `--save-dev` 参数可以将其卸载。

如果要卸载全局包：

``` sh
npm uninstall -g <package_name>
```



### 查看包

``` sh
# 远程包
npm info <packageName>

# 查看本地安装的包版本号
npm ls <pacakgeName> //本地包
npm ls <packageName> -g // 全局安装包
```





### 源

``` sh
npm config set registry https://registry.npm.taobao.org
# 使用 git bash 配置后 会出现一个 ~/.npmrc 文件
 
# 查看npm源地址
npm config get registry

# 临时使用
npm --registry https://registry.npm.taobao.org install express
```





### npx

https://www.ruanyifeng.com/blog/2019/02/npx.html

http://nodejs.cn/learn/the-npx-nodejs-package-runner