#!/usr/bin/env python
# -*- coding: utf-8 -*-

from pathlib import Path
from PIL import Image
import streamlit as st
import requests
from streamlit_lottie import st_lottie
import json
import math
import time

import config


def load_lottieurl(url: str):
    r = requests.get(url)
    if r.status_code != 200:
        return None
    return r.json()


def load_lottiefile(filepath: str):
    with open(filepath, 'r', encoding='utf-8') as f:
        return json.load(f)


# ============================ 页面配置 ============================
st.set_page_config(
    page_title="Tofu Intelligence Lens Culc",
    page_icon='🔭',
    layout="wide",
    initial_sidebar_state="expanded"
)

# ============================ 炫酷CSS（仅优化侧边栏标题颜色） ============================
st.markdown("""
<style>
    /* 深空科技背景 */
    .stApp {
        background: linear-gradient(135deg, #0f0c29, #302b63, #24243e);
        background-attachment: fixed;
        color: #e0e0e0;
    }

    /* 主标题霓虹发光 */
    .neon-title {
        font-size: 3.8rem;
        font-weight: 900;
        background: linear-gradient(90deg, #00DBDE, #FC00FF, #00DBDE);
        -webkit-background-clip: text;
        background-clip: text;
        color: transparent;
        text-align: center;
        animation: neonGlow 4s ease-in-out infinite alternate;
        text-shadow: 0 0 30px rgba(0, 219, 222, 0.8);
    }

    @keyframes neonGlow {
        from { text-shadow: 0 0 20px #00DBDE, 0 0 40px #FC00FF; }
        to { text-shadow: 0 0 40px #00DBDE, 0 0 60px #FC00FF, 0 0 80px #00DBDE; }
    }

    /* 二级标题 */
    h2 {
        color: #00DBDE;
        border-bottom: 2px solid #FC00FF;
        padding-bottom: 8px;
        font-weight: 600;
    }

    /* 玻璃拟态结果卡片 */
    .glass-section {
        background: rgba(255, 255, 255, 0.05);
        backdrop-filter: blur(12px);
        -webkit-backdrop-filter: blur(12px);
        border-radius: 16px;
        border: 1px solid rgba(255, 255, 255, 0.15);
        padding: 30px;
        margin: 25px 0;
        box-shadow: 0 8px 32px rgba(0, 0, 0, 0.4);
        text-align: center;
    }
    .glass-section:hover {
        border-color: #FC00FF;
        box-shadow: 0 12px 40px rgba(252, 0, 255, 0.4);
    }

    /* 超大高对比结果数字 */
    .big-number {
        font-size: 5.5rem !important;
        font-weight: 900 !important;
        color: #FFFFFF !important;
        text-shadow: 
            0 0 20px #FC00FF,
            0 0 40px #FC00FF,
            0 0 60px #00DBDE;
        line-height: 1.2;
        margin: 20px 0;
    }

    .big-number-unit {
        font-size: 2.5rem !important;
        color: #00DBDE !important;
        font-weight: bold;
    }

    .big-label {
        font-size: 1.8rem;
        color: #a0f0ff;
        margin-bottom: 15px;
        font-weight: 600;
    }

    .medium-number {
        font-size: 3.2rem !important;
        font-weight: bold !important;
        color: #00FFFF !important;
        text-shadow: 0 0 15px #00FFFF;
    }

    .param4-number {
        font-size: 4rem !important;
        font-weight: 900 !important;
        color: #FF00FF !important;
        text-shadow: 0 0 30px #FF00FF;
    }

    /* 流光分隔线 */
    .cyber-divider {
        height: 3px;
        background: linear-gradient(90deg, transparent, #00DBDE, #FC00FF, #00DBDE, transparent);
        border-radius: 2px;
        margin: 40px 0;
        animation: flow 3s linear infinite;
    }
    @keyframes flow {
        0% { background-position: 0% 50%; }
        100% { background-position: 200% 50%; }
    }

    /* 按钮霓虹效果 */
    .stButton > button {
        background: linear-gradient(45deg, #00DBDE, #FC00FF);
        color: white;
        border: none;
        border-radius: 10px;
        font-weight: bold;
        transition: all 0.3s ease;
        box-shadow: 0 4px 15px rgba(252, 0, 255, 0.4);
    }
    .stButton > button:hover {
        transform: translateY(-3px);
        box-shadow: 0 8px 25px rgba(252, 0, 255, 0.6);
    }

    /* 输入框聚焦高对比光环 */
    .stTextInput input:focus, .stNumberInput input:focus, .stSelectbox select:focus {
        border-color: #FC00FF !important;
        box-shadow: 0 0 15px rgba(252, 0, 255, 0.8) !important;
    }

    /* ========== 关键修改：侧边栏标题颜色改为高对比亮白 ========= */
    /* 原Streamlit侧边栏标题默认颜色较暗，这里强制改为明亮易读的白色 */
    .css-1d391kg h1, 
    .css-1d391kg h2, 
    .css-1d391kg h3,
    .sidebar .sidebar-content h1,
    .sidebar .sidebar-content h2,
    .sidebar .sidebar-content h3 {
        color: #FFFFFF !important;
        text-shadow: 0 0 10px rgba(0, 10, 10, 0.1);
        font-weight: 700 !important;
    }
</style>
""", unsafe_allow_html=True)

# ============================ 加载动画 ============================
ai_gif = load_lottiefile('lens.json')
if not ai_gif:
    ai_gif = load_lottieurl("https://assets9.lottiefiles.com/packages/lf20_2gjwqmbb.json")

# ============================ 侧边栏 ============================
st.sidebar.header("🔭 功能选择 Function Selection")   # 这行文字现在会非常清晰
menu_selection = st.sidebar.radio(
    "请选择功能",
    ["镜头焦距计算", "视场角与自定义参数4配置", "LPP配置参考"]
)

# ============================ 主标题 ============================
col_lottie, col_title = st.columns([1, 3])
with col_lottie:
    st_lottie(ai_gif, speed=1.5, height=400, key="Tofu")
with col_title:
    st.markdown('<h1 class="neon-title">Tofu LensCulc</h1>', unsafe_allow_html=True)
    st.markdown("<p style='text-align:center; font-size:1.4rem; color:#a0a0ff;'>专业光电载荷智能计算平台</p>", unsafe_allow_html=True)

st.markdown("## Product Wiki Site: [Tofu Wiki](https://tofuai.helplook.net)")
st.markdown('<div class="cyber-divider"></div>', unsafe_allow_html=True)

# ============================ 以下所有功能代码保持完全不变 ============================
# （为了篇幅这里省略，直接复制你上一个版本的功能部分即可）

if menu_selection == "镜头焦距计算":
    st.markdown('<h2>🔍 镜头焦距智能推荐</h2>', unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    with col1:
        st.subheader("📷 相机选择 Select Sensor")
        cam_selection = st.selectbox("传感器类型", config.SENSOR_LIST)
        pix_type = config.SENSOR_LIST.index(cam_selection)
        
        st.subheader("🎯 识别目标 Detection Object")
        obj_selection = st.selectbox("目标类型", config.OBJ_LIST)
        obj = config.OBJ_LIST.index(obj_selection)
    
    with col2:
        st.subheader("📏 识别距离 Detection Distance")
        DDistance = float(st.slider("距离 (米)", 300, 10000, 500))

    st.subheader("🚀 计算")
    calculate = st.button('计算焦距')

    if calculate:
        with st.spinner("AI 智能计算中..."):
            time.sleep(0.8)
            
            pix_size = [2.9, 17, 12, 15][pix_type]
            Obj_size = [1.7, 5.0, 12.0, 0.4][obj]
            coeff = [60, 60, 60, 15] if pix_size < 10 else [11, 22, 40, 2.35]
            coeff = coeff[obj]
            Focal_Len = coeff * pix_size * DDistance / (Obj_size * 1000)

        st.markdown('<div class="glass-section">', unsafe_allow_html=True)
        st.markdown('<div class="big-label">推荐镜头焦距</div>', unsafe_allow_html=True)
        st.markdown(f'<div class="big-number">{int(Focal_Len)}</div>', unsafe_allow_html=True)
        st.markdown('<div class="big-number-unit">mm</div>', unsafe_allow_html=True)
        st.markdown("</div>", unsafe_allow_html=True)
    else:
        st.info('请选择参数后点击计算按钮')

elif menu_selection == "视场角与自定义参数4配置":
    st.markdown('<h2>📐 视场角与自定义参数4配置</h2>', unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    with col1:
        st.subheader("🌈 可见光参数")
        visible_pixel_size = st.number_input("可见光像元尺寸 (μm)", min_value=1.0, value=2.9, step=0.1)
        visible_resolution = st.selectbox("可见光水平分辨率", [1920, 2560, 2688])
        visible_focal = st.number_input("可见光镜头焦距 (mm)", min_value=1.0, value=25.0, step=1.0)
        
        st.subheader("⚙️ 计算")
        calculate_lpp = st.button('计算视场角与参数4')
    
    with col2:
        st.subheader("🔥 红外参数")
        ir_pixel_size = st.selectbox("红外像元尺寸 (μm)", [12, 17])
        ir_resolution = st.selectbox("红外水平分辨率", [384, 640, 1280], index=1)
        ir_focal = st.number_input("红外镜头焦距 (mm)", min_value=1.0, value=25.0, step=1.0)
    
    if calculate_lpp:
        with st.spinner("正在计算，请稍候..."):
            time.sleep(0.8)
            visible_h_fov = 2 * math.atan((visible_resolution * visible_pixel_size / 1000) / (2 * visible_focal)) * (180 / math.pi)
            ir_h_fov = 2 * math.atan((ir_resolution * ir_pixel_size / 1000) / (2 * ir_focal)) * (180 / math.pi)

            part1 = math.ceil((visible_h_fov * 10) / ir_h_fov)
            part2 = 0 if abs(visible_h_fov - 60) < 1e-9 else math.ceil((100 * visible_h_fov) / 60) * 256
            param4_MD = part1 + part2

        st.markdown('<div class="glass-section">', unsafe_allow_html=True)
        col_res1, col_res2 = st.columns(2)
        with col_res1:
            st.markdown('<div class="big-label">可见光水平视场角</div>', unsafe_allow_html=True)
            st.markdown(f'<div class="medium-number">{visible_h_fov:.2f}°</div>', unsafe_allow_html=True)
        with col_res2:
            st.markdown('<div class="big-label">红外水平视场角</div>', unsafe_allow_html=True)
            st.markdown(f'<div class="medium-number">{ir_h_fov:.2f}°</div>', unsafe_allow_html=True)

        st.markdown("<div style='margin-top:40px;'></div>", unsafe_allow_html=True)
        st.markdown('<div class="big-label">自定义参数4 配置建议</div>', unsafe_allow_html=True)
        
        col_p1, col_p2 = st.columns(2)
        with col_p1:
            st.markdown('<div style="padding:20px; background:rgba(252,0,255,0.1); border-radius:12px; border:1px solid #FC00FF;">', unsafe_allow_html=True)
            st.markdown('<div style="font-size:1.6rem; color:#a0f0ff;">LPP协议</div>', unsafe_allow_html=True)
            st.markdown(f'<div class="param4-number">{math.ceil((visible_h_fov * 10) / ir_h_fov)}</div>', unsafe_allow_html=True)
            st.markdown('</div>', unsafe_allow_html=True)
        
        with col_p2:
            st.markdown('<div style="padding:20px; background:rgba(0,219,222,0.1); border-radius:12px; border:1px solid #00DBDE;">', unsafe_allow_html=True)
            st.markdown('<div style="font-size:1.6rem; color:#a0f0ff;">脱靶量协议</div>', unsafe_allow_html=True)
            st.markdown(f'<div class="param4-number">{param4_MD}</div>', unsafe_allow_html=True)
            st.markdown('</div>', unsafe_allow_html=True)
        
        st.markdown("</div>", unsafe_allow_html=True)

elif menu_selection == "LPP配置参考":
    st.markdown('<h2>⚙️ LPP配置参考计算</h2>', unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    with col1:
        max_fov = st.number_input("相机最大视场角（°）", min_value=0.1, value=60.0, step=0.1)
    with col2:
        ptz_speed = st.number_input("云台速度细分（°）", min_value=0.001, value=0.01, step=0.001, format="%.3f")
    
    calculate_lpp_ref = st.button("计算LPP配置参数")
    
    if calculate_lpp_ref:
        with st.spinner("正在计算，请稍候..."):
            time.sleep(0.8)
            custom_param7 = math.ceil(3.5 * max_fov / (ptz_speed * 60))
            custom_param6 = math.ceil(custom_param7 * 0.02)
            motion_coeff = math.ceil(custom_param7 * 1.5)
            integral_coeff = math.ceil(motion_coeff * 0.03)
        
        st.markdown('<div class="glass-section">', unsafe_allow_html=True)
        st.markdown('<div class="big-label">LPP 参数配置推荐</div>', unsafe_allow_html=True)
        
        cols = st.columns(3)
        with cols[0]:
            st.markdown('<div style="font-size:1.4rem; color:#a0f0ff;">自定义参数5</div>', unsafe_allow_html=True)
            st.markdown('<div class="medium-number">1</div>', unsafe_allow_html=True)
            st.markdown('<div style="font-size:1.4rem; color:#a0f0ff; margin-top:30px;">自定义参数6</div>', unsafe_allow_html=True)
            st.markdown(f'<div class="medium-number">{custom_param6}</div>', unsafe_allow_html=True)
        
        with cols[1]:
            st.markdown('<div style="font-size:1.4rem; color:#a0f0ff;">自定义参数7</div>', unsafe_allow_html=True)
            st.markdown(f'<div class="medium-number">{custom_param7}</div>', unsafe_allow_html=True)
            st.markdown('<div style="font-size:1.4rem; color:#a0f0ff; margin-top:30px;">运动系数</div>', unsafe_allow_html=True)
            st.markdown(f'<div class="medium-number">{motion_coeff}</div>', unsafe_allow_html=True)
        
        with cols[2]:
            st.markdown('<div style="font-size:1.4rem; color:#a0f0ff;">差分系数</div>', unsafe_allow_html=True)
            st.markdown('<div class="medium-number">55</div>', unsafe_allow_html=True)
            st.markdown('<div style="font-size:1.4rem; color:#a0f0ff; margin-top:30px;">积分系数</div>', unsafe_allow_html=True)
            st.markdown(f'<div class="medium-number">{integral_coeff}</div>', unsafe_allow_html=True)
        
        st.markdown("</div>", unsafe_allow_html=True)

# ============================ 页脚 ============================
st.markdown('<div class="cyber-divider"></div>', unsafe_allow_html=True)
st.markdown("<p style='text-align:center; color:#888; font-size:0.9rem;'>© 2025 Tofu Intelligence </p>", unsafe_allow_html=True)
