import streamlit as st
import datetime
import random
from datetime import date

# ------------------------ 基础数据配置 ------------------------

zodiacs = ["鼠","牛","虎","兔","龙","蛇","马","羊","猴","鸡","狗","猪"]
tiangans = ["甲","乙","丙","丁","戊","己","庚","辛","壬","癸"]
dizhis = ["子","丑","寅","卯","辰","巳","午","未","申","酉","戌","亥"]

# 纳音五行对照表（简化版）
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

# 三世书婚配等级
marriage_levels = {
    ("鼠","牛"): "上上婚", ("虎","猪"): "上等婚", ("兔","狗"): "上等婚",
    ("蛇","猴"): "中等婚", ("马","羊"): "中等婚", ("龙","鸡"): "中等婚",
    ("鼠","马"): "下等婚", ("牛","羊"): "下等婚", ("虎","猴"): "下等婚",
    ("兔","鸡"): "下等婚", ("龙","狗"): "下等婚", ("蛇","猪"): "下等婚"
}

# ------------------------ 核心算法模块 ------------------------

def get_zodiac(year):
    """获取生肖"""
    return zodiacs[(year - 4) % 12]

def get_ganzhi(year):
    """获取年柱天干地支"""
    gan_index = (year - 4) % 10
    zhi_index = (year - 4) % 12
    return tiangans[gan_index] + dizhis[zhi_index]

def get_nayin(ganzhi):
    """获取纳音五行"""
    for key, value in nayin_map.items():
        if ganzhi in key:
            return value
    return ("", "")

def calculate_marriage_score(z1, z2, w1, w2):
    """综合评分算法"""
    base_scores = {"六合":95, "三合":85, "半合":75, "普通":65, "六害":55, "六冲":45}
    relation = get_zodiac_relation(z1, z2)["type"]
    score = base_scores.get(relation, 60)
    
    # 五行相生加成
    if (w1, w2) in shengke_map and shengke_map[(w1, w2)] == "相生":
        score += 15
    elif (w2, w1) in shengke_map and shengke_map[(w2, w1)] == "相生":
        score += 10
    
    return min(max(score, 0), 100)

# ------------------------ 功能模块 ------------------------

def show_zodiac_analysis(z1, z2):
    """生肖关系分析"""
    rel_info = get_zodiac_relation(z1, z2)
    with st.expander("🔮 生肖配对分析", expanded=True):
        cols = st.columns([1,3])
        cols[0].metric("生肖组合", f"{z1} + {z2}")
        cols[1].metric("配对类型", rel_info["type"])
        st.progress(calculate_marriage_score(z1, z2, "", "")/100)

def show_nayin_analysis(gz1, gz2):
    """纳音五行分析"""
    ny1, wx1 = get_nayin(gz1)
    ny2, wx2 = get_nayin(gz2)
    
    with st.expander("🌌 纳音五行分析"):
        cols = st.columns(2)
        cols[0].write(f"男方年命：{gz1}{ny1}({wx1})")
        cols[1].write(f"女方年命：{gz2}{ny2}({wx2})")
        
        # 五行生克判断
        if (wx1, wx2) in shengke_map:
            rel = shengke_map[(wx1, wx2)]
            st.success(f"五行关系：{rel}({wx1}→{wx2})")
        else:
            st.info("五行无直接生克")

def show_marriage_level(z1, z2):
    """三世书婚配等级"""
    level = marriage_levels.get((z1,z2), marriage_levels.get((z2,z1), "需合八字"))
    with st.expander("📜 三世书婚配"):
        st.subheader(f"婚配等级：{level}")
        if "上" in level:
            st.markdown("> 《三命通会》云：阴阳会合，琴瑟和谐")
        elif "中" in level:
            st.markdown("> 《渊海子平》云：刚柔相济，亦主吉祥")
        else:
            st.markdown("> 《滴天髓》云：冲克刑害，须凭调解")

# ------------------------ 界面交互 ------------------------

def main():
    st.set_page_config(page_title="周易婚配系统", layout="wide")
    st.title("🎎 周易婚配预测系统")
    
    # 侧边栏控制
    with st.sidebar:
        st.header("⚙️ 参数设置")
        analysis_mode = st.radio("分析模式", ["手动输入", "随机测试"])
        
        if analysis_mode == "手动输入":
            man_year = st.number_input("男方出生年", 1900, 2100, 1990)
            woman_year = st.number_input("女方出生年", 1900, 2100, 1993)
        else:
            man_year = random.randint(1980, 2010)
            woman_year = random.randint(1980, 2010)
            st.write(f"随机测试年份：男{man_year} / 女{woman_year}")
    
    # 主显示区域
    tab1, tab2, tab3 = st.tabs(["核心分析", "吉日推荐", "子嗣预测"])
    
    with tab1:
        z1, z2 = get_zodiac(man_year), get_zodiac(woman_year)
        gz1, gz2 = get_ganzhi(man_year), get_ganzhi(woman_year)
        
        show_zodiac_analysis(z1, z2)
        show_nayin_analysis(gz1, gz2)
        show_marriage_level(z1, z2)
        
        # 综合评分
        score = calculate_marriage_score(z1, z2, *[get_nayin(gz1)[1], get_nayin(gz2)[1]])
        st.divider()
        st.subheader(f"综合评分：{score}/100")
        st.write("《命理约言》云：天地之道，贵在阴阳调和")
    
    with tab2:
        current_year = datetime.date.today().year
        good_years = [current_year + i for i in range(3) if (current_year + i - man_year) % 12 in [4,8,0]]
        st.markdown(f"""
        ### 🎋 推荐婚期
        - 近期吉年：{', '.join(map(str, good_years))}
        - 优选月份：双春年闰月、三合月（参考具体年份黄历）
        > 《协纪辨方书》云：宜选三合、六合之日，避刑冲破害
        """)
    
    with tab3:
        wx1, wx2 = get_nayin(gz1)[1], get_nayin(gz2)[1]
        st.markdown(f"""
        ### 👶 子嗣预测
        - 生育时机：婚后{random.randint(1,3)}年内见喜
        - 子女数量：主{random.choice([1,2])}孩，可能有双生之喜
        - 五行调和：{"旺" if wx1 != wx2 else "平"}
        > 《滴天髓》云：木火通明主文秀，金水相生多俊俏
        """)

if __name__ == "__main__":
    main()
