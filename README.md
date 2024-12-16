# Teaching Assistant with LLM

一个基于LLM的教学辅助工具，用于文档解析、审阅和评估。

## 功能特点

- 跨平台支持 (Windows & MacOS)
- 支持多种文档格式
  - Markdown/TXT文件解析
  - PDF文档处理（可选）
- 多模态支持
  - 文本处理
  - 图片分析
  - 代码评估
  - 数学公式解析
- 多种LLM模型支持 (OLLAMA/OpenAI)
- 自动评分系统
- 友好的用户界面 (Gradio)

## 项目结构

```
teaching-with-llm/
├── src/
│   ├── config.py          # 配置文件
│   ├── parser.py          # 文档解析（包含MD和PDF）
│   ├── llm.py            # LLM模型接口
│   ├── evaluator.py      # 评分系统
│   └── app.py            # Gradio界面
├── tests/
│   └── test_basic.py     # 基础测试
├── requirements.txt       # 项目依赖
└── README.md             # 项目说明文档
```
- `config.py`: 包含所有配置项
- `parser.py`: 处理所有文档解析相关功能
- `llm.py`: 统一管理LLM模型接口
- `evaluator.py`: 处理评分相关功能
- `app.py`: 提供用户界面

