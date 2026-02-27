---
name: scraped-content-summary
description: >
  从 HackerNews hn_production 数据库获取最新爬虫内容，结合用户偏好异步筛选出最相关的条目，
  再异步调用 LLM 逐条总结，最终拼接生成一份文本报告。
---

# 抓取内容摘要

## 使用说明

按以下步骤执行本技能：

### 步骤 1 — 询问关注主题

使用 AskUserQuestion 工具询问：

```
今天你对哪些主题感兴趣？
```

选项（multiSelect: true）：
- AI 与 LLM（标签：AI, LLM, 机器学习, 机器人）
- 创业与商业（标签：创业, 风险投资, 融资, 金融, 市场, 加密货币）
- 技术与工程（标签：软件工程, 开源, 开发者工具, 研究, 科学, Arxiv）
- 政策与世界（标签：政治, 政策, 监管, 中国, 地缘政治）
- 产品与设计（标签：产品, 设计, UX, 职业, 效率）
- 媒体与观点（标签：社交媒体, 观点）
- 全部主题（不过滤）

### 步骤 2 — 打破砂锅问到底(必须等前一步执行完成才能继续)

用户选择主题后，逐步深挖用户当下最关心的具体方向。例如：
- 「你在 AI 方面最近关注的是模型训练、应用落地还是基础设施？」
- 「能举一个你近期特别想了解的具体问题或项目吗？」
- 「你是想看技术深度分析，还是行业动态快讯？」

目标：构建出一段精准的「用户当前关注描述」（约 3–5 句话），用于后续 LLM 筛选的上下文。

### 步骤 3 — 更新用户画像

将本次深挖得到的关注描述追加到 `user/user.md`，记录日期和内容。

### 步骤 4 — 将选择映射为标签

将用户选择的类别转换为逗号分隔的标签字符串：
- AI 与 LLM → `AI,LLM,Machine Learning,Robotics`
- 创业与商业 → `Startup,Venture Capital,Fundraising,Finance,Markets,Crypto`
- 技术与工程 → `Software Engineering,Open Source,Developer Tools,Research,Science,Arxiv`
- 政策与世界 → `Politics,Policy,Regulation,China,Geopolitics`
- 产品与设计 → `Product,Design,UX,Career,Productivity`
- 媒体与观点 → `Social Media,Opinion`
- 全部主题 → 完全省略 `--topics` 参数

### 步骤 5 — 运行脚本

将步骤 2 中得到的用户关注描述写入临时文件 `/tmp/user_focus.txt`，然后运行：

```bash
python3 <skill_dir>/scripts/fetch_and_summarize.py \
  --topics "<逗号分隔的标签>" \
  --user-focus /tmp/user_focus.txt \
  --output /tmp/scraped_report_$(date +%Y%m%d).md
```

若用户选择「全部主题」，则省略 `--topics`。

脚本的工作流程：
1. 从数据库获取最新 100 条爬虫记录
2. **异步筛选**：并发调用 LLM，结合用户画像和当前关注点，判断每条内容是否值得阅读，不符合的直接丢弃
3. **异步总结**：对筛选保留的内容，并发调用 LLM 生成中文摘要
4. 按主题聚合，拼接生成最终的 Markdown 报告

### 步骤 6 — 呈现报告

读取脚本输出的 Markdown 报告文件，将内容直接展示给用户。

---

## 参数参考

| 参数 | 默认值 | 说明 |
|------|--------|------|
| `--limit N` | 100 | 获取记录数量 |
| `--source NAME` | all | 按来源过滤 |
| `--output FILE` | `scraped_report.md` | 输出 Markdown 文件路径 |
| `--no-cache` | false | 跳过缓存，从数据库重新获取 |
| `--topics TAGS` | none | 逗号分隔的标签，用于提升相关度 |
| `--user-focus FILE` | none | 用户当前关注描述文件路径 |

## 来源

`hacker_news`, `twitter`, `arxiv`, `github_trending`, `hugging_face`, `discord`, `reddit`, `twitter_founder`, `podcast`, `wechat`, `rednote`
