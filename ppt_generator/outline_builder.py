from typing import List, Dict
import re
from .llm_enhancer import LLMEnhancer  # 新增导入

class OutlineGenerator:
    def __init__(self, max_slides=20):
        self.max_slides = max_slides
        self.heading_re = re.compile(r'^(#{1,3})\s+(.+)$')  # 识别1-3级标题
        self.llm_enhancer = LLMEnhancer()  # 新增初始化

    def build_outline(self, markdown_content: str) -> List[Dict]:
        # 新增LLM处理步骤
        enhanced_md = self.llm_enhancer.enhance_outline(markdown_content)
        sections = self._parse_markdown(enhanced_md)  # 处理增强后的内容
        return [self._format_section(s) for s in sections[:self.max_slides]]

    def _parse_markdown(self, content: str):
        # 按标题分割文档
        sections = []
        current_section = {}
        
        for line in content.split('\n'):
            match = self.heading_re.match(line)
            if match:
                if current_section:
                    sections.append(current_section)
                current_section = {
                    "heading": match.group(2).strip(),
                    "level": len(match.group(1)),
                    "body": []
                }
            elif current_section:
                # 保留原始Markdown格式
                cleaned_line = line.strip()
                if cleaned_line:
                    current_section["body"].append(cleaned_line)
        
        if current_section:
            sections.append(current_section)
            
        return sections

    def _format_section(self, section):
        # 根据标题级别选择布局
        layout = "title-content" if section["level"] == 1 else "split"
        return {
            "title": section["heading"],
            "layout": layout,
            "content": "\n".join(section["body"]),
            "notes": ""  
        }