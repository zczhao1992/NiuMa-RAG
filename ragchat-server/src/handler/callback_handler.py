from langchain_core.callbacks import BaseCallbackHandler
from langchain_core.outputs import LLMResult
# from langchain.schema import AgentAction, AgentFinish, LLMResult
import time
from typing import Any, Dict, List, Union


class CustomCallbackHandler(BaseCallbackHandler):

    def __init__(self):
        self.start_time = None
        self.total_tokens = 0
        self.llm_calls = 0
        self.agent_actions = []

    def on_llm_start(self, serialized: Dict[str, Any], prompts: List[str], **kwargs: Any) -> None:
        self.start_time = time.time()
        self.llm_calls += 1
        print("prompts", prompts)

    def on_llm_end(self, response: LLMResult, **kwargs: Any) -> None:
        if self.start_time:
            duration = time.time() - self.start_time
            response.llm_output["custom_metadata"] = "1212"

            if response.llm_output and "token_usage" in response.llm_output:
                usage = response.llm_output["token_usage"]
                total_tokens = usage.get("total_tokens", 0)
                self.total_tokens += total_tokens
            print("总token：", self.total_tokens)
