```
流                             本 地 套 接 字                             流
入           用 户 空 间         X           X                            出
数          +-----------------X------+------X-----------+               数
据           内 核 空 间      X       |       X                          据
包                        X      前 |后       X                         包
 +                      X       半 |半        X                         +
 |                     X        场 |场         X                        |
 |                filter          |          filter                    |
 |                INPUT           |          OUTPUT                    |
 |                  ^             |             ^                      |
 v                  |             |             |                      v
                    ++            +             +
 网 +> nat      +-> 路 由 决 策 +--->filter +--->路 由 决 策 +---> nat     +->  网
 卡    PREROUTING                FORWARD                   POSTROUTING  卡

```

