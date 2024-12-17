from typing import Dict, Union
from config import config
from llm import LLMFactory

class Evaluator:
    """评分系统"""
    
    def __init__(self):
        self.llm = LLMFactory.create(config.llm_config)
        self.metrics = config.SCORING_METRICS
        
    def evaluate(self, standard_answer: str, student_answer: str) -> Dict[str, Union[float, str]]:
        """评估答案"""
        return self.llm.evaluate_answer(standard_answer, student_answer) 