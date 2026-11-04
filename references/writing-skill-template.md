# 写作 Skill 模板（Writing Skill Template）

> 用风格档案 `style_profile.yaml` 填充以下模板，产出一个独立的"仿 XX 风格写作"skill。
>
> 生成时：所有 `{{...}}` 占位符替换为风格档案里对应字段的内容；如果某字段在档案里为空，整段对应章节也要省略（不要留空占位符）。

---

## 生成的 skill 落盘位置

```
.claude/skills/
  write-as-{{profile_id}}/
    SKILL.md
    references/
      style_profile.yaml         # 原档案副本（让 skill 自包含）
```

skill 命名约定：`write-as-{profile_id}`（例如 `write-as-qbitai`、`write-as-zhihu-zhangjia`）。

---

## SKILL.md 模板

````markdown
---
name: write-as-{{profile_id}}
description: 以「{{display_name}}」的风格撰写文章。当用户提到"用{{display_name}}的风格写""模仿{{display_name}}""仿{{display_name}}风格"、或要求"按这个号的写法写一篇"且上下文涉及{{display_name}}时使用。也适用于用户给出一个主题/素材，希望生成{{display_name}}风格的{{sample_platforms_str}}文章。基于风格档案 schema {{schema_version}} 生成。
---

# 「{{display_name}}」风格写作

你现在以「{{display_name}}」的写作风格创作文章。所有规则都来自对该作者/账号 {{sample_count}} 篇样本的实证分析。

## 风格画像（200 字概括）

{{portrait}}

## 在开始之前

1. 读取 `references/style_profile.yaml` 获取完整风格档案
2. 跟用户确认：
   - **主题/素材**：写什么
   - **目标字数**（默认 {{tunables.length_target.default}} 字）
   - **风格强度** 0-1（默认 {{tunables.intensity.default}}，1=完全模仿连口头禅都上）
   - **正式度** 0-1（默认 {{tunables.formality.default}}）
   - **是否启用 emoji**（默认 {{tunables.emoji_enable.default}}）

---

## 一、标题撰写规则

**字数目标**：{{title_craft.avg_length}} 字左右，区间 {{title_craft.length_range}}。

**信息密度**：{{title_craft.info_density}}（{{title_craft.info_density_explanation}}）。

**可选公式**（按场景挑一个）：

{{#each title_craft.formulas}}
- **{{id}}（{{when_to_use}}）**：`{{pattern}}`
  - 样本例：{{example}}
{{/each}}

**情绪词库**（按强度从档案抽取，不要超出此清单）：
{{title_craft.emotion_words_list}}

**禁止**：
- 标题不要用"探析""浅谈""试论"等学术腔
- 不要使用档案 `forbidden` 列表里的元素

---

## 二、开篇手法

**第一句字数控制**：{{opening_craft.first_sentence_avg_chars}} 字以内。

**钩子选择**（按当前文章类型决定）：

{{#each opening_craft.hook_templates}}
- **{{hook}}**：`{{template}}`
  - 样本例：{{example}}
{{/each}}

**人称偏好**：
- "你/你们"使用：{{opening_craft.pronoun_usage.second_person}}
- "我们"使用：{{opening_craft.pronoun_usage.inclusive_we}}
- "我"使用：{{opening_craft.pronoun_usage.first_person_singular}}

**背景信息**：{{opening_craft.background_placement}}（early=前置铺垫；late=先抛结论再补背景）。

---

## 三、段落节奏

**单段平均句数**：{{rhythm.avg_sentences_per_paragraph}}。

**节奏序列参考**：`{{rhythm.rhythm_pattern}}`
- 字母含义：L=信息段、S=极短句独立成段、I=图片占位、Q=引用、H=小标题
- {{rhythm.rhythm_pattern_notes}}

**极短句使用率**：约 {{rhythm.short_paragraph_rate}}（即每 N 段就要有一段是"绝了。""炸了。"式的极短句）。

**小标题**：{{rhythm.uses_subheadings_decision}}
- 风格：{{rhythm.subheading_style.info_density}} 信息密度{{rhythm.subheading_style.has_emotion_note}}
- 样本例：{{rhythm.subheading_style.example}}

**图片位置**：{{rhythm.image_frequency}}（写作时用 `![](image-placeholder)` 标注预期插图位置）。

---

## 四、语言风格（最核心）

### 4.1 动词选择

**必须用力量型动词，至少 5 个不同的，从以下清单挑**：

{{#each language_style.power_verbs}}
- `{{verb}}`（替代"{{replaces}}"，强度 {{intensity}}/5，{{polarity}}）
  - 例：{{example}}
{{/each}}

**替换规则**：当你想用"批评""发布""很受欢迎"这类中性词时，**先查这张表**找力量替代。

### 4.2 语气色板

本风格共 {{language_style.tone_palette_count}} 档语气：

{{#each language_style.tone_palette}}
- **{{tone}}**（占比 {{ratio}}）：{{features}}，用于{{typical_context}}
{{/each}}

**切换规律**：
{{#each language_style.tone_transitions}}
- {{this}}
{{/each}}

**禁止档位**：{{forbidden_tones}}。

### 4.3 标点叙事

{{#each language_style.punctuation_rules}}
- **{{key}}**：{{function}}（密度 {{density}}）
{{/each}}

### 4.4 口头禅 / 惯用表达

**必须出现至少 3 个**（从以下清单选）：

{{#each language_style.signature_phrases}}
- `{{phrase}}`（用于：{{context}}）
{{/each}}

### 4.5 技术概念处理（如适用）

{{language_style.technical_concept_handling_block}}

### 4.6 自创词典

可以使用（不要滥用）：

{{#each language_style.custom_vocabulary}}
- `{{word}}` — {{meaning}}
{{/each}}

---

## 五、结尾模式

**首选结尾类型**：{{ending_craft.preferred_endings}}

**模板**：

{{#each ending_craft.ending_templates}}
- **{{type}}**：`{{template}}`
  - 样本例：{{example}}
{{/each}}

{{#if ending_craft.has_fixed_cta}}
**固定 CTA**：
```
{{ending_craft.fixed_cta_text}}
```
（如果用户的目标是同一平台发布，建议保留这段。如果是改编成其他平台，去掉。）
{{/if}}

---

{{#if scene_extras_block}}
## 六、场景特有规则

{{scene_extras_block}}
{{/if}}

---

## 七、禁区（任何情况下不要触碰）

{{#each forbidden}}
- {{this}}
{{/each}}

---

## 写作执行流程

1. **确认参数**：跟用户对齐主题、字数、强度、正式度、emoji
2. **选公式**：根据主题类型从"标题公式"选一个，先写标题
3. **构骨架**：按节奏序列 `{{rhythm.rhythm_pattern}}` 拟出段落骨架（标 L/S/I/Q/H）
4. **填血肉**：每段内容写出来，写完一段检查：
   - 是否用了力量型动词？
   - 这段属于哪个语气档？是否符合切换规律？
   - 标点是否符合本风格密度？
5. **植入口头禅**：通读时找 3+ 处自然插入 `signature_phrases`
6. **收尾**：按 `preferred_endings` 写结尾
7. **质检**（自查清单）：
   - [ ] 标题命中了某个公式
   - [ ] 第一句 ≤ {{opening_craft.first_sentence_avg_chars}} 字
   - [ ] 至少 3 个口头禅 / 自创词出现
   - [ ] 至少 5 个不同的力量型动词
   - [ ] 至少 1 个极短句独立成段
   - [ ] 语气切换有 ≥1 处
   - [ ] 禁区清单没踩
   - [ ] 字数在目标 ±15% 内

## 用户调节

如果用户希望调整：
- "再夸张一点" → 提升 intensity 到 0.9，多用情绪词和极短句
- "正经一点" → 提升 formality 到 0.6，减少调侃档语气，去掉自创词
- "短一点/长一点" → 调整 length_target
- "去掉 CTA" → 跳过 `ending_craft.fixed_cta_text`

## 引用风格档案

任何时候不确定某个细节怎么写，回到 `references/style_profile.yaml` 查具体字段。**不要凭印象瞎写**——这份档案是从真实样本里抽出来的，照着用准没错。
````

---

## 生成脚本逻辑（伪代码）

```python
def generate_writing_skill(profile_yaml_path, output_dir):
    profile = load_yaml(profile_yaml_path)
    
    # 1. 读模板
    template = load_template("writing-skill-template.md")
    
    # 2. 渲染（用 jinja2 或简单字符串替换）
    rendered = render(template, profile)
    
    # 3. 清理：删掉所有未填充的占位符行
    rendered = strip_empty_sections(rendered)
    
    # 4. 落盘
    skill_dir = output_dir / f"write-as-{profile['profile_id']}"
    skill_dir.mkdir(parents=True, exist_ok=True)
    (skill_dir / "SKILL.md").write_text(rendered, encoding="utf-8")
    
    # 5. 复制档案
    (skill_dir / "references").mkdir(exist_ok=True)
    copy(profile_yaml_path, skill_dir / "references" / "style_profile.yaml")
    
    return skill_dir
```

实际渲染时，由于 Markdown 模板里夹了不少 `{{#each}}` 这类伪 Jinja 控制流，**推荐的做法是让 Claude 在分析完毕后直接写出最终 SKILL.md**——而不是机械填充模板。Claude 把这份模板当"结构和风格说明书"，根据当前 profile 内容写一份对应版本即可。

---

## 关键约束（生成时务必遵守）

1. **不要保留未填充的占位符**——如果某字段空缺，整段对应章节删掉
2. **`description` 要写好**——这是触发 skill 的关键，必须包含"用 XX 风格""模仿 XX""仿 XX 风格"等高频触发词
3. **样例必须真实**——所有 `example` 字段必须是档案里来自原文的真实例子，不能编
4. **保持 SKILL.md 在 800 行以内**——太长会拖累加载
5. **质检清单不要漏**——每个生成的 skill 都要有自查清单，否则模型容易跑偏
