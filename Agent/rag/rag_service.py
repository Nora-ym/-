"""
总结服务类：用户提问，搜索相关参考资料，将提问和参考资料提交给模型，让模型总结回复
"""
from langchain_core.documents import Document
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import PromptTemplate

from Agent.model.factory import chat_model
from Agent.utils.prompt_loader import load_rag_prompts
from Agent.rag.vector_store import VectorStoreService

def print_prompt(prompt):
    print("="*20)
    print(prompt.to_string())
    print("="*20)
    return prompt

class RagSummarizeService(object):
    def __init__(self):
        #创建的向量库工具
        self.vector_store=VectorStoreService()
        self.retriever=self.vector_store.get_retriever()
        #加载RAG专用提示词，读取一下提示词的意思
        self.prompt_text=load_rag_prompts()
        #创建一个带空位的提示词的模板，后面会把input和context填进去
        self.prompt_template=PromptTemplate.from_template(self.prompt_text)
        #
        self.model=chat_model
        self.chain=self.__init__chain()

    #构建链
    def __init__chain(self):
        chain=self.prompt_template | print_prompt| self.model | StrOutputParser()
        return chain
    #
    #查资料返回结果
    def retriever_docs(self,query:str)->list[Document]:
        return self.retriever.invoke(query)
    #最终的回答
    #将结果拼接传给模型，返回模型回答
    #最终留给外界的接口，最后只需调用这个方法传进来问题（也就是query）
    def rag_summarize(self,query:str)->str:
        context_docs=self.retriever_docs(query)
        #要把所有的资料拼成一段文字，因为模型不能接受列表，只能接受一整段文字
        context= ""
        counter=0
        for doc in context_docs:
            counter+=1
            context+=f"[参考资料{counter}]：参考资料内容：{doc.page_content} | 参考元数据：{doc.metadata}\n"

        return self.chain.invoke(
            {
                "input":query,
                "context":context,
            }
        )

if __name__ == '__main__':
    rag=RagSummarizeService()
    print(rag.rag_summarize("小户型适合哪款扫地机器人"))