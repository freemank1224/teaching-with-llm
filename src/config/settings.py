import platform
import os
import json
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
        self._load_config_from_json()
    
    def _load_config_from_json(self):
        """从JSON文件加载配置"""
        config_path = Path(__file__).parent / "llm_paras.json"
        if config_path.exists():
            try:
                with open(config_path, 'r', encoding='utf-8') as f:
                    config_dict = json.load(f)
                # 使用加载的配置更新当前配置
                if isinstance(config_dict, dict):
                    # 直接更新属性，而不是重新赋值self
                    if 'openai' in config_dict:
                        self.openai = OpenAIConfig(**config_dict['openai'])
                    if 'ollama' in config_dict:
                        self.ollama = OllamaConfig(**config_dict['ollama'])
                    print("Parameters file found and loaded successfully!")
            except Exception as e:
                print(f"加载配置文件失败: {str(e)}")
    
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
        "正确性": 0.4,
        "创新性": 0.2
    }

settings = Settings()