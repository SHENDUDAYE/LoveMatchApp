
import streamlit as st
import datetime

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

def get_ganzhi(year):
    gan_index = (year - 4) % 10
    zhi_index = (year - 4) % 12
    return tiangans[gan_index] + dizhis[zhi_index]

def get_zodiac(year):
    return zodiacs[(year - 4) % 12]

def get_nayin(ganzhi):
    for key, value in nayin_map.items():
        if ganzhi in key:
            return value
    return ("未知", "未知")

def run_analysis(man_date, woman_date):
    my, wy = man_date.year, woman_date.year
    m_zodiac, w_zodiac = get_zodiac(my), get_zodiac(wy)
    m_gz, w_gz = get_ganzhi(my), get_ganzhi(wy)
    m_nayin, w_nayin = get_nayin(m_gz)[0], get_nayin(w_gz)[0]
    return f"👦 男方：{my}年 属{m_zodiac} 纳音：{m_nayin}\n"            f"👧 女方：{wy}年 属{w_zodiac} 纳音：{w_nayin}\n"            f"📊 配对简析：{m_zodiac}配{w_zodiac}，纳音五行为【{m_nayin}】配【{w_nayin}】。"

def main():
    st.set_page_config(page_title="良缘婚配分析师", page_icon="💘")
    st.title("💘 良缘婚配分析师")
    st.markdown("依据出生年推演生肖与纳音五行，快速婚配评估")

    col1, col2 = st.columns(2)
    with col1:
        man_date = st.date_input("男方出生日期", datetime.date(1990,1,1))
    with col2:
        woman_date = st.date_input("女方出生日期", datetime.date(1992,1,1))

    if st.button("🔮 开始配对分析"):
        result = run_analysis(man_date, woman_date)
        st.markdown("### 📋 配对结果：")
        st.code(result)

if __name__ == "__main__":
    main()
    