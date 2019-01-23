

#### rm后的文件恢复

`grep -a -B 50 -A 60 'some string in the file' /dev/sda1 > results.txt`

说明：

- 关于grep的-a意为–binary-files=text，也就是把二进制文件当作文本文件。
- -B和-A的选项就是这段字符串之前几行和之后几行。
- /dev/sda1，就是硬盘设备，
- \> results.txt，就是把结果重定向到results.txt文件中。







### 待补充

```
/proc/pid/cmdline
```