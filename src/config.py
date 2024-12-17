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
        config_path = Path(__file__).parent / "llm_paras.json"
        if config_path.exists():
            try:
                with open(config_path, 'r', encoding='utf-8') as f:
                    config_dict = json.load(f)
                if isinstance(config_dict, dict):
                    if 'openai' in config_dict:
                        self.openai = OpenAIConfig(**config_dict['openai'])
                    if 'ollama' in config_dict:
                        self.ollama = OllamaConfig(**config_dict['ollama'])
            except Exception as e:
                print(f"加载配置文件失败: {str(e)}")

class Config:
    """全局配置类"""
    # 系统相关配置
    SYSTEM = platform.system()
    IS_WINDOWS = SYSTEM == "Windows"
    IS_MACOS = SYSTEM == "Darwin"

    # 项目路径配置
    BASE_DIR = Path(__file__).parent.parent
    TEMP_DIR = BASE_DIR / "temp"
    
    # 文档处理配置
    SUPPORTED_FORMATS = [".md", ".txt", ".pdf"]
    PDF_ENABLED = True
    
    # 评分配置
    SCORING_METRICS = {
        "完整性": 0.4,
        "正确性": 0.4,
        "创新性": 0.2
    }

    # LLM配置
    llm_config = LLMConfig()

config = Config() 