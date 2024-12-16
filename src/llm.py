from typing import Optional, Dict, List, Union
import os
import requests
from abc import ABC, abstractmethod
import openai
from openai import OpenAI

class LLMBase(ABC):
    """LLM基类，定义统一接口"""
    
    @abstractmethod
    def chat(self, messages: List[Dict[str, str]]) -> str:
        """聊天接口"""
        pass
    
    @abstractmethod
    def analyze_image(self, image_path: str, prompt: str) -> str:
        """图片分析接口"""
        pass
    
    @abstractmethod
    def evaluate_answer(self, standard_answer: str, student_answer: str) -> Dict[str, Union[float, str]]:
        """评估答案"""
        pass
    
    @abstractmethod
    def analyze_code(self, code: str) -> Dict[str, str]:
        """分析代码"""
        pass

class OpenAIHandler(LLMBase):
    """OpenAI API处理器"""
    
    def __init__(self, api_key: Optional[str] = None):
        self.api_key = api_key or os.getenv("OPENAI_API_KEY")
        if not self.api_key:
            raise ValueError("OpenAI API密钥未设置")
        self.client = OpenAI(api_key=self.api_key)
        
    def chat(self, messages: List[Dict[str, str]]) -> str:
        """使用OpenAI chat completion API"""
        try:
            response = self.client.chat.completions.create(
                model="gpt-4",  # 可配置
                messages=messages
            )
            return response.choices[0].message.content
        except Exception as e:
            raise Exception(f"OpenAI API调用失败: {str(e)}")
            
    def analyze_image(self, image_path: str, prompt: str) -> str:
        """使用OpenAI Vision API分析图片"""
        try:
            with open(image_path, "rb") as image_file:
                response = self.client.chat.completions.create(
                    model="gpt-4-vision-preview",
                    messages=[
                        {
                            "role": "user",
                            "content": [
                                {"type": "text", "text": prompt},
                                {
                                    "type": "image_url",
                                    "image_url": {
                                        "url": f"data:image/jpeg;base64,{image_file.read()}"
                                    }
                                }
                            ]
                        }
                    ],
                    max_tokens=500
                )
            return response.choices[0].message.content
        except Exception as e:
            raise Exception(f"OpenAI Vision API调用失败: {str(e)}")
            
    def evaluate_answer(self, standard_answer: str, student_answer: str) -> Dict[str, Union[float, str]]:
        """评估答案并返回分数和评语"""
        prompt = f"""
        请评估以下学生答案的质量。
        
        标准答案：
        {standard_answer}
        
        学生答案：
        {student_answer}
        
        请提供：
        1. 分数（0-100）
        2. 详细评语
        3. 改进建议
        """
        
        response = self.chat([{"role": "user", "content": prompt}])
        # 这里需要解析response来提取分数和评语
        # 实际实现时可能需要更结构化的prompt和响应格式
        return {
            "score": 0,  # 解析后的分数
            "comments": response,
            "suggestions": ""
        }

    def analyze_code(self, code: str) -> Dict[str, str]:
        """分析代码质量"""
        prompt = f"""
        请分析以下代码：
        
        {code}
        
        请提供：
        1. 代码质量评估
        2. 潜在问题
        3. 改进建议
        """
        
        response = self.chat([{"role": "user", "content": prompt}])
        return {
            "quality": "",  # 解析响应得到的质量评估
            "issues": "",   # 发现的问题
            "suggestions": response  # 改进建议
        }

class OllamaHandler(LLMBase):
    """Ollama API处理器"""
    
    def __init__(self, host: str = "http://localhost:11434"):
        self.host = host
        self.model = "llama2"  # 默认模型
        
    def chat(self, messages: List[Dict[str, str]]) -> str:
        """使用Ollama chat API"""
        try:
            response = requests.post(
                f"{self.host}/api/chat",
                json={
                    "model": self.model,
                    "messages": messages
                }
            )
            response.raise_for_status()
            return response.json()["message"]["content"]
        except Exception as e:
            raise Exception(f"Ollama API调用失败: {str(e)}")
            
    def analyze_image(self, image_path: str, prompt: str) -> str:
        """使用支持多模态的Ollama模型"""
        try:
            with open(image_path, "rb") as image_file:
                response = requests.post(
                    f"{self.host}/api/generate",
                    json={
                        "model": "llava",  # 使用支持图像的模型
                        "prompt": prompt,
                        "images": [image_file.read()]
                    }
                )
            response.raise_for_status()
            return response.json()["response"]
        except Exception as e:
            raise Exception(f"Ollama图像分析失败: {str(e)}")
            
    def evaluate_answer(self, standard_answer: str, student_answer: str) -> Dict[str, Union[float, str]]:
        """评估答案并返回分数和评语"""
        prompt = f"""
        请评估以下学生答案的质量。
        
        标准答案：
        {standard_answer}
        
        学生答案：
        {student_answer}
        
        请提供：
        1. 分数（0-100）
        2. 详细评语
        3. 改进建议
        """
        
        response = self.chat([{"role": "user", "content": prompt}])
        # 这里需要解析response来提取分数和评语
        # 实际实现时可能需要更结构化的prompt和响应格式
        return {
            "score": 0,  # 解析后的分数
            "comments": response,
            "suggestions": ""
        }

    def analyze_code(self, code: str) -> Dict[str, str]:
        """分析代码质量"""
        prompt = f"""
        请分析以下代码：
        
        {code}
        
        请提供：
        1. 代码质量评估
        2. 潜在问题
        3. 改进建议
        """
        
        response = self.chat([{"role": "user", "content": prompt}])
        return {
            "quality": "",  # 解析响应得到的质量评估
            "issues": "",   # 发现的问题
            "suggestions": response  # 改进建议
        }

class LLMFactory:
    """LLM工厂类，用于创建LLM实例"""
    
    @staticmethod
    def create(provider: str = "openai", **kwargs) -> LLMBase:
        """
        创建LLM实例
        :param provider: 'openai' 或 'ollama'
        :param kwargs: 额外参数
        :return: LLM实例
        """
        if provider == "openai":
            return OpenAIHandler(**kwargs)
        elif provider == "ollama":
            return OllamaHandler(**kwargs)
        else:
            raise ValueError(f"不支持的LLM提供商: {provider}")

# 使用示例
if __name__ == "__main__":
    # 创建LLM实例
    llm = LLMFactory.create("openai")  # 或 LLMFactory.create("ollama")
    
    # 测试对话
    messages = [
        {"role": "user", "content": "请分析这段代码的质量。"}
    ]
    
    try:
        response = llm.chat(messages)
        print("回复:", response)
    except Exception as e:
        print(f"错误: {e}") 