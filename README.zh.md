# Translation Workbench

[English](README.md) | 简体中文

这是一套适合项目级翻译的 Agent Skill：依靠AI 起草、审核、记录等流程，提炼你的翻译风格，最重要的是，即便译者的源语言没有那么好，也能在这套技能的帮助下写出高质量的翻译。

![一句话的 AI 初稿、审核建议与我的定稿译文](docs/draft-vs-final.jpg)

出自[第 04 章《低语号的下落》](https://alexu0317-father.github.io/franz-lohners-chronicle-zh/franz-lohners-chronicle/chapters/04-the-fate-of-grungnis-whisper/output/index.html)，AI 起草，我定稿。

当前版本：`0.1.1`

## 功能特性

- 让AI承担对源语言的理解。我认为译文的好坏取决于译者双语的水平，技能要求AI不仅仅提供翻译译文，而且给出翻译依据，以此来弥补译者源语言的掌握深度。
- 让AI学习你的翻译风格，且持续优化，并在项目中长期保持一致性。
- 这套技能来源于[我的个人兴趣翻译项目](https://alexu0317-father.github.io/franz-lohners-chronicle-zh/)，历时两周、迭代 54 次，流程跑通之后才固化成技能。

## 一个例子

[第 01 章《布鲁亨多夫的老男爵》](https://alexu0317-father.github.io/franz-lohners-chronicle-zh/franz-lohners-chronicle/chapters/01-old-baron/output/index.html)由我手译，独立审核指出一处理解错误：

> **原文**　if there was an hour's worth of light in the sky before the storms closed in, you were doing well.
>
> **我的初稿**　如果在暴风雪来临前天空还有一小时的光亮就好了。
>
> **审核指出**　`you were doing well` 的落点是苦中作乐的庆幸——有这点光就算走运——不是初稿那种没能实现的惋惜，意思正好反了。判断依据是句式：英文这里是过去时的真实条件句，讲的是那个冬天确实时不时会有的光景；要表达「要是……就好了」，英文得用虚拟语气写成 `if there had been…, it would have been…`。上文刚说完牧师冻死在布道坛上，庆幸也比惋惜更接得上。

这类判断Google Translate/DeepL 不会提供。原句里每个词我都认识，结果它们在上下文里合起来我就不知道怎么翻译了。（引用的英文原句版权归 Fatshark 所有。）

## 安装指南

推荐从 GitHub 安装。默认装到当前项目：

```bash
npx skills add Alexu0317-FATHER/translation-workbench
```

加 `-g` 改为装到用户账户下，这样每个项目都能用。加 `-a` 指定装到哪些 agent：

```bash
npx skills add Alexu0317-FATHER/translation-workbench -a codex -a claude-code
```

项目级安装会把技能放在 `.agents/skills/translation-workbench/`，再让各 agent 自己的目录指向它，Claude Code 就是 `.claude/skills/`；加 `-g` 则在你的用户主目录下同样来一遍。也可以手动安装：把本仓库的 `skills/translation-workbench/` 复制到 Codex 的 `.agents/skills/` 或 Claude Code 的 `.claude/skills/`，装到用户级就在路径前加 `~/`。更新已安装的版本，`-p` 只更新项目级，`-g` 只更新全局：

```bash
npx skills update translation-workbench
```

调用示例：

```text
使用 translation-workbench，根据这些文件建立一个翻译项目。
```

Codex 里点名技能：

```text
$translation-workbench 开始为"渡口"这一节准备原文。
```

Claude Code 里用斜杠命令：

```text
/translation-workbench 继续审核第 4 章。
```

## 使用流程

| 阶段 | 人需要做什么 | AI做什么 |
|---|---|---|
| 初始化 | 告诉AI这是新项目、接入已有材料，还是继续某个已命名的翻译单元 | 确认既有的项目 README（如果存在）或创建项目 README，向你确认既有目录结构 |
| 材料准备 | 提供所有你可以提供的资料 | 核对原文完整与来源，逐个搜索既有术语，标出本单元的新词，建立相关文档 |
| 翻译 | 1. 下达翻译指令；2. 审核AI提供的新增术语词汇；3. 等AI产出 | 向人类确认术语表、人物卡等信息，产出翻译初稿和起草笔记 |
| 独立审核 | 下达独立审核指令，等AI产出 | 根据原文、术语表、人物卡、风格文档审核初稿，产出 `review-notes.md` |
| **合并定稿** | 1. 审核译文；2. 针对 AI 给出的 review notes 给予答复；3. 告诉AI 翻译理由；4. 决定哪些结论值得沉淀进项目文档 | 1. 逐项确认用户意见，写入 review notes；2. 确认定稿译文，以及经用户确认的术语表／人物档案／风格文档更新；3. 提炼值得沉淀的内容交由用户裁决；4. 产出 markdown 文档 |

每个阶段开始前会检查前置条件是否齐备。材料没备齐、术语还没裁完、已有的审核笔记会被覆盖，流程都会停下来告诉你缺什么。

## 让技能更好用的秘诀

1. 如果可以的话，提供几份你的翻译样章，可以帮助AI在翻译之前理解你的风格。
2. 在**翻译流程**中，审核AI提交的术语表、人物卡时，思考哪些值得长期统一的写入术语表——那些只在单章成立的记录不要让AI写进术语表或人物卡。项目越往后，一份精炼的表格收益越大。
3. 在**合并定稿**阶段，不要只告诉AI你的翻译结论，告诉AI你为什么这么想。 **你的思考过程是AI提炼译文风格最重要的依赖。**
4. 每个阶段用单独的 session，这样能让各阶段上下文更干净。 目前仅有**独立审核**流程通常无需人工干预，可以使用subagent执行。

## 跑完一章后的项目结构

```text
你的翻译项目/
├─ README.md                  # 项目入口：语言、翻译单元、文件角色
├─ <某个翻译单元>/
│  ├─ source.md                 # 原文工作副本（文件名由项目决定）
│  ├─ sourcing-handoff.json     # 材料准备到翻译的交接内容
│  ├─ <译文标题>.md              # 定稿译文
│  ├─ drafting-notes.md         # 起草笔记
│  └─ review-notes.md           # 审核笔记
├─ glossary.md                 # 术语表
├─ character-profiles.md       # 人物档案
├─ translator-style.md         # 译者风格
├─ background-notes.md         # 背景资料
└─ sources.md                  # 来源清单
```

空文件不会预先建好。只有真的产生了对应内容，skill 才会创建这些文件。

## 实测范围与限制

- 目前只验证过一个语言对（英译中）、一类文本（连载小说）。欢迎用于其他题材、其他语言以及其他文体进行测试，反馈请提 [Issue](https://github.com/Alexu0317-FATHER/translation-workbench/issues)。
- 翻译所使用的模型是 Opus 5 和 GPT-5.6 Sol。其他模型未进行测试。
- 检查器只依赖 Python 标准库。
- CI 在 Python 3.11 上验证。

## 成品、来源与许可

用这套流程做的完整项目——《弗兰兹·洛纳编年史》中文翻译——仓库在 [franz-lohners-chronicle-zh](https://github.com/Alexu0317-FATHER/franz-lohners-chronicle-zh)，在线阅读见 [https://alexu0317-father.github.io/franz-lohners-chronicle-zh/](https://alexu0317-father.github.io/franz-lohners-chronicle-zh/)。中英对照的网页由我另外的构建脚本生成，不是这个 skill 的产出；skill 到用户确认的定稿 Markdown 和一套笔记文件为止。

本项目使用 [MIT License](LICENSE)。版本记录见 [CHANGELOG.md](CHANGELOG.md)。
