from venv import logger

from Agent.utils.config_handler import prompts_conf
from Agent.utils.path_tools import get_abs_path

#从配置读路径->转成绝对路径->读取文本内容->出错要打印日志
def load_system_prompts():
    try:
        system_prompts_path =get_abs_path(prompts_conf["main_prompt_path"])
    except KeyError as e:
        logger.error(f"[load_system_prompts]在yaml配置项中没有main_prompt_path配置项")
        raise e

    try:
        return open(system_prompts_path,"r",encoding="utf-8").read()  #一次性全部读完
    except Exception as e:
        logger.error(f"[load_system_prompts]解析系统提示词出错,{str(e)}")
        raise e


def load_rag_prompts():
    try:
        rag_prompts_path =get_abs_path(prompts_conf["rag_summarize_prompt_path"])
    except KeyError as e:
        logger.error(f"[load_rag_prompts]在yaml配置项中没有rag_summarize_prompt_path配置项")
        raise e

    try:
        return open(rag_prompts_path,"r",encoding="utf-8").read()
    except Exception as e:
        logger.error(f"[load_rag_prompts]解析RAG总结提示词出错,{str(e)}")
        raise e


def load_report_prompts():
    try:
        report_prompts_path =get_abs_path(prompts_conf["report_prompt_path"])
    except KeyError as e:
        logger.error(f"[report_system_prompts]在yaml配置项中没有report_prompt_path配置项")
        raise e

    try:
        return open(report_prompts_path,"r",encoding="utf-8").read()
    except Exception as e:
        logger.error(f"[load_report_prompts]解析报告生成提示词出错,{str(e)}")
        raise e

"""if __name__ == '__main__':
    print(load_system_prompts())
    print(load_rag_prompts())
    print(load_report_prompts())
"""

