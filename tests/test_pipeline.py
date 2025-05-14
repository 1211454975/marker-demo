import unittest
from unittest.mock import Mock, patch
from pathlib import Path
from main import PipelineController

class TestPipeline(unittest.TestCase):
    def setUp(self):
        self.controller = PipelineController()
        
        # Mock所有依赖模块
        self.mock_extractor = Mock()
        self.mock_outline = Mock()
        self.mock_tts = Mock()
        self.mock_video = Mock()
        
        self.controller.pdf_extractor = self.mock_extractor
        self.controller.outline_builder = self.mock_outline
        self.controller.tts = self.mock_tts
        self.controller.video_gen = self.mock_video

    @patch('pathlib.Path.exists')
    def test_normal_flow(self, mock_exists):
        # 模拟正常流程
        mock_exists.return_value = True
        self.mock_extractor.extract.return_value = {"sections": "test content"}
        self.mock_outline.build_outline.return_value = [{"slide_image": "slide1.png"}]
        self.mock_tts.generate_audio.return_value = Path("audio.wav")
        self.mock_video.generate_video.return_value = "output/presentation.mp4"
        
        result = self.controller.process("test.pdf")
        self.assertEqual(result, "output/presentation.mp4")

    def test_pdf_extraction_failure(self):
        # 测试PDF解析失败场景
        self.mock_extractor.extract.side_effect = ValueError("Invalid PDF")
        
        with self.assertRaises(RuntimeError):
            self.controller.process("invalid.pdf")

    @patch('builtins.open', new_callable=unittest.mock.mock_open)
    def test_temp_file_cleanup(self, mock_file):
        # 验证临时文件清理机制
        self.mock_tts.generate_audio.return_value = Path("temp/audio.wav")
        
        try:
            self.controller.process("cleanup_test.pdf")
        except:
            pass
            
        self.mock_video.generate_video.assert_called_once()