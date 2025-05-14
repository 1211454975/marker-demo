import re
from pathlib import Path
import logging
import yaml
from typing import Dict, List
from .marker_adapter import MarkerParser

class PDFTextExtractor:
    def __init__(self):
        self.parser = MarkerParser()
        self.logger = logging.getLogger(__name__)
        
        # 加载配置文件
        with open("config.yaml", 'r', encoding='utf-8') as f:
            self.config = yaml.safe_load(f).get('pdf_parser', {})

    def extract_text(self, pdf_path: str) -> Dict:
        """提取PDF文本内容并转换为结构化数据"""
        try:
            # 增强二进制数据清洗
            raw_bytes = Path(pdf_path).read_bytes()
            cleaned_bytes = raw_bytes.replace(b'\x80', b'')  # 移除0x80特殊字符
            cleaned_text = cleaned_bytes.decode('utf-8', errors='ignore')
            output_path = Path(pdf_path).with_suffix('.md')  # 移出try块
            try:
                # 解析PDF内容（修正解码逻辑）
                raw_text = self.parser.parse_pdf(pdf_path)
                # 增强多阶段清洗
                cleaned_text = raw_text.encode('utf-8', errors='ignore').decode('utf-8')
                cleaned_text = ''.join(c for c in cleaned_text if c.isprintable())
                
                # 生成结构化数据
                result = {
                    "sections": self._parse_sections(cleaned_text),
                    "metadata": self._extract_metadata(cleaned_text),
                    "file_path": str(output_path)
                }
                
                # 保存Markdown文件
                output_path.parent.mkdir(parents=True, exist_ok=True)
                with open(output_path, 'w', encoding='utf-8') as f:
                    f.write(f"# {result['metadata'].get('title', 'Untitled')}\n\n")
                    f.write(cleaned_text)  # 修正为使用清洗后的文本
                    
                self.logger.info(f"成功生成Markdown文件：{output_path}")
                return result
                
            except FileNotFoundError as e:
                self.logger.error(f"文件不存在：{pdf_path}")
                raise ValueError("指定的PDF文件不存在") from e
            except Exception as e:
                self.logger.error(f"PDF解析失败：{str(e)}", exc_info=True)
                raise RuntimeError("无法解析PDF文件内容") from e
        finally:
            pass

    

    def _parse_sections(self, text: str) -> List[Dict]:
        """解析章节结构（增强版）"""
        sections = []
        current_section = {}
        
        # 使用正则表达式匹配多级标题
        header_pattern = re.compile(r'^(#{2,})\s+(.+)$')
        
        for line in text.split('\n'):
            match = header_pattern.match(line)
            if match:
                if current_section:
                    sections.append(current_section)
                level = len(match.group(1))  # ##=2, ###=3, etc.
                current_section = {
                    "heading": match.group(2).strip(),
                    "level": level,
                    "content": []
                }
            elif current_section:
                # 过滤空行并保留有效内容
                stripped_line = line.strip()
                if stripped_line:
                    current_section["content"].append(stripped_line)
                
        if current_section:
            sections.append(current_section)
            
        return sections

    def _extract_metadata(self, text: str) -> Dict:
        """提取文档元数据（增强版）"""
        metadata = {
            "title": "Untitled",
            "authors": [],
            "keywords": [],
            "abstract": ""
        }
    
        # 提取标题（增强正则匹配）
        title_match = re.search(r'^#\s+(.+)$', text, re.MULTILINE)
        if title_match:
            metadata["title"] = title_match.group(1).strip()
    
        # 提取作者（匹配常见学术论文格式）
        authors_section = re.search(r'(?i)^\s*by\s+(.+?)(?=\n#)', text, re.DOTALL)
        if authors_section:
            authors = [a.strip() for a in authors_section.group(1).split(';') if a.strip()]
            metadata["authors"] = authors[:5]  # 最多保留5位作者
    
        # 提取关键词（中英文混合支持）
        keywords_match = re.search(r'(?i)(?:关键词|keywords)[:：]\s*(.+)', text)
        if keywords_match:
            metadata["keywords"] = [kw.strip() for kw in keywords_match.group(1).split() if kw.strip()]
    
        # 提取摘要（匹配摘要章节）
        abstract_match = re.search(r'(?i)^#+\s*摘要\s*\n(.+?)(?=#)', text, re.DOTALL)
        if abstract_match:
            metadata["abstract"] = re.sub(r'\s+', ' ', abstract_match.group(1).strip())
    
        return metadata

    def _post_process(self, text: str) -> str:
        """后处理文本内容"""
        # 添加编码规范化处理
        cleaned_text = text.encode('utf-8', 'ignore').decode('utf-8')
        # 移除多余空行
        processed = '\n'.join([line for line in cleaned_text.split('\n') if line.strip()])
        # 过滤页眉页脚
        return '\n'.join(
            line for line in processed.split('\n') 
            if not any(keyword in line for keyword in ["页眉", "页脚", "Page"])
        )