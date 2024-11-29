# 甜品日记蛋糕店智能客服系统

## 项目背景

甜品日记是一家专注于定制化蛋糕的连锁品牌，随着业务规模的扩大，客服团队面临着以下挑战：
- 每天需要处理大量重复的客户咨询
- 非工作时间无法及时响应客户查询
- 客服人员对新品和促销活动的信息更新不及时
- 个性化蛋糕定制需求的沟通效率低



为解决这些问题，我们将开发一个基于 LangChain 和 RAG 技术的智能客服系统，提供 24/7 的自动化客服服务。

## 业务场景

系统将支持以下核心业务场景：

1. **产品信息查询**
   - 蛋糕品类、价格、规格查询
   - 新品推荐和促销活动介绍
   - 原材料和营养成分咨询

2. **订单服务**
   - 下单流程指导
   - 订单状态查询
   - 配送时间和范围查询
   - 支付方式咨询

3. **个性化推荐**
   - 基于场景的蛋糕推荐（生日、婚礼等）
   - 基于预算的产品推荐
   - 基于口味偏好的推荐

4. **售后服务**
   - 常见问题解答
   - 退换货政策咨询
   - 投诉建议处理

## 技术特点

- 基于最新的 LangChain 生态组件开发
  - langchain-core：核心功能组件
  - langchain-community：社区集成组件
  - langchain-openai：OpenAI模型集成
- 使用 LCEL (LangChain Expression Language) 构建RAG链
- 支持流式输出的对话响应
- 提供命令行和Web两种交互界面
- 支持异步处理和队列管理

## 培训目标

通过本项目实操，学员将掌握：

1. **RAG 系统开发全流程**
   - 文档处理和知识库构建
   - 向量存储的实现和优化
   - 检索策略的设计和调优
   - 提示词工程最佳实践

2. **LangChain 应用开发**
   - LCEL (LangChain Expression Language) 的使用
   - RunnableParallel 和 RunnablePassthrough 的应用
   - 异步处理和流式输出的实现
   - 错误处理和异常管理

3. **实用开发技能**
   - 项目结构设计
   - 代码模块化组织
   - 异常处理和日志记录
   - 性能优化方法

4. **系统集成能力**
   -  界面开发（Gradio or Streamlit）
   - 命令行工具开发
   - 多模块协同工作

## 项目结构

```
happyCake/
├── README.md           # 项目说明文档
├── requirements.txt    # 项目依赖
├── .env.example       # 环境变量示例
├── main.py            # 项目入口文件
├── knowledge_base/    # 知识库文档
├── src/               # 源代码
│   ├── chains/        # RAG链实现
│   ├── data/          # 数据处理模块
│   ├── utils/         # 工具函数
│   ├── cli/           # 命令行界面
│   └── web/           # Web界面
└── tests/             # 测试用例
```

## 技术栈

- Python 3.10+
- LangChain 生态
  - langchain>=0.1.0
  - langchain-community>=0.0.13
  - langchain-core>=0.1.12
  - langchain-openai>=0.0.5
- FAISS 向量数据库
- Gradio Web 框架
- OpenAI API

## 开始使用

1. 克隆项目并安装依赖：
```bash
git clone https://github.com/ssyzyg/happyCake.git
cd happyCake
pip install -r requirements.txt
```

2. 配置环境变量：
```bash
cp .env.example .env
# 编辑 .env 文件，填入必要的配置信息
```

3. 运行项目：
```bash
# 命令行模式
python main.py --mode cli

# Web界面模式
python main.py --mode web
```

## 注意事项

- 确保已安装所有依赖包的正确版本
- 确保环境变量配置正确
- 确保知识库目录下有有效的Markdown文档
- Web模式下默认使用7860端口

