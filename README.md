# 一个简单的Agent的项目
_提前声明：只是练手的非常简单的可实现的小小小小项目，想要做大的可以自行扩展_

## 一、项目描述及思路
面向消费者的智能客服系统，为用户提供全周期的扫地机器人相关服务。

（1）智能问答服务：
- 处理购买前的产品咨询（如功能、价格、对比）。
- 解决购买后的使用问题（如操作指导、故障处理、维护建议）。
- 基于RAG技术，从知识库中检索准确信息并生成自然语言回答，确保响应及时且可靠。

（2）使用报告与优化建议生成
- 针对已购买用户，自动分析扫地机器人的使用数据（如清洁频率、耗材状态、错误日志等）。
- 生成个性化报告，总结使用情况并提供优化建议（如清洁计划调整、部件更换提醒等）。
- 支持用户主动查询报告或系统定期推送，帮助用户最大化产品价值。


## 二、技术栈
Python, LangChain, LangGraph, Chroma, Streamlit, 通义千问, OpenAI API
## 三、项目结构
```
agent/
├── tools/                     # 智能体工具集合
│   ├── agent_tools.py         # 自定义工具（ragsummarize, get_user_location 等）
│   ├── middleware.py          # 中间件（日志、限流、上下文处理）
│   └── react_agent.py         # ReAct 智能体核心逻辑
├── config/                    # 配置管理（YAML/JSON配置）
├── data/                      # 数据目录（知识库文档、临时文件）
├── model/                     # 模型工厂
│   └── factory.py             # 模型实例化工厂（Chat, Embedding）
├── prompts/                   # 提示词模板目录
├── rag/                       # RAG 检索增强模块
│   ├── rag_service.py         # RAG 服务主逻辑
│   └── vector_store.py        # 向量库封装（Chroma）
├── utils/                     # 工具函数集合
│   ├── chain_debug.py         # LangChain 调试工具
│   ├── config_handler.py      # 配置加载与解析
│   ├── file_handler.py        # 文件读写（PDF, TXT）
│   ├── logger_handler.py      # 日志记录
│   ├── path_tools.py          # 路径处理
│   └── prompt_loader.py       # 动态加载提示词模板
├── routes.py                  # API 路由（若作为Web服务）
└── .gitignore
|__ app.py
```
附加架构图
<img width="6403" height="3117" alt="整体架构图" src="https://github.com/user-attachments/assets/540b3d14-2533-4dbe-b457-faeba8bfc761" />

## 四、

