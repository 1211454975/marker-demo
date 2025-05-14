# Marker-Demo 学术论文转视频工具

![Python](https://img.shields.io/badge/python-3.10%2B-blue)
![License](https://img.shields.io/badge/license-MIT-green)

将学术论文PDF自动转换为演示视频的智能工具，集成大模型内容增强和语音合成功能。

## 主要功能
- 📄 PDF解析与章节提取
- 📊 智能PPT大纲生成
- 🎙️ 演讲稿自动生成（DeepSeek增强）
- 🔊 语音合成(TTS)与视频合成
- 🌐 Web界面交互

## 快速开始
```bash
# 克隆项目
git clone https://github.com/yourname/marker-demo.git
cd marker-demo

# 安装依赖
pip install torch==2.0.1 torchvision==0.15.2 torchaudio==2.0.2 --index-url https://download.pytorch.org/whl/cpu


pip install torch==2.3.0 torchvision==0.18.0 torchaudio==2.3.0 --index-url https://download.pytorch.org/whl/cpu

pip install -r requirements.txt

# 配置API密钥
cp config.yaml.example config.yaml
vim config.yaml  # 填写DeepSeek API密钥

# 启动Web服务
streamlit run web_ui.py

# 或使用Docker
docker build -t paper2video .
docker run -p 8501:8501 -e DEEPSEEK_API_KEY=your_key paper2video
```
访问 http://localhost:5000 上传PDF文件

# 项目结构

```
marker-demo/
├── pdf_parser/       # PDF解析模块
├── ppt_generator/    # PPT生成模块
├── speech_generator/ # 演讲稿生成 
├── video_synthesizer/# 音视频合成
├── web_interface/    # Web交互界面
└── config.yaml       # 配置文件
```
# ## 依赖项
- marker-python >=0.2.6
- python-pptx >=0.6.21
- moviepy >=1.0.3
- Flask >=3.0.2
- pyttsx3 >=2.90

# ## 配置说明
编辑 config.yaml :

```yaml
deepseek:
  api_key: "your-api-key"  # 必填
  timeout: 30

video:
  output_dir: "./output"
  resolution: 1920x1080
```

# ## 许可证
MIT License

```

主要包含：
1. 项目简介与功能亮点
2. 快速启动指南
3. 模块化架构说明
4. 核心配置参数说明
5. 依赖项与许可信息

建议补充运行截图和详细API文档链接。需要我添加特定章节的详细说明吗？
```