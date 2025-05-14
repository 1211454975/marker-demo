from .marker_adapter import MarkerParser
from typing import Dict, List

class AcademicPDFExtractor:
    def __init__(self):
        self.parser = MarkerParser()
    
    def extract(self, pdf_path: str) -> List[Dict]:
        """带异常处理的提取入口"""
        try:
            content = self.parser.parse_pdf(pdf_path)
            return {
                "sections": self._split_sections(content),
                "equations": self._extract_equations(content),
                "tables": self._extract_tables(content)
            }
        except FileNotFoundError:
            raise ValueError("PDF文件不存在")
        except RuntimeError as e:
            raise RuntimeError(f"PDF解析引擎错误: {str(e)}")