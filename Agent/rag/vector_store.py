#AI的知识库管理工具，要完成读取文件夹里的pdf或者txt,自动切片，转成向量存入向量库
#在进行MD5去重，最后提供检索接口供给AI查询答案

##RAG核心：文档加载--切片--存储--检索

import os.path

from langchain_chroma import Chroma
from langchain_core.documents import Document
from langchain_text_splitters import RecursiveCharacterTextSplitter

from Agent.utils.config_handler import chroma_conf
from Agent.utils.file_handler import txt_loader, pdf_loader, listdir_with_allowed_type, get_file_md5_hex
from Agent.utils.logger_handler import logger
from Agent.utils.path_tools import get_abs_path
from Agent.model.factory import embed_model



class VectorStoreService:
    def __init__(self):

        #创建本地向量数据库
        self.vector_store=Chroma(
            collection_name =chroma_conf["collection_name"],
            embedding_function = embed_model,
            persist_directory= get_abs_path(chroma_conf["persist_directory"]),  #数据存在哪个路径
        )
        #创建文本切片器（格式都在源码里）
        self.spliter=RecursiveCharacterTextSplitter(
            chunk_size=chroma_conf["chunk_size"],
            chunk_overlap=chroma_conf["chunk_overlap"],
            separators=chroma_conf["separators"],
            length_function=len,
        )

    #提供一个检索器，AI用它来查最相关的内容
    def get_retriever(self):
        #返回k条最相关的片段，也就是调用这个函数就可以检索并返回三条最相近的结果
        return self.vector_store.as_retriever(search_kwargs={"k": chroma_conf["k"]})


    #扫描文件夹--去重--读取--切片--入库--记录MD5
    def load_document(self):
        """
        从数据文件夹内读取数据文件，转为向量存入向量库
        要计算MD5的去重
        :return:None
        """

        #检查文件是否已经存在，如果存在就跳过，也就相当于去重
        def check_md5_hex(md5_for_check:str):
            if not os.path.exists(get_abs_path(chroma_conf["md5_hex_store"])):
                #创建一个空的MD5文件夹
                open(get_abs_path(chroma_conf["md5_hex_store"]),"w",encoding="utf-8").close()

                return False

            #打开MD5文件
            with open(get_abs_path(chroma_conf["md5_hex_store"]),"r",encoding="utf-8") as f:
                #逐行读取
                for lines in f.readlines():
                    #去掉换行空格
                    line=lines.strip()

                    if line==md5_for_check:
                        return True
                return False

        #打开文件--追加写入MD5
        def save_md5_hex(md5_for_check:str):
            with open(get_abs_path(chroma_conf["md5_hex_store"]),"a",encoding="utf-8") as f:
                f.write(md5_for_check+"\n")

        #判断是txt文件还是pdf,调用对应的加载函数
        def get_file_documents(read_path:str):
            if read_path.endswith("txt"):
                return txt_loader(read_path)
            if read_path.endswith("pdf"):
                return pdf_loader(read_path)

            return []

        #获取所有允许的文件，调用筛选文件函数
        allowd_files_path :list[str]=listdir_with_allowed_type(
            get_abs_path(chroma_conf["data_path"]),
            tuple(chroma_conf["allow_knowledge_file_type"]))


        for path in allowd_files_path:
            #获取文件的MD5，path传参进filepath，判断最终得到MD5值返回
            md5_hex=get_file_md5_hex(path)

            if check_md5_hex(md5_hex):
                logger.info(f"加载知识库{path}已经存在知识库内，跳过")
                continue

            try:
                #path传入read_path,由函数进行判断读取内容
                documents:list[Document]=get_file_documents(path)

                if not documents:
                    logger.warning(f"[加载知识库]{path}内没有有效文本内容，跳过")
                    continue
                  #把获取到的内容保存到split_document里
                split_document:list[Document]=self.spliter.split_documents(documents)

                if not split_document:
                    logger.warning(f"[加载知识库]{path}分片后没有有效文本内容，跳过")
                    continue
                #把切片存入向量库
                self.vector_store.add_documents(split_document)
                #保存MD5下次不再保存
                save_md5_hex(md5_hex)

                logger.info(f"[加载数据库]{path}内容加载成功")
            except Exception as e:
                logger.error(f"[加载知识库]{path}加载失败：{str(e)}",exc_info=True)
                continue

if __name__ == '__main__':
    vs=VectorStoreService()
    vs.load_document()
    retriever=vs.get_retriever()
    res=retriever.invoke("迷路")
    for r in res:
        print(r.page_content)
        print("-"*20)