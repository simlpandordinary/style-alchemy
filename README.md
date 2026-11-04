# 写作风格蒸馏 Style Alchemy

> **[style-alchemy](https://github.com/simlpandordinary/style-alchemy)** —— 飞书《WorkBuddy 视频系列 · 全技能与提示词总目录》里推荐的开源技能，已拆分为独立仓库分发（一个技能一个仓库）。

| 项 | 内容 |
| - | - |
| 上游仓库 | <https://github.com/snowmays/style-alchemy> |
| 上游路径 | `仓库根目录（技能本体即仓库根）` |
| 上游协议 | MIT |
| 上游 Star | 47 |
| 拆分方式 | 仅抽取该技能自身文件，独立可用 |

## 技能说明

文章风格深度分析（通用版，不限平台）。当用户想研究某个作者/账号/媒体的写作风格、拆解爆款套路、对比不同账号风格差异、或想"一键生成模仿某风格的写作 skill"时使用。触发场景包括："帮我分析这个公众号的风格"、"研究下这些文章的写法"、"拆解这个大V的套路"、"对比这两个号"、"我想学习XX的写作风格"、"基于这些样本做个仿写技能"。即使用户只是说"帮我看看这些文章"或"研究下这个号"，如果提供了多篇文章样本，也应触发。适用于公众号、知乎、小红书、Twitter/X、博客、学术期刊、个人散文、新闻媒体等任意中长文样本。

## 目录结构

```
├── .gitignore
├── LICENSE
├── README.en.md
├── SKILL.md
├── scripts/
└── normalize_samples.py
├── references/
├── analysis-framework.md
├── sample-format.md
├── style-profile-schema.md
└── writing-skill-template.md
└── assets/
└── banner.png
```

- `SKILL.md` 是技能入口（触发条件 / 工作流 / 约束），安装时必须位于技能根目录。
- `references/`、`scripts/`、`assets/` 为该技能自带的参考文档、脚本与素材。
- `README.upstream.md` 为上游仓库原始说明，保留出处与版权信息。
- `LICENSE` 为上游许可证原件。

## 安装

WorkBuddy 技能目录为 `~/.workbuddy/skills/style-alchemy/`：

```bash
git clone https://github.com/simlpandordinary/style-alchemy.git ~/.workbuddy/skills/style-alchemy
```

也可以直接对 AI 说：「把 <https://github.com/simlpandordinary/style-alchemy> 装成 Skill」。

安装后用自然语言触发，例如「写作风格蒸馏 Style Alchemy」「用 style-alchemy 帮我处理这个任务」。

## 版权

原始作者与版权归上游仓库 `snowmays/style-alchemy` 所有。本仓库仅做独立分发与结构整理，未修改技能内容；商用请遵循上游许可证。
