#!/usr/bin/env python
# -*- coding: utf-8 -*-

from pathlib import Path
from PIL import Image
import streamlit as st
import requests
from streamlit_lottie import st_lottie
import json
import math

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

# 自定义CSS缩短输入组件宽度（进一步缩小数字输入框）
st.markdown("""
<style>
    /* 下拉选择框 */
    .stSelectbox [data-baseweb="select"] {
        width: 200px;
    }
    /* 数字输入框（带加减按钮的） */
    .stNumberInput {
        width: 200px !important;
    }
    .stNumberInput input {
        width: 150px !important;
    }
    /* 滑动条 */
    .stSlider [data-baseweb="slider"] {
        width: 200px;
    }
    /* 按钮 */
    .stButton button {
        width: 200px;
    }
</style>
""", unsafe_allow_html=True)

# 左侧功能选择
st.sidebar.header("功能选择 Function Selection")
menu_selection = st.sidebar.radio(
    "请选择功能",
    ["镜头焦距计算", "视场角与自定义参数4配置", "LPP配置参考"]
)

# 主页面标题
st.image('line.jpg', width=1600)
ai_gif = load_lottiefile('lens.json')
st_lottie(ai_gif, speed=1.5, height=200, key="Tofu")
st.title("Welcome to Tofu LensCulc App!")
st.markdown("## Product Wiki Site: [Tofu Wiki](https://tofuai.helplook.net)")

# 镜头焦距计算模式
if menu_selection == "镜头焦距计算":
    st.header("镜头焦距计算")
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
    calculate = st.button('计算焦距 Culc Focal Length')
    
    # 计算逻辑
    if calculate:
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

        # 显示结果
        st.subheader("计算结果")
        str_dis = f'镜头焦距 Focal Length of Lens: {int(Focal_Len)}mm'
        st.markdown(f'<p style="font-size: {24}px;">{str_dis}</p>', unsafe_allow_html=True)
    else:
        st.info('请选择参数后点击计算按钮 Enter the params and Click Calculate')

# LPP参数配置模式
elif menu_selection == "视场角与自定义参数4配置":
    st.header("视场角与自定义参数4配置")
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
        calculate_lpp = st.button('计算LPP参数 Culc LPP Params')
    
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
        st.subheader("计算结果")
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

        with st.expander("可见光参数结果", expanded=True):
            st.info(f"可见光水平视场角: {visible_h_fov:.2f}°")
        
        with st.expander("红外参数结果", expanded=True):
            st.info(f"红外水平视场角: {ir_h_fov:.2f}°")
        
        if ir_h_fov != 0:
            ratio = (visible_h_fov * 10) / ir_h_fov
            rounded_up = math.ceil(ratio)
            with st.expander("LPP协议下自定义参数4", expanded=True):
                st.success(f"配置值: {rounded_up}")

            with st.expander("脱靶量协议下自定义参数4", expanded=True):
                st.success(f"配置值: {param4_MD}")
        else:
            st.error("红外水平视场角不能为0，无法计算比例")

# LPP配置参考模式
elif menu_selection == "LPP配置参考":
    st.header("LPP配置参考")
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
        st.subheader("输出结果")
        custom_param7 = math.ceil(3.5 * max_fov / (ptz_speed * 60))
        custom_param6 = math.ceil(custom_param7 * 0.02)
        motion_coeff = math.ceil(custom_param7 * 1.5)
        integral_coeff = math.ceil(motion_coeff * 0.03)
        
        col_output = st.columns(1)
        with col_output[0]:
            st.info(f"自定义参数5: 1")
            st.info(f"自定义参数6: {custom_param6}")
            st.info(f"自定义参数7: {custom_param7}")
            st.info(f"运动系数: {motion_coeff}")
            st.info(f"差分系数: 55")
            st.info(f"积分系数: {integral_coeff}")
