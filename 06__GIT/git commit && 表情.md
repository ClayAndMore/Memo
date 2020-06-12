`git commit` 时，提交信息遵循以下格式：

```
:emoji1: :emoji2: 不超过 50 个字的摘要，首字母大写，使用祈使语气，句末不要加句号

提交信息主体

引用相关 issue 或 PR 编号 <#110>
```

初次提交示例：

```
git commit -m ":tada: Initialize Repo"
```



### emoji  表情

| emoji             | emoji 代码                    | commit 说明           |
| ----------------- | ----------------------------- | --------------------- |
| 🎉 (庆祝)          | `:tada:`                      | 初次提交              |
| 🆕 (全新)          | `:new:`                       | 引入新功能            |
| 🔖 (书签)          | `:bookmark:`                  | 发行/版本标签         |
| 🐛 (bug)           | `:bug:`                       | 修复 bug              |
| 🚑 (急救车)        | `:ambulance:`                 | 重要补丁              |
| 🌐 (地球)          | `:globe_with_meridians:`      | 国际化与本地化        |
| 💄 (口红)          | `:lipstick:`                  | 更新 UI 和样式文件    |
| 🎬 (场记板)        | `:clapper:`                   | 更新演示/示例         |
| 🚨 (警车灯)        | `:rotating_light:`            | 移除 linter 警告      |
| 🔧 (扳手)          | `:wrench:`                    | 修改配置文件          |
| ➕ (加号)          | `:heavy_plus_sign:`           | 增加一个依赖          |
| ➖ (减号)          | `:heavy_minus_sign:`          | 减少一个依赖          |
| ⬆️ (上升箭头)      | `:arrow_up:`                  | 升级依赖              |
| ⬇️ (下降箭头)      | `:arrow_down:`                | 降级依赖              |
| ⚡ (闪电) 🐎 (赛马) | `:zap:` `:racehorse:`         | 提升性能              |
| 📈 (上升趋势图)    | `:chart_with_upwards_trend:`  | 添加分析或跟踪代码    |
| 🚀 (火箭)          | `:rocket:`                    | 部署功能              |
| ✅ (白色复选框)    | `:white_check_mark:`          | 增加测试              |
| 📝 (备忘录) 📖 (书) | `:memo:` `:book:`             | 撰写文档              |
| 🔨 (锤子)          | `:hammer:`                    | 重大重构              |
| 🎨 (调色板)        | `:art:`                       | 改进代码结构/代码格式 |
| 🔥 (火焰)          | `:fire:`                      | 移除代码或文件        |
| ✏️ (铅笔)          | `:pencil2:`                   | 修复 typo             |
| 🚧 (施工)          | `:construction:`              | 工作进行中            |
| 🗑️ (垃圾桶)        | `:wastebasket:`               | 废弃或删除            |
| ♿ (轮椅)          | `:wheelchair:`                | 可访问性              |
| 👷 (工人)          | `:construction_worker:`       | 添加 CI 构建系统      |
| 💚 (绿心)          | `:green_heart:`               | 修复 CI 构建问题      |
| 🔒 (锁)            | `:lock:`                      | 修复安全问题          |
| 🐳 (鲸鱼)          | `:whale:`                     | Docker 相关工作       |
| 🍎 (苹果)          | `:apple:`                     | 修复 macOS 下的问题   |
| 🐧 (企鹅)          | `:penguin:`                   | 修复 Linux 下的问题   |
| 🏁 (旗帜)          | `:checkered_flag:`            | 修复 Windows 下的问题 |
| 🔀 (交叉箭头)      | `:twisted_rightwards_arrows:` | 分支合并              |