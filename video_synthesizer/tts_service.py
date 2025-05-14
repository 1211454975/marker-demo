import pyttsx3
import logging
from pathlib import Path
from typing import Optional
from config import settings

class TTSService:
    def __init__(self):
        self.engine = pyttsx3.init()
        self.output_dir = Path(settings.tts.output_dir)
        self.logger = logging.getLogger(__name__)
        
        # 从配置文件加载参数
        self.engine.setProperty('rate', settings.tts.get('rate', 150))
        self.engine.setProperty('volume', settings.tts.get('volume', 0.8))
        
        # 设置语音类型
        if 'voice' in settings.tts:
            try:
                self.engine.setProperty('voice', settings.tts.voice)
            except Exception as e:
                self.logger.warning(f"语音设置失败: {str(e)}，使用默认语音")

    def generate_audio(self, text: str, filename: str) -> Optional[Path]:
        """生成语音文件并返回路径"""
        try:
            output_path = self.output_dir / f"{filename}.wav"
            self.engine.save_to_file(text, str(output_path))
            self.engine.runAndWait()
            return output_path if output_path.exists() else None
        except Exception as e:
            self.logger.error(f"语音生成失败: {str(e)}")
            return None