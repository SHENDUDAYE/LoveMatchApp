from zipfile import ZipFile
import os

# 创建 main.py 修复版内容
main_py_code = """
import streamlit as st
import datetime
import random
from datetime import date

# ------------------------ 基础数据配置 ------------------------

zodiacs = ["鼠","牛","虎","兔","龙","蛇","马","羊","猴","鸡","狗","猪"]
tiangans = ["甲","乙","丙","丁","戊","己","庚","辛","壬","癸"]
dizhis = ["子","丑","寅","卯","辰","巳","午","未","申","酉","戌","亥"]

nayin_map = {
    ("甲子","乙丑"): ("海中金", "金"), ("丙寅","丁卯"): ("炉中火", "火"),
    ("戊辰","己巳"): ("大林木", "木"), ("庚午","辛未"): ("路旁土", "土"),
    ("壬申","癸酉"): ("剑锋金", "金"), ("甲戌","乙亥"): ("山头火", "火"),
    ("丙子","丁丑"): ("涧下水", "水"), ("戊寅","己卯"): ("城头土", "土"),
    ("庚辰","辛巳"): ("白蜡金", "金"), ("壬午","癸未"): ("杨柳木", "木"),
    ("甲申","乙酉"): ("泉中水", "水"), ("丙戌","丁亥"): ("屋上土", "土"),
    ("戊子","己丑"): ("霹雳火", "火"), ("庚寅","辛卯"): ("松柏木", "木"),
    ("壬辰","癸巳"): ("长流水", "水"), ("甲午","乙未"): ("沙中金", "金"),
    ("丙申","丁酉"): ("山下火", "火"), ("戊戌","己亥"): ("平地木", "木"),
    ("庚子","辛丑"): ("壁上土", "土"), ("壬寅","癸卯"): ("金箔金", "金"),
    ("甲辰","乙巳"): ("覆灯火", "火"), ("丙午","丁未"): ("天河水", "水"),
    ("戊申","己酉"): ("大驿土", "土"), ("庚戌","辛亥"): ("钗钏金", "金"),
    ("壬子","癸丑"): ("桑柘木", "木"), ("甲寅","乙卯"): ("大溪水", "水"),
    ("丙辰","丁巳"): ("沙中土", "土"), ("戊午","己未"): ("天上火", "火"),
    ("庚申","辛酉"): ("石榴木", "木"), ("壬戌","癸亥"): ("大海水", "水")
}

marriage_levels = {
    ("鼠","牛"): "上上婚", ("虎","猪"): "上等婚", ("兔","狗"): "上等婚",
    ("蛇","猴"): "中等婚", ("马","羊"): "中等婚", ("龙","鸡"): "中等婚",
    ("鼠","马"): "下等婚", ("牛","羊"): "下等婚", ("虎","猴"): "下等婚",
    ("兔","鸡"): "下等婚", ("龙","狗"): "下等婚", ("蛇","猪"): "下等婚"
}

shengke_map = {
    ("木", "火"): "相生", ("火", "土"): "相生", ("土", "金"): "相生",
    ("金", "水"): "相生", ("水", "木"): "相生",
    ("木", "土"): "相克", ("土", "水"): "相克", ("水", "火"): "相克",
    ("火", "金"): "相克", ("金", "木"): "相克"
}

def get_zodiac(year):
    return zodiacs[(year - 4) % 12]

def get_ganzhi(year):
    return tiangans[(year - 4) % 10] + dizhis[(year - 4) % 12]

def get_nayin(ganzhi):
    for key, value in nayin_map.items():
        if ganzhi in key:
            return value
    return ("未知", "未知")

def get_zodiac_relation(z1, z2):
    liuhe = [("鼠","牛"), ("虎","猪"), ("兔","狗"), ("龙","鸡"), ("蛇","猴"), ("马","羊")]
    liuchong = [("鼠","马"), ("牛","羊"), ("虎","猴"), ("兔","鸡"), ("龙","狗"), ("蛇","猪")]
    liuhai = [("鼠","羊"), ("牛","马"), ("虎","蛇"), ("兔","龙"), ("狗","鸡"), ("猴","猪")]
    sanhe = [["猴","鼠","龙"], ["虎","马","狗"], ["蛇","鸡","牛"], ["猪","兔","羊"]]

    if (z1, z2) in liuhe or (z2, z1) in liuhe:
        return {"type": "六合", "desc": "天作之合", "score": 95}
    elif (z1, z2) in liuchong or (z2, z1) in liuchong:
        return {"type": "六冲", "desc": "相冲不合", "score": 45}
    elif (z1, z2) in liuhai or (z2, z1) in liuhai:
        return {"type": "六害", "desc": "暗中相害", "score": 55}
    elif any(z1 in g and z2 in g for g in sanhe):
        return {"type": "三合", "desc": "三合吉配", "score": 85}
    elif z1 == z2:
        return {"type": "同属相", "desc": "需具体分析", "score": 75}
    else:
        return {"type": "普通", "desc": "中性组合", "score": 65}

# 主程序入口
st.title("修复版：命理婚配分析")
st.write("本页面用于测试 get_zodiac_relation 是否定义错误")

z1 = st.selectbox("男方生肖", zodiacs)
z2 = st.selectbox("女方生肖", zodiacs)

if st.button("分析生肖关系"):
    rel = get_zodiac_relation(z1, z2)
    st.write(f"配对关系：{rel['type']} - {rel['desc']}（评分：{rel['score']}）")
"""

# 写入 main.py
os.makedirs("/mnt/data/lovematchapp_fixed", exist_ok=True)
with open("/mnt/data/lovematchapp_fixed/main.py", "w", encoding="utf-8") as f:
    f.write(main_py_code)

# 打包为 ZIP 文件
zip_path = "/mnt/data/lovematchapp_fixed.zip"
with ZipFile(zip_path, "w") as zipf:
    zipf.write("/mnt/data/lovematchapp_fixed/main.py", arcname="main.py")

zip_path
