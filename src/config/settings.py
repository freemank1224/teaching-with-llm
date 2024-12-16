import platform
import os
from pathlib import Path
from typing import Dict, Optional
from dataclasses import dataclass

@dataclass
class OpenAIConfig:
    api_key: Optional[str] = None
    base_url: str = "https://api.openai.com/v1"
    chat_model: str = "gpt-4"
    vision_model: str = "gpt-4-vision-preview"
    max_tokens: int = 500
    temperature: float = 0.7
    timeout: int = 30

@dataclass
class OllamaConfig:
    host: str = "http://localhost:11434"
    chat_model: str = "llama2"
    vision_model: str = "llava"
    max_tokens: int = 500
    temperature: float = 0.7
    timeout: int = 30

class LLMConfig:
    """LLM配置管理类"""
    
    def __init__(self):
        self.openai = OpenAIConfig()
        self.ollama = OllamaConfig()
    
    @classmethod
    def from_dict(cls, config_dict: Dict) -> 'LLMConfig':
        """从字典创建配置"""
        instance = cls()
        if 'openai' in config_dict:
            instance.openai = OpenAIConfig(**config_dict['openai'])
        if 'ollama' in config_dict:
            instance.ollama = OllamaConfig(**config_dict['ollama'])
        return instance

class Settings:
    # 系统相关配置
    SYSTEM = platform.system()  # 自动检测操作系统
    IS_WINDOWS = SYSTEM == "Windows"
    IS_MACOS = SYSTEM == "Darwin"

    # 项目路径配置
    BASE_DIR = Path(__file__).parent.parent.parent
    TEMP_DIR = BASE_DIR / "temp"
    
    # LLM配置
    DEFAULT_LLM = "openai"  # 可选: "openai", "ollama"
    OPENAI_API_KEY = os.getenv("OPENAI_API_KEY", "")
    OLLAMA_HOST = os.getenv("OLLAMA_HOST", "http://localhost:11434")
    
    # PDF处理配置
    PDF_ENABLED = True
    
    # 文档处理配置
    SUPPORTED_FORMATS = [".md", ".txt", ".pdf"]
    
    # 评分配置
    SCORING_METRICS = {
        "完整性": 0.4,
        "准确性": 0.4,
        "创新性": 0.2
    }

settings = Settings() 