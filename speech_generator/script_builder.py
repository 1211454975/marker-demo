
from config import settings
import markdown
from typing import Optional
import logging
from openai import OpenAI

class SpeechGenerator:
    def __init__(self):
        self.client = OpenAI(
            api_key=settings.deepseek.api_key,
            base_url="https://api.deepseek.com/v1",
            timeout=settings.deepseek.timeout
        )
        # 假设 max_retries 应该从 settings 中获取，这里从 settings 里取默认重试次数
        self.retries = settings.deepseek.max_retries if hasattr(settings.deepseek, 'max_retries') else 3
        self.logger = logging.getLogger(__name__)
        
    def generate_script(self, slide_data: dict) -> Optional[str]:
        """生成带背景知识的演讲稿"""
        try:
            prompt = self._build_prompt(slide_data)
            response = self._safe_api_call(prompt)
            return self._post_process(response, slide_data)
        except Exception as e:
            self.logger.error(f"演讲稿生成失败: {str(e)}")
            return None

    def _build_prompt(self, data: dict) -> str:
        """构造符合DeepSeek要求的prompt"""
        return f"""基于以下学术内容生成适合课堂教学的演讲稿：
# 标题: {data.get('title','')}
# 原始内容: 
{data.get('content','')}

要求：
1. 补充3个相关专业术语的解释（使用比喻说明）
2. 添加实际应用案例（至少1个）
3. 包含1个互动提问环节设计
4. 输出格式使用标准Markdown"""

    def _post_process(self, raw_text: str, data: dict) -> str:
        """后处理增强"""
        # 保留原始标题结构
        return f"# {data['title']}\n\n{markdown.markdown(raw_text)}"

    def _safe_api_call(self, prompt):
        """适配OpenAI格式的调用"""
        return self.client.chat.completions.create(
            model="deepseek-1.0",
            messages=[{"role": "user", "content": prompt}],
            max_tokens=2000
        )