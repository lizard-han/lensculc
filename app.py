#!/usr/bin/env python
# -*- coding: utf-8 -*-

from pathlib import Path
from PIL import Image
import streamlit as st
import requests
from streamlit_lottie import st_lottie
import json

import config
# from utils import load_model, infer_uploaded_image, infer_uploaded_video, infer_uploaded_webcam


def load_lottieurl(url:str):
    r = requests.get(url)
    if r.status_code != 200:
        return None
    return r.json()

def load_lottiefile(filepath:str):
    with open(filepath, 'r') as f:
        return json.load(f)

# setting page layout
st.set_page_config(
    page_title="Tofu Intelligence Lens Culc",
    page_icon='logo.png',
    layout="wide",
    initial_sidebar_state="expanded"
    )

# main page heading
st.image('line.jpg',width=1600)
ai_gif = load_lottiefile('lens.json')
st_lottie(ai_gif, speed=1.5, height=200, key="Tofu")
st.title("Welcome to Tofu LensCulc App!")
st.markdown("## Product Wiki Site: [Tofu Wiki](https://tofuai.helplook.net)")

# sidebar
st.sidebar.header("相机选择Select Sensor")
cam_selection = st.sidebar.selectbox(
        "123",
        config.SENSOR_LIST,
        label_visibility="hidden"
    )

pix_type = config.SENSOR_LIST.index(cam_selection)

st.sidebar.header("识别距离 Dectection Distance")
DDistance = float(st.sidebar.slider(
    "123", 300, 10000, 500,label_visibility="hidden"))


# image/video options
st.sidebar.header("识别目标 Detection Obj")
obj_selection = st.sidebar.selectbox(
    "123",
    config.OBJ_LIST,
    label_visibility="hidden"
)

obj = config.OBJ_LIST.index(obj_selection)



if st.button('计算 Culc'):
    
    # "Visual 2.9um pixel",
    # "Uncooled Thermal 17um pixel",
    # "Uncooled Thermal 12um pixel",
    # "CooledThermal 15um pixel"

    if pix_type==0:
        pix_size = 2.9
    elif pix_type==1:
        pix_size = 17
    elif pix_type==2:
        pix_size = 12
    elif pix_type==3:
        pix_size = 15

    if obj==0: #人
        Obj_size = 1.7
        if pix_size < 10:
            Focal_Len =  60.0 * pix_size * DDistance / (Obj_size * 1000)
        else:
            Focal_Len =  11.0 * pix_size * DDistance / (Obj_size * 1000)
    elif obj==1:#车
        Obj_size = 5.0
        if pix_size < 10:
            Focal_Len =  60.0 * pix_size * DDistance / (Obj_size * 1000)
        else:
            Focal_Len =  22.0 * pix_size * DDistance / (Obj_size * 1000)
    elif obj==2:#船
        Obj_size = 12.0
        if pix_size < 10:
            Focal_Len =  60.0 * pix_size * DDistance / (Obj_size * 1000)
        else:
            Focal_Len =  40.0 * pix_size * DDistance / (Obj_size * 1000)
    elif obj==3: #无人机
        Obj_size = 0.4
        if pix_size < 10:
            Focal_Len =  15.0 * pix_size * DDistance / (Obj_size * 1000)
        else :
            Focal_Len =  2.35 * pix_size * DDistance / (Obj_size * 1000)

    str_dis = '镜头焦距 Focal Length of Lens:' + str(int(Focal_Len)) + 'mm'
    # st.markdown(str_dis)
    st.markdown(f'<p style="font-size: {24}px;">{str_dis}</p>', unsafe_allow_html=True)
else:
    st.write('请选择参数后点击按钮 Enter the params and Click')