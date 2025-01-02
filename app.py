import streamlit as st
from langchain_community.document_loaders import PyPDFLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter 
from langchain_openai import OpenAIEmbeddings
from langchain_community.vectorstores import FAISS
from langchain_community.chat_models import ChatOpenAI
from langchain.memory import ConversationBufferMemory
from langchain.chains import ConversationalRetrievalChain
from dotenv import load_dotenv
import os
from langchain.prompts import PromptTemplate

# 加载环境变量
load_dotenv()

# 设置页面标题
st.set_page_config(page_title="AWS文档QA助手")
st.title("AWS文档QA助手")

# 初始化session state
if "conversation" not in st.session_state:
    st.session_state.conversation = None

if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

# 加载PDF
@st.cache_resource
def load_and_process_pdf():
    # 直接加载本地PDF文件
    loader = PyPDFLoader("aws-overview.pdf")
    pages = loader.load()
    
    # 分割文本
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=1000,
        chunk_overlap=200
    )
    splits = text_splitter.split_documents(pages)

    # 创建向量存储
    embeddings = OpenAIEmbeddings()
    vectorstore = FAISS.from_documents(splits, embeddings)
    
    return vectorstore

# 加载文档并创建向量存储
try:
    vectorstore = load_and_process_pdf()
    
    # 如果conversation还没有初始化,创建对话链
    if st.session_state.conversation is None:
        llm = ChatOpenAI(temperature=0.7, model_name="gpt-4o-mini")
        memory = ConversationBufferMemory(
            memory_key="chat_history",
            return_messages=True
        )
        
        # Add custom prompt template
        template = """基于以下内容回答问题。如果你不知道答案，就说你不知道，不要试图编造答案。
        
        相关文档内容:
        {context}
        
        问题: {question}
        
        请在回答的最后，工整地列出支持你回答的具体文档原文，并给出文档的页码。
        
        回答:"""
        
        st.session_state.conversation = ConversationalRetrievalChain.from_llm(
            llm=llm,
            retriever=vectorstore.as_retriever(),
            memory=memory,
            combine_docs_chain_kwargs={'prompt': PromptTemplate(
                input_variables=["context", "question"],
                template=template
            )}
        )
except Exception as e:
    st.error(f"加载文档时出错: {str(e)}")

# 用户输入
if prompt := st.chat_input("请输入您关于AWS的问题"):
    if st.session_state.conversation is None:
        st.error("系统初始化失败!")
    else:
        try:
            # 获取回答
            response = st.session_state.conversation({"question": prompt})
            st.session_state.chat_history.append((prompt, response['answer']))
        except Exception as e:
            st.error(f"处理问题时出错: {str(e)}")

# 显示对话历史
for user_query, bot_response in st.session_state.chat_history:
    st.chat_message("user").write(user_query)
    st.chat_message("assistant").write(bot_response) 