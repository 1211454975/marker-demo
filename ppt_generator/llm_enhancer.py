from openai import OpenAI
from config import settings

class LLMEnhancer:
    def __init__(self):
        self.client = OpenAI(
            api_key=settings.deepseek.api_key,
            base_url="https://api.deepseek.com/v1",
            timeout=settings.deepseek.timeout
        )
    
    def enhance_outline(self, markdown: str) -> str:
        """适配后的调用方式"""
        completion = self.client.chat.completions.create(
            model="deepseek-academic-1.0",
            messages=[{
                "role": "user", 
                "content": f"将以下学术内容转换为适合PPT展示的结构（中文）：\n{markdown}"
            }]
        )
        return completion.choices[0].message.content