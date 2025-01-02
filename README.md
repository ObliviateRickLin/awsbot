# AWS文档QA助手

这是一个基于Streamlit和LangChain开发的智能问答系统，专门用于解答AWS相关文档问题。该系统能够智能理解和回答用户关于AWS的各类问题，并提供准确的文档引用。

## 功能特点

- 📚 基于AWS官方文档的智能问答
- 🤖 使用GPT-4模型进行智能对话
- 💡 提供准确的文档引用和页码
- 🔍 支持上下文理解和对话记忆
- 🌐 友好的Web界面

## 技术栈

- Streamlit：Web应用框架
- LangChain：大语言模型应用框架
- OpenAI GPT-4：语言模型
- FAISS：向量数据库
- PyPDF：PDF文档处理

## 安装步骤

1. 克隆项目
```bash
git clone https://github.com/ObliviateRickLin/awsbot.git
cd awsbot
```

2. 安装依赖
```bash
pip install -r requirements.txt
```

3. 配置环境变量
创建`.env`文件并添加以下配置：
```
OPENAI_API_KEY=你的OpenAI API密钥
```

4. 运行应用
```bash
streamlit run app.py
```

## 使用说明

1. 启动应用后，系统会自动加载AWS文档
2. 在对话框中输入你的AWS相关问题
3. 系统会基于文档内容提供详细回答，并标注参考来源
4. 支持连续对话，系统会记住对话上下文

## 注意事项

- 请确保已安装所有依赖包
- 需要有效的OpenAI API密钥
- 确保`aws-overview.pdf`文件存在于项目根目录 