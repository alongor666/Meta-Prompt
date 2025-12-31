# Meta Prompt Builder - Claude网页版安装指南

## 📋 文件说明

本目录包含以下文件：

1. **meta-prompt-builder-for-claude-web.md** ⭐
   - Claude.ai网页版专用的整合版本
   - 包含完整的5个模板和工作流程
   - **这是你需要上传到Claude.ai的主文件**

2. **skill.md**
   - Claude Code CLI版本的技能定义
   - 用于本地Claude Code命令行工具

3. **README.md**
   - 详细的使用指南和示例
   - 包含ROI计算和最佳实践

4. **references/** 目录
   - 5个独立的模板文件（已整合到网页版中）

---

## 🚀 在Claude.ai网页版安装步骤

### 方法1: 创建专用项目（推荐）

1. **登录Claude.ai**
   - 访问 https://claude.ai
   - 登录你的账号

2. **创建新项目**
   - 点击左侧边栏的 "Projects"
   - 点击 "+ New Project"
   - 项目名称: `Meta Prompt Builder`

3. **添加自定义指令**
   - 在项目设置中找到 "Custom Instructions"
   - 复制 `meta-prompt-builder-for-claude-web.md` 的全部内容
   - 粘贴到 "Custom Instructions" 文本框中
   - 点击 "Save"

4. **开始使用**
   - 在该项目的对话中输入：
   ```
   使用Meta Prompt Builder: 我需要评估一个AI客服系统，预算200万
   ```
   - Claude会自动按照Meta Prompt Builder的工作流程生成定制化Prompt

### 方法2: 上传为知识文件

1. **在现有对话中上传**
   - 打开任意Claude对话
   - 点击附件图标（📎）
   - 上传 `meta-prompt-builder-for-claude-web.md`

2. **每次使用时引用**
   ```
   参考上传的Meta Prompt Builder文档，帮我生成一个Prompt：
   我需要评估一个AI客服系统，预算200万
   ```

---

## 💡 使用示例

### 示例1: 商业决策

**你输入**:
```
使用Meta Prompt Builder: 评估智车睿控的网约车风控方案，预算500万，2周决策
```

**Claude会**:
1. 识别为"商业决策类"任务
2. 推断你是"决策者"角色
3. 检测缺少"输出对象"信息
4. 提问1-2个关键问题（如：报告给谁看？）
5. 生成完整的商业决策深度分析Prompt

### 示例2: 学习场景

**你输入**:
```
使用Meta Prompt Builder: 学习网约车保险风控，我是保险新人
```

**Claude会**:
1. 识别为"学习研究类"任务
2. 推断你是"新手"水平
3. 选择"学习知识萃取"模板
4. 可能问：学习目标是理解概念还是建立体系？
5. 生成定制化的学习分析Prompt

### 示例3: 技术评估

**你输入**:
```
使用Meta Prompt Builder: 评估是否采用微服务架构，团队10人，技术栈Java
```

**Claude会**:
1. 识别为"技术分析类"任务
2. 提取约束（团队10人、Java技术栈）
3. 选择"技术可行性评估"模板
4. 可能问：系统规模多大？实施时限？
5. 生成技术评估Prompt

---

## 🎯 使用技巧

### 技巧1: 越具体越好
❌ "使用Meta Prompt Builder: 分析这个方案"
✅ "使用Meta Prompt Builder: 我是CTO，2周内决定是否投200万采购这个系统"

### 技巧2: 说明约束条件
❌ "使用Meta Prompt Builder: 评估方案"
✅ "使用Meta Prompt Builder: 快速评估，今天汇报，重点关注ROI和合规"

### 技巧3: 明确受众
❌ "使用Meta Prompt Builder: 做个分析"
✅ "使用Meta Prompt Builder: 给董事会的报告，需要数据支撑"

### 技巧4: 允许迭代
```
你: 使用Meta Prompt Builder: 评估XX方案
Claude: [生成Prompt]
你: 太复杂了，简化版本，只保留核心框架
Claude: [生成简化版]
```

---

## ⚙️ 高级用法

### 组合多个模板

```
使用Meta Prompt Builder: 评估技术方案，同时识别风险，快速决策
```

Claude会融合多个模板:
- 核心: 技术可行性评估
- 增强: 风险识别
- 约束: 快速决策模式

### 指定特定框架

```
使用Meta Prompt Builder: 分析这个商业方案，重点用SCQA和逆向思考
```

### 自定义输出格式

```
使用Meta Prompt Builder: 评估XX，输出格式为1页摘要+5页详细分析
```

---

## 📊 适用场景判断

### ✅ 什么时候用？

1. **任务复杂度高**
   - 多维度分析需求
   - 决策影响重大

2. **重复性任务**
   - 每月分析多份方案
   - 希望标准化流程

3. **不确定如何提问**
   - 新手不知道问什么
   - 跨领域任务

4. **质量要求高**
   - 向董事会汇报
   - 需要可复现流程

### ❌ 什么时候不用？

1. 简单查询（"Python语法是..."）
2. 创意发散（头脑风暴）
3. 即时响应（聊天对话）
4. 你已明确知道要用什么框架

---

## 🔧 故障排查

### 问题1: Claude没有按Meta Prompt Builder执行

**解决**:
- 确保在开头明确写 `使用Meta Prompt Builder:`
- 如果用的是"方法2"（上传文件），需要明确说"参考上传的文档"

### 问题2: 生成的Prompt太复杂

**解决**:
```
简化版本，只保留核心框架
```

### 问题3: 生成的Prompt不符合需求

**解决**:
1. 提供更多背景信息
2. 明确说明期望输出
3. 指定使用的模板类型

---

## 💰 ROI参考

假设每月分析20份商业方案:

**不用Meta Prompt Builder**:
- 每份设计Prompt: 30分钟
- 往返修改: 30分钟
- 总耗时: 20小时/月

**使用Meta Prompt Builder**:
- 每份生成: 5分钟
- 修改: 5分钟
- 总耗时: 3.3小时/月

**节省**: 16.7小时/月 ≈ 200小时/年 ≈ 25个工作日

---

## 📞 需要帮助？

如果遇到问题：

1. **检查文件内容**: 确保完整复制了 `meta-prompt-builder-for-claude-web.md`
2. **使用正确格式**: `使用Meta Prompt Builder: [需求]`
3. **提供足够上下文**: 角色、目标、约束
4. **迭代优化**: 第一次生成不满意可以要求调整

---

## 🎓 核心原理

Meta Prompt Builder基于5大原则:

1. **Context Precision（上下文精确性）**
   - 精确捕获用户角色、目标、约束

2. **Constraint-Driven（约束驱动）**
   - 用约束条件定义输出边界

3. **Comparative Reasoning（对比推理）**
   - 提供多种对比维度（横向/纵向/基准）

4. **Layered Output（分层输出）**
   - 分层设计输出（摘要→详细→清单）

5. **Gap Highlighting（盲区提示）**
   - 明确标注需验证和需补充的信息

---

## ✨ 开始使用

1. 按照上述"方法1"或"方法2"完成安装
2. 在Claude对话中输入：
   ```
   使用Meta Prompt Builder: [你的需求描述]
   ```
3. 跟随Claude的引导，回答1-3个问题
4. 获得定制化的高质量分析Prompt

**祝使用愉快！** 🚀

---

**版本**: v1.0
**最后更新**: 2025-12-31
**适用于**: Claude.ai网页版 / Claude for Slack / Claude API
