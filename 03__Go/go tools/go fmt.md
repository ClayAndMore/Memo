---
title: "go fmt.md"
date: 2020-09-11 19:01:02 +0800
lastmod: 2020-09-11 19:01:02 +0800
draft: false
tags: ["go 语法"]
categories: ["go"]
author: "Claymore"

---





### gofmt

gofmt命令参数列表如下：

```bash
usage: gofmt [flags] [path ...]
  -cpuprofile string
        write cpu profile to this file
  -d    display diffs instead of rewriting files
  -e    report all errors (not just the first 10 on different lines)
  -l    list files whose formatting differs from gofmt's
  -r string
        rewrite rule (e.g., 'a[b:len(a)] -> a[b:]')
  -s    simplify code
  -w    write result to (source) file instead of stdout
```



### go  fmt

```bash
usage: go fmt [-n] [-x] [packages]

Fmt runs the command 'gofmt -l -w' on the packages named
by the import paths. It prints the names of the files that are modified.
For more about gofmt, see 'go doc cmd/gofmt'.
For more about specifying packages, see 'go help packages'.
The -n flag prints commands that would be executed.
The -x flag prints commands as they are executed.
To run gofmt with specific options, run gofmt itself.

See also: go fix, go vet.
```

go fmt命令本身只有两个可选参数-n和-x，-n仅打印出内部要执行的go fmt的命令，-x命令既打印出go fmt命令又执行它，如果需要更细化的配置，需要直接执行gofmt命令。

go fmt在调用gofmt时添加了-l -w参数，相当于执行了`gofmt -l -w`。

