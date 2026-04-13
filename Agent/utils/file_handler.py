import hashlib
import os.path
from langchain_community.document_loaders import PyPDFLoader, TextLoader
from langchain_core.documents import Document
from Agent.utils.logger_handler import logger


#获取文件的MD5的十六进制字符串,先查看是否存在或者格式是否正确
def get_file_md5_hex(filepath:str):

    if not os.path.exists(filepath):
        logger.error(f"[md5]文件{filepath}不存在")
        return
    if not os.path.isfile(filepath):
        logger.error(f"[md5]路径{filepath}不是文件")
        return

#创建一个md5计算器对象
    md5_obj=hashlib.md5()
#4kb数据
    chunk_size=4096
    try:
        #以二进制只读模式打开文件
        with open(filepath,"rb") as f:
            #循环读4kb直到读完
            while chunk := f.read(chunk_size):
                md5_obj.update(chunk)
            md5_hex=md5_obj.hexdigest()
            return md5_hex
    except Exception as e:
        logger.error(f"计算文件{filepath}md5失败，{str(e)}")
"""
:= 
chunk=f.read(chunk_size)
while chunk:
md5_obj.update(chunk)
chunk=f.read(chunk_size)
"""
#返回文件夹内的文件列表（允许的文件后缀）
def listdir_with_allowed_type(path:str,allowed_type:tuple[str]):
    files=[]
#不是文件夹直接退出
    if not os.path.isdir(path):
        logger.error(f"[listdir_with_allowed_type]{path}不是文件夹")
        return allowed_type

    #遍历文件夹的所有名字，
    #如果是以指定后缀结尾的话，把文件夹路径和文件名拼成完整的路径
    for f in os.listdir(path):
        if  f.endswith(allowed_type):
            files.append(os.path.join(path,f))
    return tuple(files)



def pdf_loader(filepath:str,password=None) ->list[Document]:
    return PyPDFLoader(filepath,password).load()




def txt_loader(filepath:str) ->list[Document]:
    return TextLoader(filepath,encoding="utf-8").load()