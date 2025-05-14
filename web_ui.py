import os
import asyncio
os.environ["PYTHONUTF8"] = "1"

# Enhanced event loop configuration
if os.name == 'nt':
    asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
    asyncio.set_event_loop(asyncio.ProactorEventLoop())

import streamlit as st
from main import PipelineController
from pathlib import Path
import time
import locale
locale.setlocale(locale.LC_ALL, 'en_US.UTF-8')  # 添加在文件开头

# 界面配置
st.set_page_config(page_title="Paper2Video", page_icon=":film_projector:")

# 产品标识
col1, col2 = st.columns([0.3, 0.7])
with col1:
    st.image("assets/logo.png", width=120)
with col2:
    st.title("学术论文视频生成系统")

# 文件上传区
uploaded_file = st.file_uploader("选择PDF论文文件", type=["pdf"])
process_btn = st.button("开始转换", disabled=not uploaded_file)

if process_btn and uploaded_file:
    try:
        # 保存上传文件
        # 增强文件名编码处理（Windows兼容）
        safe_filename = uploaded_file.name.encode('utf-8', errors='replace').decode('utf-8')
        safe_filename = ''.join(c for c in safe_filename if c.isprintable()).strip()
        # 增强路径编码处理
        safe_path = Path("uploads") / Path(safe_filename).as_posix()
        safe_path.parent.mkdir(parents=True, exist_ok=True)
        with open(safe_path, "wb") as f:
            f.write(uploaded_file.getbuffer())
        # 确保临时目录存在
        temp_dir = Path("temp")
        temp_dir.mkdir(parents=True, exist_ok=True)
        
        # 新增日志文件操作
        # 修正后的日志文件操作
        log_content = f"开始处理文件: {uploaded_file.name}".encode('utf-8')
        (temp_dir / "processing_log.txt").write_bytes(log_content)
        
        # 初始化进度条
        progress_bar = st.progress(0)
        status_text = st.empty()
        st.success("初始化进度条完成！")
        # 处理流程
        controller = PipelineController()
        video_path = controller.process(str(safe_path))
        
        # 显示结果
        st.success("生成完成！")
        st.video(str(video_path))
        
    except Exception as e:
        st.error(f"生成失败: {str(e)}")
        st.stop()