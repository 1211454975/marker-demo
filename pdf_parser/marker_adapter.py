from marker.converters.pdf import PdfConverter
from marker.models import create_model_dict
from marker.output import text_from_rendered
import logging
import yaml
from pathlib import Path

class MarkerParser:
    def __init__(self):
        print("MarkerParser begin init...........")
        # 加载配置文件
        with open("config.yaml", "r", encoding="utf-8") as f:
            config = yaml.load(f.read(), Loader=yaml.FullLoader)["marker"]
        
        print("MarkerParser initing after load config...........", config if config else "config is null")
        
        # 初始化模型配置
        # 修正后的模型初始化
        self.artifact_dict = create_model_dict(
            
        )
        print("MarkerParser init model ...........")
        # 加载配置文件
        self.converter = PdfConverter(artifact_dict=self.artifact_dict)
        self.logger = logging.getLogger(__name__)

        print("MarkerParser inited...........")

    def parse_pdf(self, pdf_path):
        # 在解析前添加编码预处理
        with open(pdf_path, 'rb', encoding='utf-8-sig') as f:
            raw_data = f.read().replace(b'\x80', b'')
        cleaned_data = raw_data.decode('utf-8', errors='ignore')
        return cleaned_data.encode('utf-8').decode('utf-8-sig')
        try:
            # 核心转换逻辑
            rendered = self.converter(
                pdf_path,
                max_pages=self.config.get("max_pages", None),
                langs=["chi_sim", "eng"],  # 中英文混合支持
                table_format="markdown"
            )
            text, _, _ = text_from_rendered(rendered)
            
            return self._post_process(text)
            
        except Exception as e:
            self.logger.error(f"PDF解析失败: {str(e)}")
            raise RuntimeError("论文解析服务不可用") from e

    def _post_process(self, text: str) -> str:
        """后处理增强逻辑"""
        # 重组段落结构
        processed = text.replace("\n\n", "\n").strip()
        # 过滤残留页眉页脚（示例实现）
        return "\n".join([
            line for line in processed.splitlines()
            if not any(keyword in line for keyword in ["页眉", "页脚", "Page"])
        ])