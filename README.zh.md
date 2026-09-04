# Translation Workbench

[English](README.md) | 简体中文

Translation Workbench 是一个 Agent Skill，用于运行结构化翻译项目，覆盖原文准备、翻译起草、独立审核和用户主导的合并定稿。

当前版本：`0.1.1`

它适用于长文本或需要保持连续性的翻译工作：项目可以积累术语、人物或说话者信息、背景资料、起草笔记，并执行单独的审核。它不限于小说、特定语言组合或数字章节。

## 功能范围

本 skill 包含：

1. 初始化新项目，或接入已有资料；
2. 获取并核对原文；
3. 准备术语和本次翻译需要的上下文；
4. 完成整份译文初稿和起草笔记；
5. 在不修改初稿的情况下进行独立审核；
6. 由用户逐项决定并完成定稿。

它不包含发布、平台格式转换、Dashboard、统计分析或 subagent 调度。

内置的两个检查器只使用 Python 3 标准库。它们负责校验上下文交接和阶段边界，不负责判断文学质量。

## 支持的运行端

唯一的 skill 正本位于 `skills/translation-workbench/`，供 Codex 和 Claude Code 共同使用。

## 安装

推荐从 GitHub 安装：

```bash
npx skills add Alexu0317-FATHER/translation-workbench
```

明确指定同时安装到 Codex 和 Claude Code：

```bash
npx skills add Alexu0317-FATHER/translation-workbench -a codex -a claude-code
```

以上命令默认安装到当前项目。如需其他作用范围或安装方式，请按安装器提示选择。

也可以手动安装到项目：

- Codex：`.agents/skills/translation-workbench/`
- Claude Code：`.claude/skills/translation-workbench/`

请把同一份完整 skill 目录安装或复制到对应位置，不要分别维护两套翻译规则。

通过 skills CLI 管理的安装可以这样更新：

```bash
npx skills update translation-workbench
```

当问题只有少量明确选项时，skill 会优先使用当前运行端提供的结构化提问工具。Claude Code 可以使用 `AskUserQuestion`；Codex 在工具可用时可以使用 `request_user_input`。没有相应工具或问题需要开放式回答时，则使用普通对话。

## 调用方式

示例：

```text
使用 translation-workbench，根据这些文件建立一个翻译项目。
```

```text
$translation-workbench 开始为“渡口”这一节准备原文。
```

```text
/translation-workbench 继续审核第 4 章。
```

第一种写法依靠运行端根据 skill 名称和描述进行识别。Codex 通常使用 `$translation-workbench`，Claude Code 通常使用 `/translation-workbench`。

## 推荐的 session 使用方式

建议每个主要阶段使用单独的 session：

```text
原文准备 → 翻译 → 独立审核 → 合并定稿
```

每个 session 开始时，说明项目、翻译单元和本次阶段。例如：

```text
使用 translation-workbench。阅读本项目的 README，执行第 4 章的翻译流程。
```

一个阶段结束时，skill 会说明生成了哪些文件，并给出在新 session 中开始下一阶段的简短提示。这只是建议，不是强制的 session 规则。没有实测过的模型和超长 session 策略可能产生不同结果。

## 项目初始化

Skill 支持三种起点：

- 没有既有结构的新项目；
- 已有原文或参考资料，但需要整理；
- 已有翻译项目，并且需要保留当前目录结构。

对于新项目，skill 会根据内置模板创建项目 `README.md`。该 README 是项目入口，记录语言组合、作品或翻译单元、文件作用、项目资料和流程链接。

用户提供的 Word、Markdown、表格、PDF 或其他资料保持不变。当前运行端能够读取时，skill 会根据内置模板把相关内容整理成项目文档。只有资料冲突、无法可靠分类或涉及编辑取舍时才询问用户。

初始化时不会创建空白 glossary、人物、背景、来源或文风文件。只有用户提供了对应资料，或者项目第一次产生了需要长期保留的内容时，才创建相应文件。

## 示例成品

[浏览 Vermintide 同人翻译展示](showcase/index.html)。

展示目录包含一个章节索引、五篇已翻译的中英对照章节，以及页面实际引用的本地图片。它用于展示这套流程的真实产出，不会随 skill 一起安装。

原作文本和图片的权利仍归各自权利人所有。仓库的 MIT License 不授予 `showcase/` 下第三方素材的使用权；详见 [showcase/NOTICE.md](showcase/NOTICE.md)。

## Skill 正本结构

```text
skills/translation-workbench/
├─ SKILL.md
├─ agents/
│  └─ openai.yaml
├─ references/
│  ├─ project-initialization.md
│  ├─ sourcing.md
│  ├─ translation.md
│  ├─ independent-review.md
│  └─ finalization.md
├─ scripts/
│  ├─ check_translation_context.py
│  ├─ check_stage.py
│  └─ test_*.py
└─ assets/
   └─ templates/
```

版本记录见 [CHANGELOG.md](CHANGELOG.md)。本项目使用 [MIT License](LICENSE)。
