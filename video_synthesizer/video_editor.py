from moviepy.editor import ImageClip, AudioFileClip, concatenate_videoclips, CompositeVideoClip
from moviepy.video.VideoClip import TextClip
from typing import List
import logging

class VideoGenerator:
    def __init__(self, resolution=(1920, 1080), fps=24):
        self.resolution = resolution
        self.fps = fps
        self.logger = logging.getLogger(__name__)
        
    def generate_video(self, slides: List[str], audio_files: List[str]) -> str:
        """增强版视频合成"""
        video_clips = []
        
        for idx, (slide_path, audio_path) in enumerate(zip(slides, audio_files)):
            try:
                audio_clip = self._load_audio(audio_path)
                slide_duration = audio_clip.duration
                slide_clip = self._create_slide_clip(slide_path, slide_duration)
                video_clips.append(slide_clip.set_audio(audio_clip))
            except Exception as e:
                self.logger.error(f"幻灯片{idx+1}处理失败: {str(e)}")
                
        final_clip = concatenate_videoclips(video_clips)
        output_path = "output/presentation.mp4"
        final_clip.write_videofile(output_path, fps=self.fps)
        return output_path

class VideoGeneratorBase:
    """视频生成基类（保留核心功能）"""
    def _create_slide_clip(self, image_path: str, duration: float):
        clip = ImageClip(image_path, duration=duration)
        txt_clip = TextClip("AI Generated Presentation", fontsize=24, color='white')
        txt_clip = txt_clip.set_position(('center', 20)).set_duration(duration)
        return CompositeVideoClip([clip, txt_clip])

    def _load_audio(self, audio_path: str):
        if not audio_path.endswith(".wav"):
            raise ValueError("仅支持WAV格式音频")
        return AudioFileClip(audio_path)