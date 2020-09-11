



使用 git  时，有如下 warning: LF will be replaced by CRLF in XX的警告。

是因为在*Linux*下的换行符为LF，而*windows*下的换行符为 CRLF，所以在windows钟执行add . 时出现如上提示



### autocrlf

在不同平台上，换行符发生改变时，Git 会认为整个文件被修改，这就造成我们没法 `diff`，不能正确反映本次的修改。还好 Git 在设计时就考虑了这一点，其提供了一个 `autocrlf` 的配置项，用于在提交和检出时自动转换换行符，该配置有三个可选项：

- **true:** 提交时转换为 LF，检出时转换为 CRLF
- **false:** 提交检出均不转换
- **input:** 提交时转换为LF，检出时不转换

用如下命令即可完成配置：

```sh
# 提交时转换为LF，检出时转换为CRLF
git config --global core.autocrlf true

# 提交时转换为LF，检出时不转换
git config --global core.autocrlf input

# 提交检出均不转换
git config --global core.autocrlf false
```



### safecrlf

如果把 autocrlf 设置为 false 时，那另一个配置项 `safecrlf` 最好设置为 **ture**。该选项用于检查文件是否包含混合换行符，其有三个可选项：

- **true:** 拒绝提交包含混合换行符的文件
- **false:** 允许提交包含混合换行符的文件
- **warn:** 提交包含混合换行符的文件时给出警告

配置方法：

```sh
# 拒绝提交包含混合换行符的文件
git config --global core.safecrlf true

# 允许提交包含混合换行符的文件
git config --global core.safecrlf false

# 提交包含混合换行符的文件时给出警告
git config --global core.safecrlf warn
```



如果涉及到在多个系统平台上工作，推荐将 git 做如下配置：

```
$ git config --global core.autocrlf input
$ git config --global core.safecrlf true
```

**也就是让代码仓库使用统一的换行符(LF)，如果代码中包含 CRLF 类型的文件时将无法提交，需要用 `dos2unix` 或者其他工具手动转换文件类型**



### dos2unix

手动修改文件的换行符为LF,Windows 上 Git bash 客户端自带了该工具。其他系统上也可以安装该工具，例如 Ubuntu 上安装：

`sudo apt-get install dos2unix`

``` sh
# 转换单个文件
dos2unix test.sh
# 转换文件夹内的所有文件
find . -type f |xargs dos2unix
```



###  .gitattribute

您可以配置 *.gitattribute* 文件来管理 Git 如何读取特定仓库中的行结束符。 将此文件提交到仓库时，它将覆盖所有仓库贡献者的 `core.autocrlf` 设置。 这可确保所有用户的行为一致，而不管其 Git 设置和环境如何。

*.gitattributes* 文件必须在仓库的根目录下创建，且像任何其他文件一样提交。

*.gitattributes* 文件看上去像一个两列表格。

- 左侧是 Git 要匹配的文件名。
- 右侧是 Git 应对这些文件使用的行结束符配置。

以下是 *.gitattributes* 文件示例。 您可以将其用作仓库的模板：

```sh
# Set the default behavior, in case people don't have core.autocrlf set.
* text=auto

# Explicitly declare text files you want to always be normalized and converted
# to native line endings on checkout.
*.c text
*.h text

# Declare files that will always have CRLF line endings on checkout.
*.sln text eol=crlf

# Denote all files that are truly binary and should not be modified.
*.png binary
*.jpg binary
```

您会发现文件是匹配的—`*.c`, `*.sln`, `*.png`—用空格分隔，然后提供设置—`text`, `text eol=crlf`, `binary`。 我们将在下面介绍一些可能的设置。

- `text=auto` Git 将以其认为最佳的方式处理文件。 这是一个合适的默认选项。
- `text eol=crlf` 在检出时 Git 将始终把行结束符转换为 `CRLF`。 您应将其用于必须保持 `CRLF` 结束符的文件，即使在 OSX 或 Linux 上。
- `text eol=lf` 在检出时 Git 将始终把行结束符转换为 `LF`。 您应将其用于必须保持 LF 结束符的文件，即使在 Windows 上。
- `binary` Git 会理解指定文件不是文本，并且不应尝试更改这些文件。 `binary` 设置也是 `-text -diff` 的一个别名。



### 在更改行结束后刷新仓库

改。 Git 更改了行结束符，以匹配您的新配置。

为确保仓库中的所有行结束符与新配置匹配，请使用 Git 备份文件，删除仓库中的所有文件（`.git` 目录除外），然后一次性恢复所有文件。

1. 在 Git 中保存当前文件，以便不会丢失任何工作。

   ```shell
   $ git add . -u
   $ git commit -m "Saving files before refreshing line endings"
   ```

2. 添加回所有已更改的文件，然后标准化行结束符。

   ```shell
   $ git add --renormalize .
   ```

3. 显示已重写的标准化文件。

   ```shell
   $ git status
   ```

4. 将更改提交到仓库。

   ```shell
   $ git commit -m "Normalize all the line endings"
   ```