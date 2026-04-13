from typing import Callable

from langchain.agents import AgentState
from langchain.agents.middleware import wrap_tool_call, before_model, dynamic_prompt, ModelRequest
from langgraph.prebuilt.tool_node import ToolCallRequest
from langgraph.runtime import Runtime
from langgraph.types import Command
from langchain_core.messages import ToolMessage

from Agent.tools.agent_tools import fill_context_for_report
from Agent.utils.logger_handler import logger
from Agent.utils.prompt_loader import load_report_prompts, load_system_prompts


#所有的工具调用都会经过这里，自动开启报告模式
@wrap_tool_call
def monitor_tool(
        #请求的数据封装
        request: ToolCallRequest,
        #执行的函数本身
        handler: Callable[[ToolCallRequest], ToolMessage | Command],
)->ToolMessage | Command:  #工具执行的监控

    logger.info(f"[tool monitor]执行工具：{request.tool_call['name']}")
    logger.info(f"[tool monitor]传入参数：{request.tool_call['args']}")

    try:
        #执行工具
        result= handler(request)
        logger.info(f"[tool monitor]工具{request.tool_call['name']}调用成功")

        #如果等于这个函数
        if request.tool_call['name']==fill_context_for_report:
            #是就标记report为True
            request.runtime.context["report"]=True

        return result
    except Exception as e:
        logger.error(f"工具{request.tool_call['name']}调用失败，原因：{str(e)}")
        raise e


#模型调用前日志，方便调试，知道Agent什么时候思考
@before_model
def log_before_model(
        state:AgentState,  #整个Agent智能体中的状态记录
        runtime:Runtime,   #记录了整个执行过程中的上下文信息
):  #在模型执行前输出日志
    logger.info(f"[log_before_model]即将调用模型，带有{len(state['messages'])}条消息。")
    #打印最后一条消息
    logger.debug(f"[log_before_model]{type(state['messages'])[-1].__name__} | {state['messages'][-1].content.strip()}")

    return None

#动态切换提示词
#普通聊天：用普通系统提示词
#写报告：自动转换成报告专用提示词
@dynamic_prompt              #每一次在生成提示词之前调用此函数
def report_prompt_switch(request:ModelRequest):  #动态切换提示词
    #查看是否标记了报告模式
    is_report=request.runtime.context.get("report",False)
    #是报告模式：加载报告提示词
    if is_report:
        return load_report_prompts()
    #不是就加载普通提示词
    return load_system_prompts()
