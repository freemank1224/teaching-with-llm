import platform
import os
from pathlib import Path

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