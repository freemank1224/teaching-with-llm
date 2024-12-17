from pathlib import Path
from typing import Dict, Union
from config import config
from parsers.markit_parser import MarkitParser
from parsers.miner_parser import MinerParser

class DocumentParser:
    """文档解析器工厂"""
    
    def __init__(self):
        self.supported_formats = config.parser.SUPPORTED_FORMATS
        if config.parser.PARSER_TYPE == "markit":
            self.parser = MarkitParser()
        elif config.parser.PARSER_TYPE == "miner":
            self.parser = MinerParser()
        else:
            raise ValueError(f"不支持的解析器类型: {config.parser.PARSER_TYPE}")

    def parse(self, file_path: Union[str, Path]) -> Dict:
        """解析输入文档"""
        file_path = Path(file_path)
        if not file_path.exists():
            raise FileNotFoundError(f"文件不存在: {file_path}")
            
        if file_path.suffix not in self.supported_formats:
            raise ValueError(f"不支持的文件格式: {file_path.suffix}")
            
        return self.parser.parse(file_path) 