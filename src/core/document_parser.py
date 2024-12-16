from pathlib import Path
from typing import Dict, List, Union
import markdown
from ..config.settings import settings

class DocumentParser:
    def __init__(self):
        self.supported_formats = settings.SUPPORTED_FORMATS

    def parse(self, file_path: Union[str, Path]) -> Dict:
        """解析输入文档"""
        file_path = Path(file_path)
        if not file_path.exists():
            raise FileNotFoundError(f"文件不存在: {file_path}")
            
        if file_path.suffix not in self.supported_formats:
            raise ValueError(f"不支持的文件格式: {file_path.suffix}")
            
        if file_path.suffix in ['.md', '.txt']:
            return self._parse_markdown(file_path)
        elif file_path.suffix == '.pdf' and settings.PDF_ENABLED:
            return self._parse_pdf(file_path)
            
    def _parse_markdown(self, file_path: Path) -> Dict:
        """解析Markdown文件"""
        content = file_path.read_text(encoding='utf-8')
        # TODO: 实现Markdown解析逻辑
        return {
            'type': 'markdown',
            'content': content,
            'blocks': self._split_content(content)
        }
        
    def _split_content(self, content: str) -> List[Dict]:
        """将内容分割为不同类型的块"""
        # TODO: 实现内容分块逻辑
        return [] 