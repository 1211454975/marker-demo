from pdf_parser.content_extractor import AcademicPDFExtractor  # 修正导入路径
from ppt_generator.outline_builder import OutlineGenerator
from speech_generator.script_builder import SpeechGenerator
from video_synthesizer.tts_service import TTSService
# from video_synthesizer.video_editor import VideoGenerator  # 移除旧导入
from video_synthesizer.render import VideoRenderer
from pathlib import Path
import logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s [%(levelname)s] %(message)s',
    handlers=[
        logging.FileHandler("app.log", encoding='utf-8'),
        logging.StreamHandler()
    ]
)


class PipelineController:
    def __init__(self):
        print("controller init.........")
        self.pdf_extractor = AcademicPDFExtractor()
        print("controller init 1.........")
        self.outline_builder = OutlineGenerator()
        print("controller init 2.........")
        self.speech_gen = SpeechGenerator()
        print("controller init 3.........")
        self.tts = TTSService()
        print("controller init 4.........")
        self.video_gen = VideoRenderer(output_dir="output/videos")
        print("controller init 5.........")
        self.logger = logging.getLogger(__name__)
        
    def process(self, pdf_path: str):
        try:
            print("开始PDF解析出markdown")
            markdown = self.pdf_extractor.extract(pdf_path)
            if not markdown:
                raise ValueError("PDF解析结果为空")
            else:
                print("PDF解析出markdown")
            outline = self.outline_builder.build_outline(markdown.get("sections", ""))
            scripts = []
            for i, slide in enumerate(outline):
                try:
                    scripts.append(self.speech_gen.generate_script(slide))
                except Exception as e:
                    self.logger.error(f"幻灯片{i+1}讲稿生成失败: {str(e)}")
                    scripts.append("生成失败，请检查内容")
            
            audio_files = []
            temp_files = []
            for i, script in enumerate(scripts):
                try:
                    audio_path = self.tts.generate_audio(script, f"slide_{i}")
                    if audio_path:
                        audio_files.append(str(audio_path))
                        temp_files.append(audio_path)
                except Exception as e:
                    self.logger.error(f"语音合成失败: {str(e)}")
                    # 添加静音音频作为fallback
                    fallback_path = self._create_silent_audio()
                    audio_files.append(fallback_path)
            
            return self.video_gen.generate_video(
            slides=[s["slide_image"] for s in outline], 
            audio_files=audio_files
        )
        except Exception as e:
            self._cleanup_temp_files(temp_files)
            raise RuntimeError(f"流程执行失败: {str(e)}") from e
        finally:
            self._cleanup_temp_files(temp_files)

    def _create_silent_audio(self):
        # 增强路径处理
        silent_path = Path("temp/silent.wav").resolve().as_posix()
        silent_path = silent_path.encode('utf-8', errors='ignore').decode()
        import wave
        import os
        
        silent_path = Path("temp/silent.wav")
        silent_path.parent.mkdir(exist_ok=True)
        
        with wave.open(str(silent_path), 'wb') as f:
            f.setnchannels(1)  # 单声道
            f.setsampwidth(2)   # 16位采样
            f.setframerate(44100)
            f.writeframes(b'\x00' * 44100)  # 1秒静音
            
        return str(silent_path)

    def _cleanup_temp_files(self, files):
        """清理临时音频文件"""
        import os
        from pathlib import Path
        
        for f in files:
            try:
                if isinstance(f, Path):
                    f.unlink(missing_ok=True)
                elif isinstance(f, str):
                    Path(f).unlink(missing_ok=True)
            except Exception as e:
                self.logger.warning(f"文件清理失败: {str(f)} - {str(e)}")