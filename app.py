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
    with open(filepath, 'r') as f:
        return json.load(f)


# 设置页面布局
st.set_page_config(
    page_title="Tofu Intelligence Lens Culc",
    page_icon='logo.png',
    layout="wide",
    initial_sidebar_state="expanded"
)

# 自定义CSS - 增加炫酷效果但保持按钮和输入框长度
st.markdown("""
<style>
    /* 保持原有输入组件和按钮长度 */
    .stSelectbox [data-baseweb="select"] {
        width: 200px;
    }
    .stNumberInput {
        width: 200px !important;
    }
    .stNumberInput input {
        width: 150px !important;
    }
    .stSlider [data-baseweb="slider"] {
        width: 200px;
    }
    .stButton button {
        width: 200px;
    }

    /* 新增炫酷效果 */
    /* 渐变色标题 */
    .gradient-title {
        background: linear-gradient(90deg, #4facfe 0%, #00f2fe 100%);
        -webkit-background-clip: text;
        background-clip: text;
        color: transparent;
        animation: fadeIn 1.5s ease-in-out;
    }
    
    /* 结果卡片动效 */
    .result-card {
        border-radius: 10px;
        box-shadow: 0 4px 20px rgba(0, 0, 0, 0.1);
        padding: 20px;
        margin: 10px 0;
        transition: transform 0.3s ease, box-shadow 0.3s ease;
    }
    .result-card:hover {
        transform: translateY(-5px);
        box-shadow: 0 8px 30px rgba(0, 0, 0, 0.15);
    }
    
    /* 页面加载动画 */
    @keyframes fadeIn {
        from { opacity: 0; transform: translateY(20px); }
        to { opacity: 1; transform: translateY(0); }
    }
    
    .animate-on-load {
        animation: fadeIn 0.8s ease-out forwards;
    }
    
    /* 按钮悬停效果 */
    .stButton button:hover {
        background-color: #4facfe;
        color: white;
        transition: all 0.3s ease;
    }
    
    /* 输入框聚焦效果 */
    .stTextInput input:focus, .stNumberInput input:focus {
        border: 2px solid #4facfe;
        box-shadow: 0 0 0 3px rgba(79, 172, 254, 0.2);
    }
    
    /* 分隔线美化 */
    .custom-divider {
        height: 3px;
        background: linear-gradient(90deg, transparent, #4facfe, transparent);
        margin: 20px 0;
    }
</style>
""", unsafe_allow_html=True)

# 页面加载动画
with st.spinner("正在加载应用..."):
    time.sleep(0.5)

# 左侧功能选择
st.sidebar.header("功能选择 Function Selection")
menu_selection = st.sidebar.radio(
    "请选择功能",
    ["镜头焦距计算", "视场角与自定义参数4配置", "LPP配置参考"]
)

# 主页面标题
ai_gif = load_lottiefile('lens.json')
col_lottie, _ = st.columns([1, 3])  # 第一列占1份（放动效），第二列占9份（空白）
with col_lottie:
    st_lottie(ai_gif, speed=1.5, height=400, key="Tofu")

# st_lottie(ai_gif, speed=1.5, height=200, key="Tofu")
st.markdown('<h1 class="gradient-title">Welcome to Tofu LensCulc App!</h1>', unsafe_allow_html=True)
st.markdown("## Product Wiki Site: [Tofu Wiki](https://tofuai.helplook.net)")
st.markdown('<div class="custom-divider"></div>', unsafe_allow_html=True)

# 镜头焦距计算模式
if menu_selection == "镜头焦距计算":
    st.markdown('<h2 class="animate-on-load">镜头焦距计算</h2>', unsafe_allow_html=True)
    st.markdown("### 请输入以下参数进行计算")
    
    # 相机选择
    st.subheader("相机选择 Select Sensor")
    cam_selection = st.selectbox(
        "传感器类型",
        config.SENSOR_LIST
    )
    pix_type = config.SENSOR_LIST.index(cam_selection)
    
    # 识别距离设置
    st.subheader("识别距离 Detection Distance")
    DDistance = float(st.slider(
        "距离 (米)", 300, 10000, 500
    ))
    
    # 识别目标选择
    st.subheader("识别目标 Detection Object")
    obj_selection = st.selectbox(
        "目标类型",
        config.OBJ_LIST
    )
    obj = config.OBJ_LIST.index(obj_selection)
    
    # 计算按钮
    st.subheader("计算")
    calculate = st.button('计算焦距')
    
    # 计算逻辑
    if calculate:
        with st.spinner("正在计算，请稍候..."):
            time.sleep(0.8)  # 增加计算反馈延迟
            
            # 确定像素尺寸
            if pix_type == 0:
                pix_size = 2.9
            elif pix_type == 1:
                pix_size = 17
            elif pix_type == 2:
                pix_size = 12
            elif pix_type == 3:
                pix_size = 15

            # 计算焦距
            if obj == 0:  # 人
                Obj_size = 1.7
                if pix_size < 10:
                    Focal_Len = 60.0 * pix_size * DDistance / (Obj_size * 1000)
                else:
                    Focal_Len = 11.0 * pix_size * DDistance / (Obj_size * 1000)
            elif obj == 1:  # 车
                Obj_size = 5.0
                if pix_size < 10:
                    Focal_Len = 60.0 * pix_size * DDistance / (Obj_size * 1000)
                else:
                    Focal_Len = 22.0 * pix_size * DDistance / (Obj_size * 1000)
            elif obj == 2:  # 船
                Obj_size = 12.0
                if pix_size < 10:
                    Focal_Len = 60.0 * pix_size * DDistance / (Obj_size * 1000)
                else:
                    Focal_Len = 40.0 * pix_size * DDistance / (Obj_size * 1000)
            elif obj == 3:  # 无人机
                Obj_size = 0.4
                if pix_size < 10:
                    Focal_Len = 15.0 * pix_size * DDistance / (Obj_size * 1000)
                else:
                    Focal_Len = 2.35 * pix_size * DDistance / (Obj_size * 1000)

        # 显示结果（带卡片动效）
        st.subheader("计算结果")
        str_dis = f'镜头焦距 Focal Length of Lens: {int(Focal_Len)}mm'
        st.markdown(f'<div class="result-card"><p style="font-size: 24px;">{str_dis}</p></div>', unsafe_allow_html=True)
    else:
        st.info('请选择参数后点击计算按钮 Enter the params and Click Calculate')

# LPP参数配置模式
elif menu_selection == "视场角与自定义参数4配置":
    st.markdown('<h2 class="animate-on-load">视场角与自定义参数4配置</h2>', unsafe_allow_html=True)
    st.markdown("### 请输入以下参数")
    
    col1, col2 = st.columns(2)
    
    with col1:
        # 可见光参数
        st.subheader("可见光参数")
        visible_pixel_size = st.number_input(
            "可见光像元尺寸 (μm)", 
            min_value=1.0, 
            value=2.9, 
            step=0.1
        )
        visible_resolution = st.selectbox(  # 改为选择框
            "可见光水平分辨率", 
            [1920, 2560, 2688]
        )
        visible_focal = st.number_input(
            "可见光镜头焦距 (mm)", 
            min_value=1.0, 
            value=25.0, 
            step=1.0
        )
        
        # 计算按钮移至左下
        st.subheader("计算")
        calculate_lpp = st.button('计算视场角与参数4')
    
    with col2:
        # 红外参数
        st.subheader("红外参数")
        ir_pixel_size = st.selectbox(
            "红外像元尺寸 (μm)",
            [12, 17]
        )
        ir_resolution = st.selectbox(
            "红外水平分辨率",
            [384, 640, 1280],
            index=1
        )
        ir_focal = st.number_input(
            "红外镜头焦距 (mm)", 
            min_value=1.0, 
            value=25.0, 
            step=1.0
        )
    
    # 计算结果展示
    if calculate_lpp:
        with st.spinner("正在计算，请稍候..."):
            time.sleep(0.8)
            # 可见光视场角计算（水平）
            visible_h_fov = 2 * math.atan((visible_resolution * visible_pixel_size / 1000) / (2 * visible_focal)) * (180 / math.pi)
            # 红外视场角计算（水平）
            ir_h_fov = 2 * math.atan((ir_resolution * ir_pixel_size / 1000) / (2 * ir_focal)) * (180 / math.pi)

            #脱靶量协议
            part1 = math.ceil((visible_h_fov * 10) / ir_h_fov)
            
            if abs(visible_h_fov - 60) < 1e-9:
                part2 = 0
            else:
                part2 = math.ceil((100 * visible_h_fov) / 60) * 256
            
            param4_MD = part1 + part2

        st.subheader("计算结果")
        
        with st.expander("可见光参数结果", expanded=True):
            st.markdown(f'<div class="result-card">可见光水平视场角: {visible_h_fov:.2f}°</div>', unsafe_allow_html=True)
        
        with st.expander("红外参数结果", expanded=True):
            st.markdown(f'<div class="result-card">红外水平视场角: {ir_h_fov:.2f}°</div>', unsafe_allow_html=True)
        
        if ir_h_fov != 0:
            ratio = (visible_h_fov * 10) / ir_h_fov
            rounded_up = math.ceil(ratio)
            with st.expander("LPP协议下自定义参数4", expanded=True):
                st.markdown(f'<div class="result-card">配置值: {rounded_up}</div>', unsafe_allow_html=True)

            with st.expander("脱靶量协议下自定义参数4", expanded=True):
                st.markdown(f'<div class="result-card">配置值: {param4_MD}</div>', unsafe_allow_html=True)
        else:
            st.error("红外水平视场角不能为0，无法计算比例")

# LPP配置参考模式
elif menu_selection == "LPP配置参考":
    st.markdown('<h2 class="animate-on-load">LPP配置参考</h2>', unsafe_allow_html=True)
    st.markdown("### 请输入参数进行计算")
    
    # 输入参数
    st.subheader("输入参数")
    col_input = st.columns(1)
    with col_input[0]:
        max_fov = st.number_input(
            "相机最大视场角（°）",
            min_value=0.1,
            value=60.0,
            step=0.1
        )
        ptz_speed = st.number_input(
            "云台速度细分（°）",
            min_value=0.001,
            value=0.01,
            step=0.001,
            format="%.3f"
        )
        
        calculate_lpp_ref = st.button("计算LPP配置参数")
    
    # 计算并显示结果
    if calculate_lpp_ref:
        with st.spinner("正在计算，请稍候..."):
            time.sleep(0.8)
            custom_param7 = math.ceil(3.5 * max_fov / (ptz_speed * 60))
            custom_param6 = math.ceil(custom_param7 * 0.02)
            motion_coeff = math.ceil(custom_param7 * 1.5)
            integral_coeff = math.ceil(motion_coeff * 0.03)
        
        st.subheader("计算结果")
        col_output = st.columns(1)
        with col_output[0]:
            st.markdown(f'<div class="result-card">自定义参数5: 1</div>', unsafe_allow_html=True)
            st.markdown(f'<div class="result-card">自定义参数6: {custom_param6}</div>', unsafe_allow_html=True)
            st.markdown(f'<div class="result-card">自定义参数7: {custom_param7}</div>', unsafe_allow_html=True)
            st.markdown(f'<div class="result-card">运动系数: {motion_coeff}</div>', unsafe_allow_html=True)
            st.markdown(f'<div class="result-card">差分系数: 55</div>', unsafe_allow_html=True)
            st.markdown(f'<div class="result-card">积分系数: {integral_coeff}</div>', unsafe_allow_html=True)
