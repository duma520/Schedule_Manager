import sys
import os
import shutil
from PyQt5.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, 
                             QTableView, QPushButton, QLabel, QLineEdit, QDateEdit, 
                             QComboBox, QMessageBox, QHeaderView, QFormLayout, QDialog,
                             QTimeEdit, QDialogButtonBox, QMenu, QTableWidget, QTableWidgetItem,
                             QCheckBox, QSpinBox, QGroupBox, QGridLayout, QWIDGETSIZE_MAX,
                             QListWidget,  QListWidgetItem
                             )
from PyQt5.QtGui import QIcon, QStandardItemModel, QStandardItem, QColor, QFont
from PyQt5.QtCore import Qt, QDate, QTime, QSettings, QSize, QTimer
import sqlite3
from sqlite3 import Error
from datetime import datetime, timedelta

class ProjectInfo:
    """项目信息元数据（集中管理所有项目相关信息）
    
    特性：
    - 集中管理项目元数据
    - 提供多种格式的输出方法
    - 包含详细的帮助文档
    - 支持版本比较
    """
    
    # 基础元数据
    VERSION = "1.57.0"
    BUILD_DATE = "2026-08-20"
    AUTHOR = "杜玛"
    LICENSE = "MIT"
    COPYRIGHT = "© 永久 杜玛"
    URL = "https://github.com/duma520"
    MAINTAINER_EMAIL = "不提供"
    NAME = "排班表管理系统"
    DESCRIPTION = "一个简单易用的排班表管理系统，支持多种功能"
    
    # 依赖项信息
    DEPENDENCIES = {
        "Python": ">=3.8",
        "pandas": ">=1.3.0",
        "numpy": ">=1.21.0"
    }
    
    # 详细的帮助文档
    HELP_TEXT = """
排班表管理系统使用说明:

1. 基本功能
   - 创建排班表: 输入员工信息和排班需求
   - 自动排班: 系统根据规则自动生成排班表
   - 手动调整: 可手动调整自动生成的排班
   - 导出报表: 支持Excel、PDF等多种格式

2. 快捷键
   - Ctrl+N: 新建排班表
   - Ctrl+O: 打开现有排班表
   - Ctrl+S: 保存当前排班表
   - F1: 显示帮助

3. 常见问题
   Q: 如何添加新员工?
   A: 在"员工管理"界面点击"添加"按钮

   Q: 如何设置排班规则?
   A: 在"设置"->"排班规则"中进行配置

4. 联系支持
   - 官网: https://github.com/duma520
   - 问题反馈: 请通过GitHub提交Issue
"""

    @classmethod
    def get_metadata(cls) -> dict:
        """获取主要元数据字典
        
        返回:
            dict: 包含版本、作者、许可证等核心元数据的字典
        """
        return {
            'name': cls.NAME,
            'version': cls.VERSION,
            'build_date': cls.BUILD_DATE,
            'author': cls.AUTHOR,
            'license': cls.LICENSE,
            'copyright': cls.COPYRIGHT,
            'url': cls.URL,
            'description': cls.DESCRIPTION
        }

    @classmethod
    def get_header(cls) -> str:
        """生成标准化的项目头信息
        
        返回:
            str: 格式化后的项目头信息字符串
        """
        return f"{cls.NAME} {cls.VERSION} | {cls.LICENSE} License | {cls.URL}"

    @classmethod
    def get_full_info(cls) -> str:
        """获取完整的项目信息
        
        返回:
            str: 包含所有元数据的格式化字符串
        """
        return (
            f"{cls.NAME} - {cls.DESCRIPTION}\n"
            f"版本: {cls.VERSION} (编译于 {cls.BUILD_DATE})\n"
            f"作者: {cls.AUTHOR} | 许可证: {cls.LICENSE}\n"
            f"版权: {cls.COPYRIGHT}\n"
            f"主页: {cls.URL}\n"
            f"依赖: {', '.join(f'{k}{v}' for k, v in cls.DEPENDENCIES.items())}"
        )

    @classmethod
    def compare_version(cls, version_str: str) -> int:
        """比较当前版本与指定版本
        
        参数:
            version_str (str): 要比较的版本字符串
            
        返回:
            int: 
                -1: 当前版本 < 指定版本
                0: 版本相同
                1: 当前版本 > 指定版本
                
        异常:
            ValueError: 当版本格式无效时抛出
        """
        def parse_version(v):
            parts = v.split('.')
            if len(parts) != 3:
                raise ValueError(f"无效的版本格式: {v}")
            return tuple(int(part) for part in parts)
        
        try:
            current = parse_version(cls.VERSION)
            other = parse_version(version_str)
            return (current > other) - (current < other)
        except (ValueError, AttributeError) as e:
            raise ValueError(f"版本比较失败: {str(e)}")



# 马卡龙色系定义
class MacaronColors:
    # 马卡龙色系 300种核心色全色域
    # 粉色系（30色）    
    SAKURA_PINK = QColor('#FFB7CE')  # 樱花粉
    BABY_PINK = QColor('#FFD1DC')  # 婴儿粉
    COTTON_CANDY = QColor('#FFB8D9')  # 棉花糖粉
    PEACH_BLOSSOM = QColor('#FFB3BF')  # 桃花粉
    ROSE_QUARTZ = QColor('#F7CAC9')  # 玫瑰石英粉
    PALE_PINK = QColor('#FADADD')  # 苍粉
    BLUSH_PINK = QColor('#FE828C')  # 腮红粉
    PINK_LEMONADE = QColor('#FFE5E2')  # 粉柠水
    POWDER_PINK = QColor('#FFB2D0')  # 粉末粉
    MACARON_PINK = QColor('#FF9AA2')  # 马卡龙粉
    RASPBERRY_SORBET = QColor('#FF6B8B')  # 树莓雪芭粉
    BUBBLEGUM = QColor('#FFC1CC')  # 泡泡糖粉
    FAIRY_PINK = QColor('#FFD4E5')  # 仙女粉
    STRAWBERRY_MILK = QColor('#FFDFE2')  # 草莓牛奶粉
    PINK_MIST = QColor('#FFC3D7')  # 粉雾
    TUTU_PINK = QColor('#F8C3CD')  # 芭蕾粉
    PEONY_PINK = QColor('#E6A8B7')  # 芍药粉
    CHERRY_BLOSSOM = QColor('#FFCCD5')  # 樱花瓣粉
    CARNATION = QColor('#FFA6C9')  # 康乃馨粉
    BALLET_SLIPPER = QColor('#EDC9D8')  # 芭蕾舞鞋粉
    WATERMELON = QColor('#FD5B78')  # 西瓜粉
    LOLLIPOP = QColor('#D291BC')  # 棒棒糖粉
    CUPCAKE = QColor('#F6C9D6')  # 纸杯蛋糕粉
    PARISIAN_PINK = QColor('#DA9BB2')  # 巴黎粉
    PINK_SHERBET = QColor('#F78FA7')  # 雪酪粉
    MIMOSA = QColor('#FFE4E1')  # 含羞草粉
    PRETTY_IN_PINK = QColor('#F3A4B5')  # 少女粉
    SUGAR_PLUM = QColor('#DDA0DD')  # 糖梅粉
    PINK_PEARL = QColor('#E7CFCA')  # 珍珠粉
    FLAMINGO = QColor('#FC8EAC')  # 火烈鸟粉
    ROSE_PINK = QColor('#FF66CC')  # 玫瑰粉
    # 蓝色系（30色）
    BABY_BLUE = QColor('#89CFF0')  # 婴儿蓝
    SKY_BLUE = QColor('#87CEEB')  # 天空蓝
    POWDER_BLUE = QColor('#B0E0E6')  # 粉末蓝
    ICE_BLUE = QColor('#D4F1F9')  # 冰蓝
    PERIWINKLE = QColor('#C3CDE6')  # 长春花蓝
    AQUA_MARINE = QColor('#7FFFD4')  # 碧蓝
    SEAFOAM = QColor('#93E9BE')  # 海沫蓝
    MISTY_BLUE = QColor('#B7D3DF')  # 雾霭蓝
    PASTEL_BLUE = QColor('#A2C5E0')  # 淡彩蓝
    ROBIN_EGG = QColor('#96DED1')  # 知更鸟蛋蓝
    CORNFOWER = QColor('#9ACEEB')  # 矢车菊蓝
    CADET_BLUE = QColor('#B0B7C6')  # 学员蓝
    BLUE_MIST = QColor('#B7D3DF')  # 蓝雾
    POLAR_BLUE = QColor('#D4F1F9')  # 极地蓝
    BERMUDA = QColor('#7FB7D4')  # 百慕大蓝
    COTTON_BLUE = QColor('#BCD2E8')  # 棉花蓝
    SPA_BLUE = QColor('#C6E6FB')  # 水疗蓝
    BREEZY_BLUE = QColor('#C6E3F7')  # 微风蓝
    BLUEBERRY = QColor('#6B7FD7')  # 蓝莓蓝
    ANGEL_BLUE = QColor('#C6D4E8')  # 天使蓝
    BLUE_FROST = QColor('#C2D4E4')  # 冰霜蓝
    MORNING_GLORY = QColor('#9AC1D9')  # 朝颜蓝
    PEACOCK_BLUE = QColor('#00A1C9')  # 孔雀蓝
    TIFFANY = QColor('#81D8D0')  # 蒂芙尼蓝
    AQUA_SKY = QColor('#7FC7D4')  # 水色天空
    MARINA = QColor('#71C6D8')  # 码头蓝
    POOL_BLUE = QColor('#A5D5E6')  # 泳池蓝
    DENIM_LIGHT = QColor('#A4C4E0')  # 浅牛仔蓝
    BLUE_JAY = QColor('#A4C8E1')  # 蓝松鸦蓝
    BLUE_HORIZON = QColor('#C6D4E8')  # 地平线蓝
    # 绿色系（30色）
    MINT_GREEN = QColor('#98FF98')  # 薄荷绿
    PISTACHIO = QColor('#93C572')  # 开心果绿
    SEAFOAM_GREEN = QColor('#9FE2BF')  # 海沫绿
    PALE_GREEN = QColor('#C1E1C1')  # 苍绿
    TEA_GREEN = QColor('#D0F0C0')  # 茶绿
    CELADON = QColor('#ACE1AF')  # 青瓷绿
    PEAR_GREEN = QColor('#D1E189')  # 梨绿
    WASABI = QColor('#C4D6A4')  # 芥末绿
    PALE_OLIVE = QColor('#C9DC89')  # 浅橄榄绿
    MEADOW_GREEN = QColor('#C1FBA4')  # 草甸绿
    APPLE_MINT = QColor('#D0EBA8')  # 苹果薄荷绿
    SPRING_BUD = QColor('#A7F432')  # 春芽绿
    LIME_PULP = QColor('#D1E189')  # 青柠肉绿
    NEON_MINT = QColor('#98FF98')  # 霓虹薄荷
    FROSTED_MINT = QColor('#D1E5C2')  # 霜冻薄荷
    PINEAPPLE_GREEN = QColor('#C9DC87')  # 凤梨绿
    KIWI = QColor('#C1E1A4')  # 奇异果绿
    HONEYDEW_GREEN = QColor('#F0FFF0')  # 蜜瓜绿
    LIGHT_GRASS = QColor('#C1E4C5')  # 浅草绿
    GLACIER_GREEN = QColor('#C1E5D3')  # 冰川绿
    PASTEL_GREEN = QColor('#B5EAD7')  # 淡彩绿
    SOFT_EMERALD = QColor('#A4D4AE')  # 柔翡翠
    SAFARI_GREEN = QColor('#B8D8B0')  # 丛林绿
    CLOVER = QColor('#B0D3AB')  # 三叶草绿
    PEA_GREEN = QColor('#89C35C')  # 豌豆绿
    GUM_LEAF = QColor('#ACC9B9')  # 桉树叶绿
    SPRING_RAIN = QColor('#A3C8B0')  # 春雨绿
    PASTEL_PEA = QColor('#B0EBB4')  # 淡豌豆绿
    FROG_PRINCE = QColor('#A5D152')  # 青蛙王子绿
    LEAF_GREEN = QColor('#B2D3C2')  # 嫩叶绿
    APPLE_GREEN = QColor('#8DB600')  # 苹果绿
    # 紫色系（30色）
    LAVENDER = QColor('#E6E6FA')  # 薰衣草紫
    LILAC = QColor('#C8A2C8')  # 丁香紫
    PALE_PURPLE = QColor('#FAE6FA')  # 淡紫
    WISTERIA = QColor('#C9A0DC')  # 紫藤色
    THISTLE = QColor('#D8BFD8')  # 蓟紫
    ORCHID = QColor('#DA70D6')  # 兰花紫
    MAUVE = QColor('#E0B0FF')  # 木槿紫
    HELIOTROPE = QColor('#D462FF')  # 缬草紫
    PASTEL_PURPLE = QColor('#CA9BF7')  # 淡彩紫
    GRAPE_SODA = QColor('#CCACED')  # 葡萄苏打紫
    LILAC_MIST = QColor('#D5C7E8')  # 紫雾
    LILAC_LUSTER = QColor('#AE98AA')  # 丁香光泽紫
    SOFT_LAVENDER = QColor('#D7BDE2')  # 柔薰衣草
    PURPLE_HAZE = QColor('#B399D4')  # 紫色薄雾
    MYSTIC = QColor('#D8BFD8')  # 神秘紫
    CREPE = QColor('#CA9BF7')  # 绉纱紫
    MAGIC_MINT = QColor('#AAF0D1')  # 魔法薄荷紫
    PURPLE_RAIN = QColor('#B399D4')  # 紫雨
    VIOLET_TULIP = QColor('#C5A0E4')  # 紫郁金香
    PASTEL_VIOLET = QColor('#CB99C9')  # 淡紫罗兰
    DUSK = QColor('#89729E')  # 黄昏紫
    PURPLE_AMETHYST = QColor('#9966CC')  # 紫水晶
    PURPLE_DRAGON = QColor('#C38EC7')  # 紫龙
    ROYAL_PURPLE = QColor('#7851A9')  # 皇家紫
    SOFT_PURPLE = QColor('#B695C0')  # 柔和紫
    PURPLE_SAGE = QColor('#B5A8C0')  # 紫鼠尾草
    MAGENTA = QColor('#FF00FF')  # 品红
    PINK_PURPLE = QColor('#DB7093')  # 粉紫
    PURPLE_PLUM = QColor('#9C51B6')  # 紫李子
    PURPLE_ORCHID = QColor('#7A4988')  # 紫兰花
    # 黄色系（30色）
    LEMON_CHIFFON = QColor('#FFFACD')  # 柠檬雪纺黄
    PASTEL_YELLOW = QColor('#FDFD96')  # 淡彩黄
    CREAM = QColor('#FFFDD0')  # 奶油黄
    BANANA = QColor('#FFE135')  # 香蕉黄
    MANGO = QColor('#FFD700')  # 芒果黄
    BUTTER = QColor('#F5DEB3')  # 黄油黄
    MAIZE = QColor('#FBEC5D')  # 玉米黄
    CANARY = QColor('#FFFF99')  # 金丝雀黄
    PASTEL_GOLD = QColor('#F0E68C')  # 淡金
    STRAW = QColor('#E4D96F')  # 稻草黄
    GOLDENROD = QColor('#F9D857')  # 金菊黄
    PASTEL_YELLOW = QColor('#FDFD96')  # 淡黄
    CORN = QColor('#FBEC5D')  # 玉米黄
    LEMON = QColor('#FFF700')  # 柠檬黄
    YELLOW_CRAYOLA = QColor('#FCE883')  # 蜡笔黄
    GOLD = QColor('#FFD700')  # 金色
    YELLOW_ROSE = QColor('#FFF000')  # 黄玫瑰
    SUNFLOWER = QColor('#FFDA03')  # 向日葵黄
    PASTEL_LEMON = QColor('#FFF44F')  # 淡柠檬黄
    GOLDEN_YELLOW = QColor('#FFDF00')  # 金黄
    YELLOW_ORANGE = QColor('#FFAE42')  # 黄橙
    PASTEL_GOLD = QColor('#F0E68C')  # 淡金
    YELLOW_GREEN = QColor('#9ACD32')  # 黄绿
    CITRINE = QColor('#E4D00A')  # 柠檬晶黄
    YELLOW_TAN = QColor('#FFE36B')  # 黄褐色
    GOLDEN_BROWN = QColor('#996515')  # 金棕
    YELLOW_OCRE = QColor('#C19A6B')  # 赭黄
    PASTEL_CREAM = QColor('#FFFDD0')  # 淡奶油黄
    BRIGHT_YELLOW = QColor('#FFEA00')  # 亮黄
    SUNSHINE = QColor('#FFFD37')  # 阳光黄
    # 橙色系（30色）
    PEACH = QColor('#FFDAB9')  # 桃子橙
    APRICOT = QColor('#FBCEB1')  # 杏橙
    CORAL = QColor('#FF7F50')  # 珊瑚橙
    SALMON = QColor('#FFA07A')  # 鲑鱼橙
    PUMPKIN = QColor('#FF7518')  # 南瓜橙
    MANGO_TANGO = QColor('#FF8243')  # 芒果橙
    PASTEL_ORANGE = QColor('#FFB347')  # 淡橙
    MELON = QColor('#FDBCB4')  # 蜜瓜橙
    SUNSET = QColor('#FAD6A5')  # 日落橙
    CREAMSICLE = QColor('#FFB347')  # 奶油冰橙
    ORANGE_SORBET = QColor('#FFA474')  # 橙味雪芭
    TANGERINE = QColor('#F28500')  # 柑橘橙
    PEACH_PUFF = QColor('#FFDAB9')  # 桃扑橙
    CARROT = QColor('#ED9121')  # 胡萝卜橙
    ORANGE_PEEL = QColor('#FF9F00')  # 橙皮橙
    BRIGHT_ORANGE = QColor('#FFAC1C')  # 亮橙
    PASTEL_PEACH = QColor('#FFCBA4')  # 淡桃橙
    ORANGE_YELLOW = QColor('#F8D568')  # 橙黄
    ORANGE_RED = QColor('#FF4500')  # 橙红
    ORANGE_CRAYOLA = QColor('#FF7538')  # 蜡笔橙
    ORANGE_SHERBET = QColor('#F9A957')  # 橙雪酪
    ORANGE_GROVE = QColor('#FFCC99')  # 橙树林
    ORANGE_CHIFFON = QColor('#F5CBA7')  # 橙雪纺
    ORANGE_LIGHT = QColor('#FFB366')  # 浅橙
    ORANGE_PINK = QColor('#FF9966')  # 橙粉
    ORANGE_TAWNY = QColor('#CC5500')  # 茶色橙
    ORANGE_RUST = QColor('#CD5700')  # 锈橙
    ORANGE_BURNT = QColor('#CC5500')  # 焦橙
    ORANGE_PASTEL = QColor('#FFB347')  # 淡橙
    ORANGE_CREAM = QColor('#FFE5B4')  # 橙奶油
    LEMON_YELLOW = QColor('#FFF44F')  # 柠檬黄 
    PEACH_ORANGE = QColor('#FFCC99')  # 蜜桃橙
    # 红色系（30色）
    WATERMELON = QColor('#FD5B78')  # 西瓜红
    ROSE = QColor('#FF007F')  # 玫瑰红
    PASTEL_RED = QColor('#FF6961')  # 淡红
    SALMON_PINK = QColor('#FF91A4')  # 鲑鱼粉红
    CORAL_PINK = QColor('#F88379')  # 珊瑚粉红
    RASPBERRY = QColor('#E30B5D')  # 树莓红
    STRAWBERRY = QColor('#FC5A8D')  # 草莓红
    CHERRY = QColor('#DE3163')  # 樱桃红
    PINK_RED = QColor('#FF6B6B')  # 粉红
    CRIMSON = QColor('#DC143C')  # 深红
    TOMATO = QColor('#FF6347')  # 番茄红
    SCARLET = QColor('#FF2400')  # 猩红
    CARMINE = QColor('#960018')  # 胭脂红
    RUBY = QColor('#E0115F')  # 红宝石红
    BURGUNDY = QColor('#800020')  # 勃艮第红
    MAHOGANY = QColor('#C04000')  # 桃花心木红
    MAROON = QColor('#800000')  # 栗色
    RED_ORANGE = QColor('#FF5349')  # 红橙
    VERMILION = QColor('#E34234')  # 朱砂红
    ROSEWOOD = QColor('#65000B')  # 红木红
    CARDINAL = QColor('#C41E3A')  # 红衣主教红
    FIREBRICK = QColor('#B22222')  # 火砖红
    RUST = QColor('#B7410E')  # 锈红
    PINK_SHERBET = QColor('#F78FA7')  # 粉雪酪红
    BLUSH = QColor('#DE5D83')  # 腮红
    AMARANTH = QColor('#E52B50')  # 苋红
    CERISE = QColor('#DE3163')  # 樱桃红
    BERRY = QColor('#990F4B')  # 浆果红
    RED_VIOLET = QColor('#C71585')  # 红紫
    FUCHSIA = QColor('#FF00FF')  # 紫红色
    # 中性色系（30色）
    IVORY = QColor('#FFFFF0')  # 象牙白
    EGGSHELL = QColor('#F0EAD6')  # 蛋壳色
    ALMOND = QColor('#EFDECD')  # 杏仁色
    BEIGE = QColor('#F5F5DC')  # 米色
    PARCHMENT = QColor('#F1E9D2')  # 羊皮纸色
    SEASHELL = QColor('#FFF5EE')  # 贝壳白
    LACE = QColor('#FDF5E6')  # 蕾丝白
    COCONUT = QColor('#FBF1D3')  # 椰子白
    FLAX = QColor('#EEDC82')  # 亚麻色
    CHAMPAGNE = QColor('#F7E7CE')  # 香槟色
    CREAM = QColor('#FFFDD0')  # 奶油色
    PEARL = QColor('#EAE0C8')  # 珍珠色
    BONE = QColor('#E3DAC9')  # 骨色
    VANILLA = QColor('#F3E5AB')  # 香草色
    PALE_GOLD = QColor('#E6BE8A')  # 淡金色
    LIGHT_TAUPE = QColor('#B38B6D')  # 浅灰褐色
    MOCHA = QColor('#967969')  # 摩卡色
    SAND = QColor('#F4A460')  # 沙色
    KHAKI = QColor('#F0E68C')  # 卡其色
    TAUPE = QColor('#483C32')  # 灰褐色
    GREY = QColor('#808080')  # 灰色
    CHARCOAL = QColor('#36454F')  # 木炭色
    SLATE = QColor('#708090')  # 板岩色
    SMOKE = QColor('#738276')  # 烟色
    ASH = QColor('#B2BEB5')  # 灰白色
    STONE = QColor('#928E85')  # 石色
    CLAY = QColor('#B66A50')  # 黏土色
    TERRACOTTA = QColor('#E2725B')  # 陶土色
    SANDSTONE = QColor('#C2B280')  # 砂岩色
    PORCELAIN = QColor('#F7F7F7')  # 瓷白色
    # 特殊色系（30色）
    DUSTY_ROSE = QColor('#DCAE96')  # 灰玫瑰色
    MOONSTONE = QColor('#C0C0C0')  # 月光石色
    AURORA_PINK = QColor('#FF9E9E')  # 极光粉
    OPAL = QColor('#A8C3BC')  # 蛋白石色
    PEARL = QColor('#EAE0C8')  # 珍珠色
    PALE_TURQUOISE = QColor('#AFEEEE')  # 浅绿松石
    HONEYDEW = QColor('#F0FFF0')  # 蜜瓜色
    LAVENDER_BLUSH = QColor('#FFF0F5')  # 薰衣草胭脂
    AZURE_MIST = QColor('#F0FFFF')  # 薄雾蓝
    PINK_GLOW = QColor('#FFD3E0')  # 粉光
    MINT_CREAM = QColor('#F5FFFA')  # 薄荷奶油
    ALICE_BLUE = QColor('#F0F8FF')  # 爱丽丝蓝
    GHOST_WHITE = QColor('#F8F8FF')  # 幽灵白
    SNOW = QColor('#FFFAFA')  # 雪白色
    FLORAL_WHITE = QColor('#FFFAF0')  # 花卉白
    CORNFLOWER = QColor('#93CCEA')  # 矢车菊蓝
    BABY_BLUE_EYES = QColor('#A1CAF1')  # 婴儿蓝眼
    POWDER_BLUE = QColor('#B0E0E6')  # 粉末蓝
    AQUA = QColor('#00FFFF')  # 水色
    TURQUOISE = QColor('#40E0D0')  # 绿松石
    AQUAMARINE = QColor('#7FFFD4')  # 海蓝宝石
    MINT = QColor('#3EB489')  # 薄荷绿
    JADE = QColor('#00A86B')  # 翡翠绿
    EMERALD = QColor('#50C878')  # 翠绿
    FOREST_GREEN = QColor('#228B22')  # 森林绿
    OLIVE = QColor('#808000')  # 橄榄绿
    LIME = QColor('#00FF00')  # 柠檬绿
    SPRING_GREEN = QColor('#00FF7F')  # 春绿色
    SEA_GREEN = QColor('#2E8B57')  # 海绿色
    LAWN_GREEN = QColor('#7CFC00')  # 草坪绿
    # 的金属/矿物/食物/季节色
    # 金属光泽色（5色）
    PALE_GOLD = QColor('#E6BE8A')  # 淡金色  
    ROSE_GOLD = QColor('#B76E79')  # 玫瑰金  
    BRONZE = QColor('#CD7F32')  # 青铜色  
    COPPER = QColor('#B87333')  # 铜色  
    PLATINUM = QColor('#E5E4E2')  # 铂金色  
    # 自然矿物色（5色）
    MOONSTONE_BLUE = QColor('#73A9C2')  # 月光石蓝  
    AMETHYST = QColor('#9966CC')  # 紫水晶  
    JASMINE = QColor('#F8DE7E')  # 茉莉黄  
    MALACHITE = QColor('#0BDA51')  # 孔雀石绿  
    LAPIS_LAZULI = QColor('#26619C')  # 青金石蓝  
    # 食物灵感色（10色）
    MACARON_BEIGE = QColor('#F5D6AA')  # 马卡龙米色  
    CARAMEL = QColor('#FFD59A')  # 焦糖色  
    HONEY = QColor('#FEE0B6')  # 蜂蜜色  
    MATCHA = QColor('#A5D46A')  # 抹茶绿  
    MOCHA = QColor('#967969')  # 摩卡棕  
    PISTACHIO = QColor('#93C572')  # 开心果绿  
    BUBBLE_TEA = QColor('#E7C9A9')  # 珍珠奶茶色  
    RED_BEAN = QColor('#843F3F')  # 红豆色  
    TARO = QColor('#B399D4')  # 芋头紫  
    MILK_TEA = QColor('#F3E0BE')  # 奶茶色  
    # 季节限定色（10色）
    SPRING_BUD = QColor('#A7F432')  # 春芽绿  
    SUMMER_SKY = QColor('#38B0DE')  # 夏日晴空  
    AUTUMN_LEAF = QColor('#D07B3C')  # 秋叶橙  
    WINTER_SNOW = QColor('#F0F9FF')  # 冬雪白  
    CHERRY_BLOSSOM = QColor('#FFB7C5')  # 樱粉色  
    HARVEST_MOON = QColor('#F2D2A2')  # 秋月黄  
    MIDSUMMER = QColor('#6EC4E8')  # 仲夏蓝  
    FROST = QColor('#E1F5FE')  # 霜冻蓝  
    MAPLE = QColor('#D1603D')  # 枫叶红  
    FIRST_SNOW = QColor('#F8F8FF')  # 初雪白  
    BUTTER_CREAM = QColor('#F5E6C8')  # 奶油黄油色
    TARO_PURPLE = QColor('#B399D4')  # 芋头紫
    CARAMEL_CREAM = QColor('#E3C9A5')  # 焦糖奶油色
    LEMON_YELLOW = QColor('#FFF44F')  # 柠檬黄
    PEACH_ORANGE = QColor('#FFCC99')  # 蜜桃橙
    LILAC_MIST = QColor('#D5C7E8')  # 淡丁香紫
    APPLE_GREEN = QColor('#8DB600')  # 苹果绿
    ROSE_PINK = QColor('#FF66CC')  # 玫瑰粉
    # 其他补充的常用马卡龙色
    POWDER_BLUE = QColor('#B0E0E6')  # 粉末蓝
    LAVENDER_BLUSH = QColor('#FFF0F5')  # 薰衣草胭脂
    MINT_CREAM = QColor('#F5FFFA')  # 薄荷奶油
    HONEYDEW = QColor('#F0FFF0')  # 蜜瓜色
    ALICE_BLUE = QColor('#F0F8FF')  # 爱丽丝蓝
    BABY_BLUE_EYES = QColor('#A1CAF1')  # 婴儿蓝眼
    CORNFLOWER = QColor('#93CCEA')  # 矢车菊蓝



class UserManager:
    """用户管理类"""
    USERS_DB = 'users.db'
    CONFIG_FILE = 'user_config.ini'
    
    @classmethod
    def init_users_db(cls):
        """初始化用户数据库"""
        try:
            conn = sqlite3.connect(cls.USERS_DB)
            cursor = conn.cursor()
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS users (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    username TEXT NOT NULL UNIQUE,
                    password TEXT DEFAULT '',
                    db_file TEXT NOT NULL UNIQUE,
                    last_login TEXT,
                    has_password BOOLEAN DEFAULT FALSE
                )
            ''')
            conn.commit()
            conn.close()
        except Error as e:
            print(f"[DEBUG] 无法初始化用户数据库: {str(e)}")
            raise Exception(f"无法初始化用户数据库: {str(e)}")

    @classmethod
    def create_user(cls, username, password=''):
        """创建新用户"""
        try:
            db_file = f"user_{username}.db"
            conn = sqlite3.connect(db_file)
            conn.close()
            
            conn = sqlite3.connect(cls.USERS_DB)
            cursor = conn.cursor()
            has_password = bool(password)  # 判断是否有密码
            cursor.execute(
                "INSERT INTO users (username, password, db_file, has_password) VALUES (?, ?, ?, ?)",
                (username, password, db_file, has_password)
            )
            conn.commit()
            return True
        except Error as e:
            raise Exception(f"无法创建用户: {str(e)}")
        finally:
            if 'conn' in locals():
                conn.close()

    @classmethod
    def authenticate(cls, username, password=''):
        """验证用户登录"""
        try:
            conn = sqlite3.connect(cls.USERS_DB)
            cursor = conn.cursor()
            cursor.execute(
                "SELECT db_file, has_password, password FROM users WHERE username=?",
                (username,)
            )
            result = cursor.fetchone()
            
            if not result:
                return None
                
            db_file, has_password, stored_password = result
            
            # 如果有密码但未提供密码，或密码不匹配
            if has_password and (not password or stored_password != password):
                return None
                
            # 更新最后登录时间
            cursor.execute(
                "UPDATE users SET last_login=? WHERE username=?",
                (datetime.now().strftime("%Y-%m-%d %H:%M:%S"), username)
            )
            conn.commit()
            return db_file  # 返回数据库文件路径
            
        except Error as e:
            raise Exception(f"认证失败: {str(e)}")
        finally:
            if 'conn' in locals():
                conn.close()

    @classmethod
    def delete_user(cls, username):
        """删除用户及其数据库文件"""
        try:
            # 先获取用户的数据库文件路径
            conn = sqlite3.connect(cls.USERS_DB)
            cursor = conn.cursor()
            cursor.execute("SELECT db_file FROM users WHERE username=?", (username,))
            result = cursor.fetchone()
            
            if not result:
                return False
                
            db_file = result[0]
            
            # 从用户表中删除记录
            cursor.execute("DELETE FROM users WHERE username=?", (username,))
            conn.commit()
            
            # 删除用户数据库文件
            if os.path.exists(db_file):
                os.remove(db_file)
                
            return True
        except Error as e:
            raise Exception(f"无法删除用户: {str(e)}")
        finally:
            if 'conn' in locals():
                conn.close()

    @classmethod
    def save_login_config(cls, username, password='', remember=False):
        """保存登录配置"""
        import configparser
        config = configparser.ConfigParser()
        # 总是保存用户名
        config['LOGIN'] = {
            'username': username,
            'password': password if remember else '',
            'remember': 'True' if remember else 'False'
        }
        
        with open(cls.CONFIG_FILE, 'w') as configfile:
            config.write(configfile)
    
    @classmethod
    def load_login_config(cls):
        """读取登录配置"""
        import configparser
        import os
        config = configparser.ConfigParser()
        if not os.path.exists(cls.CONFIG_FILE):
            return None, None, False
            
        config.read(cls.CONFIG_FILE)
        if 'LOGIN' in config:
            return (
                config['LOGIN'].get('username', ''),
                config['LOGIN'].get('password', ''),
                config['LOGIN'].getboolean('remember', False)
            )
        return None, None, False

    @classmethod
    def update_username(cls, old_username, new_username, password=''):
        """修改用户名"""
        try:
            # 验证旧用户
            conn = sqlite3.connect(cls.USERS_DB)
            cursor = conn.cursor()
            
            # 检查新用户名是否已存在
            cursor.execute("SELECT id FROM users WHERE username=?", (new_username,))
            if cursor.fetchone():
                raise Exception("新用户名已存在")
                
            # 验证旧用户密码(如果有密码)
            cursor.execute(
                "SELECT password, has_password FROM users WHERE username=?",
                (old_username,)
            )
            result = cursor.fetchone()
            
            if not result:
                raise Exception("原用户名不存在")
                
            stored_password, has_password = result
            
            if has_password and (not password or stored_password != password):
                raise Exception("密码验证失败")
            
            # 获取用户数据库文件
            cursor.execute("SELECT db_file FROM users WHERE username=?", (old_username,))
            db_file = cursor.fetchone()[0]
            
            # 更新用户名
            cursor.execute(
                "UPDATE users SET username=? WHERE username=?",
                (new_username, old_username)
            )
            conn.commit()
            
            # 如果数据库文件名包含用户名，则重命名数据库文件
            if f"user_{old_username}.db" in db_file:
                new_db_file = f"user_{new_username}.db"
                if os.path.exists(db_file):
                    os.rename(db_file, new_db_file)
                
                # 更新数据库文件路径
                cursor.execute(
                    "UPDATE users SET db_file=? WHERE username=?",
                    (new_db_file, new_username)
                )
                conn.commit()
                
            return True
        except Error as e:
            raise Exception(f"无法修改用户名: {str(e)}")
        finally:
            if 'conn' in locals():
                conn.close()

    @classmethod
    def get_backup_dir(cls):
        """获取备份目录路径"""
        backup_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "backups")
        if not os.path.exists(backup_dir):
            os.makedirs(backup_dir)
        return backup_dir
    
    @classmethod
    def backup_db(cls, db_file, backup_type="manual"):
        """备份数据库文件"""
        try:
            backup_dir = cls.get_backup_dir()
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            backup_file = os.path.join(
                backup_dir, 
                f"{os.path.basename(db_file)}_{backup_type}_{timestamp}.bak"  # 确保使用正确的备份类型
            )
            
            # 复制数据库文件
            shutil.copy2(db_file, backup_file)
            
            # 如果是自动备份，清理超过30天的旧备份
            if backup_type == "auto":
                cls.clean_old_backups(db_file, days=30)
                
            return backup_file
        except Exception as e:
            raise Exception(f"备份失败: {str(e)}")
    
    @classmethod
    def clean_old_backups(cls, db_file, days=30):
        """清理超过指定天数的旧备份"""
        try:
            backup_dir = cls.get_backup_dir()
            cutoff_time = datetime.now() - timedelta(days=days)
            
            for filename in os.listdir(backup_dir):
                if filename.startswith(os.path.basename(db_file)) and filename.endswith(".bak"):
                    filepath = os.path.join(backup_dir, filename)
                    mtime = datetime.fromtimestamp(os.path.getmtime(filepath))
                    
                    if mtime < cutoff_time:
                        os.remove(filepath)
        except Exception as e:
            print(f"[WARNING] 清理旧备份失败: {str(e)}")
    
    @classmethod
    def get_backups(cls, db_file):
        """获取指定数据库的所有备份文件"""
        try:
            backup_dir = cls.get_backup_dir()
            backups = []
            db_basename = os.path.basename(db_file)
            
            for filename in os.listdir(backup_dir):
                if filename.startswith(db_basename) and filename.endswith(".bak"):
                    filepath = os.path.join(backup_dir, filename)
                    mtime = datetime.fromtimestamp(os.path.getmtime(filepath))
                    size = os.path.getsize(filepath)
                    
                    # 解析备份类型 - 修改后的逻辑
                    parts = filename[len(db_basename)+1:-4].split("_")  # 去掉.db_和.bak
                    if len(parts) >= 2:
                        backup_type = parts[0]  # 第一个部分是备份类型
                    else:
                        backup_type = "unknown"
                    
                    backups.append({
                        "path": filepath,
                        "name": filename,
                        "date": mtime,
                        "size": size,
                        "type": backup_type
                    })
            
            # 按日期降序排序
            backups.sort(key=lambda x: x["date"], reverse=True)
            return backups
        except Exception as e:
            raise Exception(f"获取备份列表失败: {str(e)}")
    
    @classmethod
    def restore_db(cls, db_file, backup_file):
        """从备份恢复数据库"""
        try:
            # 1. 首先创建当前数据库的备份(用于回滚)
            rollback_file = cls.backup_db(db_file, "rollback")
            
            # 2. 尝试恢复
            shutil.copy2(backup_file, db_file)
            
            return rollback_file
        except Exception as e:
            raise Exception(f"恢复失败: {str(e)}")

class BatchAddDialog(QDialog):
    """批量添加排班对话框"""
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("批量添加排班")
        self.setWindowIcon(QIcon('icon.ico'))
        self.resize(800, 600)
        
        # 表单布局
        layout = QVBoxLayout()
        self.setLayout(layout)
        
        # 选择员工区域
        employee_group = QGroupBox("选择员工")
        employee_layout = QVBoxLayout()
        
        # 员工表格
        self.employee_table = QTableWidget()
        self.employee_table.setColumnCount(3)
        self.employee_table.setHorizontalHeaderLabels(["选择", "员工姓名", "部门"])
        self.employee_table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.employee_table.setSelectionBehavior(QTableView.SelectRows)
        self.load_employees()
        
        employee_layout.addWidget(self.employee_table)
        employee_group.setLayout(employee_layout)
        layout.addWidget(employee_group)
        
        # 选择日期区域
        date_group = QGroupBox("选择日期")
        date_layout = QVBoxLayout()
        
        # 日期选择模式
        self.date_mode = QComboBox()
        self.date_mode.addItems(["连续日期", "不连续日期"])
        date_layout.addWidget(QLabel("日期选择模式:"))
        date_layout.addWidget(self.date_mode)
        
        # 连续日期选项
        self.continuous_date_widget = QWidget()
        continuous_layout = QHBoxLayout()
        continuous_layout.addWidget(QLabel("从:"))
        self.start_date = QDateEdit(QDate.currentDate())
        self.start_date.setCalendarPopup(True)
        self.start_date.dateChanged.connect(self.update_end_date_by_days)
        continuous_layout.addWidget(self.start_date)
        
        continuous_layout.addWidget(QLabel("到:"))
        self.end_date = QDateEdit(QDate.currentDate())
        self.end_date.setCalendarPopup(True)
        continuous_layout.addWidget(self.end_date)
        
        continuous_layout.addWidget(QLabel("天数:"))
        self.day_count = QSpinBox()
        self.day_count.setRange(1, 365)
        self.day_count.setValue(1)
        self.day_count.valueChanged.connect(self.update_end_date_by_days)
        continuous_layout.addWidget(self.day_count)
        
        continuous_layout.addWidget(QLabel("工作日:"))
        self.weekdays = QComboBox()
        self.weekdays.addItems(["全部", "仅工作日", "仅周末", "自定义..."])
        self.weekdays.currentIndexChanged.connect(self.toggle_custom_weekdays)
        continuous_layout.addWidget(self.weekdays)
        
        # 自定义工作日选择控件
        self.custom_weekdays_widget = QWidget()
        custom_weekdays_layout = QHBoxLayout()
        self.custom_weekdays_widget.setLayout(custom_weekdays_layout)
        
        self.weekday_checks = []
        weekday_names = ["周一", "周二", "周三", "周四", "周五", "周六", "周日"]
        for i, day in enumerate(weekday_names):
            check = QCheckBox(day)
            check.setChecked(i < 5)  # 默认勾选工作日
            self.weekday_checks.append(check)
            custom_weekdays_layout.addWidget(check)
        
        continuous_layout.addWidget(self.custom_weekdays_widget)
        self.custom_weekdays_widget.hide()
        
        self.continuous_date_widget.setLayout(continuous_layout)
        date_layout.addWidget(self.continuous_date_widget)
        
        # 不连续日期选项
        self.discontinuous_date_widget = QWidget()
        discontinuous_layout = QVBoxLayout()
        
        self.date_list = QListWidget()
        self.date_list.setSelectionMode(QListWidget.MultiSelection)
        
        btn_layout = QHBoxLayout()
        self.add_date_btn = QPushButton("添加日期")
        self.add_date_btn.clicked.connect(self.add_custom_date)
        btn_layout.addWidget(self.add_date_btn)
        
        self.remove_date_btn = QPushButton("移除选中日期")
        self.remove_date_btn.clicked.connect(lambda: self.remove_items(self.date_list))
        btn_layout.addWidget(self.remove_date_btn)
        
        discontinuous_layout.addWidget(self.date_list)
        discontinuous_layout.addLayout(btn_layout)
        self.discontinuous_date_widget.setLayout(discontinuous_layout)
        date_layout.addWidget(self.discontinuous_date_widget)
        
        # 默认显示连续日期
        self.discontinuous_date_widget.hide()
        self.date_mode.currentIndexChanged.connect(self.toggle_date_mode)
        
        date_group.setLayout(date_layout)
        layout.addWidget(date_group)
        
        # 班次和备注
        form_layout = QFormLayout()
        
        # 班次类型
        self.shift_type = QComboBox()
        self.shift_type.setEditable(True)
        try:
            parent.cursor.execute("SELECT shift_name || ' (' || start_time || '-' || end_time || ')' FROM custom_shifts ORDER BY shift_name")
            shifts = parent.cursor.fetchall()
            self.shift_type.addItems([shift[0] for shift in shifts])
        except Error as e:
            QMessageBox.critical(self, "数据库错误", f"无法加载班次列表:\n{str(e)}")
        form_layout.addRow("班次类型:", self.shift_type)
        
        # 自定义班次按钮
        self.custom_shift_btn = QPushButton("自定义时间段")
        self.custom_shift_btn.clicked.connect(self.show_custom_shift_dialog)
        form_layout.addRow("", self.custom_shift_btn)
        
        # 职位
        self.position = QLineEdit()
        form_layout.addRow("职位:", self.position)
        
        # 备注
        self.remarks = QLineEdit()
        form_layout.addRow("备注:", self.remarks)
        
        layout.addLayout(form_layout)
        
        # 按钮
        button_box = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel)
        button_box.accepted.connect(self.accept)
        button_box.rejected.connect(self.reject)
        layout.addWidget(button_box)


        # 设置按钮样式
        button_box.button(QDialogButtonBox.Ok).setStyleSheet(
            f"background-color: {MacaronColors.MINT_GREEN.name()}; color: black;")
        button_box.button(QDialogButtonBox.Cancel).setStyleSheet(
            f"background-color: {MacaronColors.ROSE_PINK.name()}; color: black;")
        self.custom_shift_btn.setStyleSheet(
            f"background-color: {MacaronColors.SKY_BLUE.name()}; color: black;")
        self.add_date_btn.setStyleSheet(
            f"background-color: {MacaronColors.SKY_BLUE.name()}; color: black;")
        self.remove_date_btn.setStyleSheet(
            f"background-color: {MacaronColors.ROSE_PINK.name()}; color: black;")
    
    def update_end_date_by_days(self):
        """根据选择的天数更新结束日期"""
        days = self.day_count.value()
        start_date = self.start_date.date()
        end_date = start_date.addDays(days - 1)  # 减1因为包含开始当天
        self.end_date.setDate(end_date)
    
    def toggle_custom_weekdays(self, index):
        """显示/隐藏自定义工作日选择控件"""
        if index == 3:  # 选择"自定义..."时
            self.custom_weekdays_widget.show()
        else:
            self.custom_weekdays_widget.hide()
    
    def toggle_date_mode(self, index):
        """切换日期选择模式"""
        if index == 0:  # 连续日期
            self.continuous_date_widget.show()
            self.discontinuous_date_widget.hide()
        else:  # 不连续日期
            self.continuous_date_widget.hide()
            self.discontinuous_date_widget.show()
    
    def load_employees(self):
        """加载员工列表"""
        try:
            self.parent().cursor.execute("SELECT DISTINCT employee_name, department FROM schedules ORDER BY department, employee_name")
            employees = self.parent().cursor.fetchall()
            
            self.employee_table.setRowCount(len(employees))
            for row, (name, dept) in enumerate(employees):
                # 选择框
                checkbox = QCheckBox()
                checkbox_widget = QWidget()
                checkbox_layout = QHBoxLayout(checkbox_widget)
                checkbox_layout.addWidget(checkbox)
                checkbox_layout.setAlignment(Qt.AlignCenter)
                checkbox_layout.setContentsMargins(0, 0, 0, 0)
                self.employee_table.setCellWidget(row, 0, checkbox_widget)
                
                # 员工姓名
                self.employee_table.setItem(row, 1, QTableWidgetItem(name))
                
                # 部门
                self.employee_table.setItem(row, 2, QTableWidgetItem(dept))
            
            # 调整列宽
            self.employee_table.setColumnWidth(0, 50)
        except Error as e:
            QMessageBox.critical(self, "数据库错误", f"无法加载员工列表:\n{str(e)}")
    
    def add_custom_date(self):
        """添加自定义日期"""
        dialog = QDialog(self)
        dialog.setWindowTitle("添加日期")
        dialog.resize(300, 150)
        
        layout = QVBoxLayout()
        dialog.setLayout(layout)
        
        date_edit = QDateEdit(QDate.currentDate())
        date_edit.setCalendarPopup(True)
        layout.addWidget(date_edit)
        
        button_box = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel)
        button_box.accepted.connect(dialog.accept)
        button_box.rejected.connect(dialog.reject)
        layout.addWidget(button_box)
        
        if dialog.exec_() == QDialog.Accepted:
            date = date_edit.date().toString("yyyy-MM-dd")
            if not self.date_list.findItems(date, Qt.MatchExactly):
                self.date_list.addItem(date)
    
    def remove_items(self, list_widget):
        """移除选中项"""
        for item in list_widget.selectedItems():
            list_widget.takeItem(list_widget.row(item))
    
    def show_custom_shift_dialog(self):
        """显示自定义时间段对话框"""
        dialog = QDialog(self)
        dialog.setWindowTitle("自定义班次时间段")
        dialog.resize(400, 500)  # 增加对话框高度
        
        layout = QVBoxLayout(dialog)
        
        # 班次列表区域
        shift_list_group = QGroupBox("现有班次")
        shift_list_layout = QVBoxLayout()
        
        self.shift_list = QListWidget()
        self.load_shift_list()  # 加载现有班次
        shift_list_layout.addWidget(self.shift_list)
        
        # 操作按钮
        btn_layout = QHBoxLayout()
        self.edit_shift_btn = QPushButton("编辑")
        self.edit_shift_btn.clicked.connect(self.edit_selected_shift)
        btn_layout.addWidget(self.edit_shift_btn)
        
        self.delete_shift_btn = QPushButton("删除")
        self.delete_shift_btn.clicked.connect(self.delete_selected_shift)
        btn_layout.addWidget(self.delete_shift_btn)
        
        shift_list_layout.addLayout(btn_layout)
        shift_list_group.setLayout(shift_list_layout)
        layout.addWidget(shift_list_group)
        
        # 添加/编辑班次区域
        edit_group = QGroupBox("添加/编辑班次")
        edit_layout = QFormLayout()
        
        # 班次名称
        self.shift_name = QLineEdit()
        self.shift_name.setPlaceholderText("例如: 弹性班")
        edit_layout.addRow("班次名称:", self.shift_name)
        
        # 开始时间
        self.start_time = QTimeEdit()
        self.start_time.setDisplayFormat("HH:mm")
        self.start_time.setTime(QTime(8, 0))
        edit_layout.addRow("开始时间:", self.start_time)
        
        # 结束时间
        self.end_time = QTimeEdit()
        self.end_time.setDisplayFormat("HH:mm")
        self.end_time.setTime(QTime(17, 0))
        edit_layout.addRow("结束时间:", self.end_time)
        
        # 添加说明标签
        info_label = QLabel("提示: 可以留空时间创建模糊班次")
        info_label.setStyleSheet("color: gray;")
        edit_layout.addRow(info_label)
        
        # 添加/更新按钮
        self.add_update_btn = QPushButton("添加")
        self.add_update_btn.clicked.connect(lambda: self.add_or_update_shift(dialog))
        edit_layout.addRow(self.add_update_btn)
        
        edit_group.setLayout(edit_layout)
        layout.addWidget(edit_group)
        
        # 关闭按钮
        close_btn = QPushButton("关闭")
        close_btn.clicked.connect(dialog.reject)
        layout.addWidget(close_btn)
        
        # 设置按钮样式
        self.edit_shift_btn.setStyleSheet(f"background-color: {MacaronColors.SKY_BLUE.name()}; color: black;")
        self.delete_shift_btn.setStyleSheet(f"background-color: {MacaronColors.ROSE_PINK.name()}; color: black;")
        self.add_update_btn.setStyleSheet(f"background-color: {MacaronColors.MINT_GREEN.name()}; color: black;")
        close_btn.setStyleSheet(f"background-color: {MacaronColors.LAVENDER.name()}; color: black;")
        
        dialog.exec_()

    def load_shift_list(self):
        """加载班次列表"""
        self.shift_list.clear()
        try:
            self.parent().cursor.execute("SELECT shift_name, start_time, end_time FROM custom_shifts ORDER BY shift_name")
            shifts = self.parent().cursor.fetchall()
            
            for shift in shifts:
                name, start, end = shift
                if start and end:
                    item_text = f"{name} ({start}-{end})"
                else:
                    item_text = name
                item = QListWidgetItem(item_text)
                item.setData(Qt.UserRole, shift)  # 存储原始数据
                self.shift_list.addItem(item)
        except Error as e:
            QMessageBox.critical(self, "数据库错误", f"无法加载班次列表:\n{str(e)}")

    def edit_selected_shift(self):
        """编辑选中的班次"""
        selected = self.shift_list.currentItem()
        if not selected:
            QMessageBox.warning(self, "警告", "请先选择一个班次")
            return
            
        shift_data = selected.data(Qt.UserRole)
        name, start_str, end_str = shift_data
        
        # 填充编辑表单
        self.shift_name.setText(name)
        
        if start_str:
            start_time = QTime.fromString(start_str, "HH:mm")
            self.start_time.setTime(start_time)
        else:
            self.start_time.setTime(QTime())
        
        if end_str:
            end_time = QTime.fromString(end_str, "HH:mm")
            self.end_time.setTime(end_time)
        else:
            self.end_time.setTime(QTime())
        
        # 更改按钮文本为"更新"
        self.add_update_btn.setText("更新")
        self.current_edit_name = name  # 存储当前编辑的班次名

    def delete_selected_shift(self):
        """删除选中的班次"""
        selected = self.shift_list.currentItem()
        if not selected:
            QMessageBox.warning(self, "警告", "请先选择一个班次")
            return
        
        name = selected.data(Qt.UserRole)[0]
        
        reply = QMessageBox.question(
            self, "确认删除",
            f"确定要删除班次 '{name}' 吗？",
            QMessageBox.Yes | QMessageBox.No, QMessageBox.No
        )
        
        if reply == QMessageBox.Yes:
            try:
                # 检查是否有排班使用此班次
                self.parent().cursor.execute("SELECT COUNT(*) FROM schedules WHERE shift_type = ?", (name,))
                count = self.parent().cursor.fetchone()[0]
                
                if count > 0:
                    QMessageBox.warning(self, "警告", f"无法删除，因为有 {count} 条排班记录使用此班次")
                    return
                    
                self.parent().cursor.execute("DELETE FROM custom_shifts WHERE shift_name = ?", (name,))
                self.parent().conn.commit()
                self.load_shift_list()
                self.parent().update_shifts_in_ui()  # 更新主界面中的班次下拉框
            except Error as e:
                QMessageBox.critical(self, "数据库错误", f"无法删除班次:\n{str(e)}")

    def add_or_update_shift(self, dialog):
        """添加或更新班次"""
        name = self.shift_name.text().strip()
        if not name:
            QMessageBox.warning(self, "警告", "请输入班次名称")
            return
        
        # 处理时间输入
        start_time = self.start_time.time().toString("HH:mm") if self.start_time.time().isValid() else ""
        end_time = self.end_time.time().toString("HH:mm") if self.end_time.time().isValid() else ""
        
        try:
            if hasattr(self, 'current_edit_name') and self.current_edit_name:
                # 更新现有班次
                self.parent().cursor.execute(
                    "UPDATE custom_shifts SET shift_name=?, start_time=?, end_time=? WHERE shift_name=?",
                    (name, start_time, end_time, self.current_edit_name)
                )
                delattr(self, 'current_edit_name')
                self.add_update_btn.setText("添加")
            else:
                # 添加新班次
                self.parent().cursor.execute(
                    "INSERT OR REPLACE INTO custom_shifts (shift_name, start_time, end_time) VALUES (?, ?, ?)",
                    (name, start_time, end_time)
                )
            
            self.parent().conn.commit()
            self.load_shift_list()
            self.parent().update_shifts_in_ui()  # 更新主界面中的班次下拉框
            
            # 重置表单
            self.shift_name.clear()
            self.start_time.setTime(QTime(8, 0))
            self.end_time.setTime(QTime(17, 0))
            
        except Error as e:
            QMessageBox.critical(self, "数据库错误", f"无法保存班次:\n{str(e)}")




    
    def get_schedule_data(self):
        """获取排班数据"""
        data = []
        
        # 获取选中的员工
        selected_employees = []
        for row in range(self.employee_table.rowCount()):
            checkbox = self.employee_table.cellWidget(row, 0).findChild(QCheckBox)
            if checkbox and checkbox.isChecked():
                name = self.employee_table.item(row, 1).text()
                dept = self.employee_table.item(row, 2).text()
                selected_employees.append((name, dept))
        
        if not selected_employees:
            QMessageBox.warning(self, "警告", "请至少选择一个员工")
            return data
        
        # 获取日期
        dates = []
        if self.date_mode.currentIndex() == 0:  # 连续日期
            start = self.start_date.date()
            end = self.end_date.date()
            if start > end:
                QMessageBox.warning(self, "警告", "结束日期不能早于开始日期")
                return data
                
            current = start
            weekday_mode = self.weekdays.currentIndex()
            
            while current <= end:
                weekday = current.dayOfWeek()
                
                # 处理不同的工作日模式
                if weekday_mode == 1 and weekday >= 6:  # 仅工作日
                    current = current.addDays(1)
                    continue
                if weekday_mode == 2 and weekday < 6:  # 仅周末
                    current = current.addDays(1)
                    continue
                if weekday_mode == 3:  # 自定义工作日
                    # Qt的周日是7，周一至周六是1-6
                    # 我们调整为0-6对应周一到周日
                    adjusted_weekday = (weekday - 1) % 7
                    if not self.weekday_checks[adjusted_weekday].isChecked():
                        current = current.addDays(1)
                        continue
                        
                dates.append(current.toString("yyyy-MM-dd"))
                current = current.addDays(1)
        else:  # 不连续日期
            for i in range(self.date_list.count()):
                dates.append(self.date_list.item(i).text())
        
        if not dates:
            QMessageBox.warning(self, "警告", "请至少选择一个日期")
            return data
        
        # 获取其他信息
        shift = self.shift_type.currentText()
        position = self.position.text().strip()
        remarks = self.remarks.text().strip()
        
        # 生成排班数据
        for name, dept in selected_employees:
            for date in dates:
                data.append((name, dept, position, date, shift, remarks))
        
        return data



class ScheduleDialog(QDialog):
    """排班记录编辑对话框"""
    last_department = ""  # 类变量存储最后选择的部门
    last_shift_type = ""  # 类变量存储最后选择的班次类型
    
    def __init__(self, parent=None, is_edit_mode=False):
        super().__init__(parent)
        self.is_edit_mode = is_edit_mode
        self.setWindowTitle("排班记录")
        self.setWindowIcon(QIcon('icon.ico'))
        self.resize(400, 350)
        
        # 表单布局
        layout = QFormLayout()
        self.setLayout(layout)
        
        # 员工姓名
        self.employee_name = QLineEdit()
        layout.addRow("员工姓名:", self.employee_name)
        
        # 部门
        self.department = QComboBox()
        self.department.setEditable(True)
        
        try:
            parent.cursor.execute("SELECT name FROM departments ORDER BY name")
            depts = parent.cursor.fetchall()
            self.department.addItems([dept[0] for dept in depts])
            
            # 如果不是编辑模式，使用最后选择的部门
            if not self.is_edit_mode and ScheduleDialog.last_department:
                dept_index = self.department.findText(ScheduleDialog.last_department)
                if dept_index >= 0:
                    self.department.setCurrentIndex(dept_index)
                else:
                    self.department.setCurrentText(ScheduleDialog.last_department)
        except Error as e:
            QMessageBox.critical(self, "数据库错误", f"无法加载部门列表:\n{str(e)}")
        
        layout.addRow("部门:", self.department)
        
        # 自定义部门按钮
        self.custom_dept_btn = QPushButton("自定义部门")
        self.custom_dept_btn.clicked.connect(self.show_custom_dept_dialog)
        layout.addRow("", self.custom_dept_btn)
        
        # 职位
        self.position = QLineEdit()
        layout.addRow("职位:", self.position)
        
        # 工作日期
        self.work_date = QDateEdit(QDate.currentDate())
        self.work_date.setCalendarPopup(True)
        layout.addRow("工作日期:", self.work_date)
        
        # 班次类型
        self.shift_type = QComboBox()
        self.shift_type.setEditable(True)
        
        try:
            parent.cursor.execute("SELECT shift_name || ' (' || start_time || '-' || end_time || ')' FROM custom_shifts ORDER BY shift_name")
            shifts = parent.cursor.fetchall()
            self.shift_type.addItems([shift[0] for shift in shifts])
        
            # 设置最后选择的班次类型
            if ScheduleDialog.last_shift_type:
                shift_index = self.shift_type.findText(ScheduleDialog.last_shift_type)
                if shift_index >= 0:
                    self.shift_type.setCurrentIndex(shift_index)
                else:
                    self.shift_type.setCurrentText(ScheduleDialog.last_shift_type)
            else:
                # 如果没有最后选择的班次，设置默认选中"全天班"
                full_day_index = -1
                for i in range(self.shift_type.count()):
                    if "全天班" in self.shift_type.itemText(i):
                        full_day_index = i
                        break
                
                if full_day_index != -1:
                    self.shift_type.setCurrentIndex(full_day_index)
            
        except Error as e:
            QMessageBox.critical(self, "数据库错误", f"无法加载班次列表:\n{str(e)}")
        
        layout.addRow("班次类型:", self.shift_type)
        
        # 自定义班次按钮
        self.custom_shift_btn = QPushButton("自定义时间段")
        self.custom_shift_btn.clicked.connect(self.show_custom_shift_dialog)
        layout.addRow("", self.custom_shift_btn)
        
        # 备注
        self.remarks = QLineEdit()
        layout.addRow("备注:", self.remarks)
        
        # 按钮
        button_layout = QHBoxLayout()
        layout.addRow(button_layout)
        
        self.ok_btn = QPushButton("确定")
        self.ok_btn.clicked.connect(self.accept)
        button_layout.addWidget(self.ok_btn)
        
        self.cancel_btn = QPushButton("取消")
        self.cancel_btn.clicked.connect(self.reject)
        button_layout.addWidget(self.cancel_btn)

        self.employee_name.installEventFilter(self)
        self.department.lineEdit().installEventFilter(self)
        self.position.installEventFilter(self)
        self.work_date.installEventFilter(self)
        self.shift_type.lineEdit().installEventFilter(self)
        self.remarks.installEventFilter(self)

        # 设置按钮样式
        self.ok_btn.setStyleSheet(
            f"background-color: {MacaronColors.MINT_GREEN.name()}; color: black;")  # 薄荷绿
        self.cancel_btn.setStyleSheet(
            f"background-color: {MacaronColors.ROSE_PINK.name()}; color: black;")  # 玫瑰粉
        self.custom_dept_btn.setStyleSheet(
            f"background-color: {MacaronColors.SKY_BLUE.name()}; color: black;")  # 天空蓝
        self.custom_shift_btn.setStyleSheet(
            f"background-color: {MacaronColors.SKY_BLUE.name()}; color: black;")  # 天空蓝

    def eventFilter(self, obj, event):
        """处理回车键事件"""
        if event.type() == event.KeyPress and event.key() == Qt.Key_Return:
            # 检查当前焦点是否在某个输入控件上
            if obj in [self.employee_name, self.department.lineEdit(), self.position, 
                    self.work_date, self.shift_type.lineEdit(), self.remarks]:
                self.accept()  # 按回车键相当于点击确定
                return True
        return super().eventFilter(obj, event)




    def show_custom_dept_dialog(self):
        """显示自定义部门对话框"""
        dialog = QDialog(self)
        dialog.setWindowTitle("自定义部门")
        dialog.resize(300, 150)
        
        layout = QFormLayout(dialog)
        
        self.new_dept = QLineEdit()
        self.new_dept.setPlaceholderText("输入新部门名称")
        layout.addRow("部门名称:", self.new_dept)
        
        button_box = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel)
        button_box.accepted.connect(dialog.accept)
        button_box.rejected.connect(dialog.reject)
        layout.addRow(button_box)
        
        if dialog.exec_() == QDialog.Accepted and self.new_dept.text().strip():
            new_dept = self.new_dept.text().strip()
            try:
                self.parent().cursor.execute("INSERT OR IGNORE INTO departments (name) VALUES (?)", (new_dept,))
                self.parent().conn.commit()
                self.department.addItem(new_dept)
                self.department.setCurrentText(new_dept)
            except Error as e:
                QMessageBox.critical(self, "数据库错误", f"无法添加部门:\n{str(e)}")

    def show_custom_shift_dialog(self):
        """显示自定义时间段对话框"""
        dialog = QDialog(self)
        dialog.setWindowTitle("自定义班次时间段")
        dialog.resize(400, 500)  # 增加对话框高度
        
        layout = QVBoxLayout(dialog)
        
        # 班次列表
        shift_list_group = QGroupBox("现有班次")
        shift_list_layout = QVBoxLayout()
        
        self.shift_list = QListWidget()
        self.load_shift_list()  # 加载现有班次
        shift_list_layout.addWidget(self.shift_list)
        
        # 操作按钮
        btn_layout = QHBoxLayout()
        self.edit_shift_btn = QPushButton("编辑")
        self.edit_shift_btn.clicked.connect(self.edit_selected_shift)
        btn_layout.addWidget(self.edit_shift_btn)
        
        self.delete_shift_btn = QPushButton("删除")
        self.delete_shift_btn.clicked.connect(self.delete_selected_shift)
        btn_layout.addWidget(self.delete_shift_btn)
        
        shift_list_layout.addLayout(btn_layout)
        shift_list_group.setLayout(shift_list_layout)
        layout.addWidget(shift_list_group)
        
        # 添加/编辑班次区域
        edit_group = QGroupBox("添加/编辑班次")
        edit_layout = QFormLayout()
        
        # 班次名称
        self.shift_name = QLineEdit()
        self.shift_name.setPlaceholderText("例如: 弹性班")
        edit_layout.addRow("班次名称:", self.shift_name)
        
        # 开始时间
        self.start_time = QTimeEdit()
        self.start_time.setDisplayFormat("HH:mm")
        self.start_time.setTime(QTime(8, 0))
        edit_layout.addRow("开始时间:", self.start_time)
        
        # 结束时间
        self.end_time = QTimeEdit()
        self.end_time.setDisplayFormat("HH:mm")
        self.end_time.setTime(QTime(17, 0))
        edit_layout.addRow("结束时间:", self.end_time)
        
        # 添加说明标签
        info_label = QLabel("提示: 可以留空时间创建模糊班次")
        info_label.setStyleSheet("color: gray;")
        edit_layout.addRow(info_label)
        
        # 添加/更新按钮
        self.add_update_btn = QPushButton("添加")
        self.add_update_btn.clicked.connect(lambda: self.add_or_update_shift(dialog))
        edit_layout.addRow(self.add_update_btn)
        
        edit_group.setLayout(edit_layout)
        layout.addWidget(edit_group)
        
        # 关闭按钮
        close_btn = QPushButton("关闭")
        close_btn.clicked.connect(dialog.reject)
        layout.addWidget(close_btn)
        
        # 设置按钮样式
        self.edit_shift_btn.setStyleSheet(f"background-color: {MacaronColors.SKY_BLUE.name()}; color: black;")
        self.delete_shift_btn.setStyleSheet(f"background-color: {MacaronColors.ROSE_PINK.name()}; color: black;")
        self.add_update_btn.setStyleSheet(f"background-color: {MacaronColors.MINT_GREEN.name()}; color: black;")
        close_btn.setStyleSheet(f"background-color: {MacaronColors.LAVENDER.name()}; color: black;")

        
        dialog.exec_()

    def load_shift_list(self):
        """加载班次列表"""
        self.shift_list.clear()
        try:
            self.parent().cursor.execute("SELECT shift_name, start_time, end_time FROM custom_shifts ORDER BY shift_name")
            shifts = self.parent().cursor.fetchall()
            
            for shift in shifts:
                name, start, end = shift
                if start and end:
                    item_text = f"{name} ({start}-{end})"
                else:
                    item_text = name
                item = QListWidgetItem(item_text)
                item.setData(Qt.UserRole, shift)  # 存储原始数据
                self.shift_list.addItem(item)
        except Error as e:
            QMessageBox.critical(self, "数据库错误", f"无法加载班次列表:\n{str(e)}")

    def edit_selected_shift(self):
        """编辑选中的班次"""
        selected = self.shift_list.currentItem()
        if not selected:
            QMessageBox.warning(self, "警告", "请先选择一个班次")
            return
            
        shift_data = selected.data(Qt.UserRole)
        name, start_str, end_str = shift_data
        
        # 填充编辑表单
        self.shift_name.setText(name)
        
        if start_str:
            start_time = QTime.fromString(start_str, "HH:mm")
            self.start_time.setTime(start_time)
        else:
            self.start_time.setTime(QTime())
        
        if end_str:
            end_time = QTime.fromString(end_str, "HH:mm")
            self.end_time.setTime(end_time)
        else:
            self.end_time.setTime(QTime())
        
        # 更改按钮文本为"更新"
        self.add_update_btn.setText("更新")
        self.current_edit_name = name  # 存储当前编辑的班次名

    def delete_selected_shift(self):
        """删除选中的班次"""
        selected = self.shift_list.currentItem()
        if not selected:
            QMessageBox.warning(self, "警告", "请先选择一个班次")
            return
        
        name = selected.data(Qt.UserRole)[0]
        
        reply = QMessageBox.question(
            self, "确认删除",
            f"确定要删除班次 '{name}' 吗？",
            QMessageBox.Yes | QMessageBox.No, QMessageBox.No
        )
        
        if reply == QMessageBox.Yes:
            try:
                # 检查是否有排班使用此班次
                self.parent().cursor.execute("SELECT COUNT(*) FROM schedules WHERE shift_type = ?", (name,))
                count = self.parent().cursor.fetchone()[0]
                
                if count > 0:
                    QMessageBox.warning(self, "警告", f"无法删除，因为有 {count} 条排班记录使用此班次")
                    return
                    
                self.parent().cursor.execute("DELETE FROM custom_shifts WHERE shift_name = ?", (name,))
                self.parent().conn.commit()
                self.load_shift_list()
                self.parent().update_shifts_in_ui()  # 更新主界面中的班次下拉框
            except Error as e:
                QMessageBox.critical(self, "数据库错误", f"无法删除班次:\n{str(e)}")

    def add_or_update_shift(self, dialog):
        """添加或更新班次"""
        name = self.shift_name.text().strip()
        if not name:
            QMessageBox.warning(self, "警告", "请输入班次名称")
            return
        
        # 处理时间输入
        start_time = self.start_time.time().toString("HH:mm") if self.start_time.time().isValid() else ""
        end_time = self.end_time.time().toString("HH:mm") if self.end_time.time().isValid() else ""
        
        try:
            if hasattr(self, 'current_edit_name') and self.current_edit_name:
                # 更新现有班次
                self.parent().cursor.execute(
                    "UPDATE custom_shifts SET shift_name=?, start_time=?, end_time=? WHERE shift_name=?",
                    (name, start_time, end_time, self.current_edit_name)
                )
                delattr(self, 'current_edit_name')
                self.add_update_btn.setText("添加")
            else:
                # 添加新班次
                self.parent().cursor.execute(
                    "INSERT OR REPLACE INTO custom_shifts (shift_name, start_time, end_time) VALUES (?, ?, ?)",
                    (name, start_time, end_time)
                )
            
            self.parent().conn.commit()
            self.load_shift_list()
            self.parent().update_shifts_in_ui()  # 更新主界面中的班次下拉框
            
            # 重置表单
            self.shift_name.clear()
            self.start_time.setTime(QTime(8, 0))
            self.end_time.setTime(QTime(17, 0))
            
        except Error as e:
            QMessageBox.critical(self, "数据库错误", f"无法保存班次:\n{str(e)}")





    def get_data(self):
        """获取表单数据"""
        return (
            self.employee_name.text().strip(),
            self.department.currentText().strip(),
            self.position.text().strip(),
            self.work_date.date().toString("yyyy-MM-dd"),
            self.shift_type.currentText(),
            self.remarks.text().strip()
        )
    
    def set_data(self, data):
        """设置表单数据"""
        self.employee_name.setText(data[0])
        
        dept_index = self.department.findText(data[1])
        if dept_index >= 0:
            self.department.setCurrentIndex(dept_index)
        else:
            self.department.setCurrentText(data[1])
        
        self.position.setText(data[2])
        self.work_date.setDate(QDate.fromString(data[3], "yyyy-MM-dd"))
        
        shift_index = self.shift_type.findText(data[4])
        if shift_index >= 0:
            self.shift_type.setCurrentIndex(shift_index)
        else:
            self.shift_type.setCurrentText(data[4])
        
        self.remarks.setText(data[5] if data[5] else "")

        # 只有在添加模式下才更新最后选择的值
        if not self.is_edit_mode:
            ScheduleDialog.last_department = data[1]
            ScheduleDialog.last_shift_type = data[4]

    def set_date(self, date):
        """设置对话框日期"""
        self.work_date.setDate(date)

class BatchDeleteDialog(QDialog):
    """批量删除排班对话框"""
    def __init__(self, parent=None, schedules=None):
        super().__init__(parent)
        
        self.setWindowTitle("批量删除排班")
        self.setWindowIcon(QIcon('icon.ico'))
        self.resize(800, 600)  # 增大对话框尺寸
        
        layout = QVBoxLayout()
        self.setLayout(layout)
        
        # 提示信息和过滤区域
        filter_layout = QHBoxLayout()
        
        # 员工姓名过滤
        self.name_filter = QLineEdit()
        self.name_filter.setPlaceholderText("过滤员工姓名")
        self.name_filter.textChanged.connect(self.filter_schedules)
        filter_layout.addWidget(QLabel("员工姓名:"))
        filter_layout.addWidget(self.name_filter)
        
        # 部门过滤
        self.dept_filter = QComboBox()
        self.dept_filter.addItem("所有部门", "")
        self.dept_filter.currentIndexChanged.connect(self.filter_schedules)
        filter_layout.addWidget(QLabel("部门:"))
        filter_layout.addWidget(self.dept_filter)
        
        # 日期范围过滤
        self.date_filter = QComboBox()
        self.date_filter.addItem("所有日期", "")
        self.date_filter.addItem("今天", "today")
        self.date_filter.addItem("本周", "week")
        self.date_filter.addItem("本月", "month")
        self.date_filter.currentIndexChanged.connect(self.filter_schedules)
        filter_layout.addWidget(QLabel("日期范围:"))
        filter_layout.addWidget(self.date_filter)
        
        layout.addLayout(filter_layout)
        
        # 排班表格
        self.schedule_table = QTableWidget()
        self.schedule_table.setColumnCount(6)
        self.schedule_table.setHorizontalHeaderLabels(["员工姓名", "部门", "职位", "工作日期", "班次类型", "备注"])
        self.schedule_table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.schedule_table.setSelectionMode(QTableWidget.MultiSelection)
        self.schedule_table.setSortingEnabled(True)
        
        # 存储所有排班数据
        self.all_schedules = schedules
        self.schedule_ids = [s[0] for s in schedules]
        
        # 加载部门列表
        departments = set()
        for s in schedules:
            departments.add(s[2])  # 部门在第2列
        for dept in sorted(departments):
            self.dept_filter.addItem(dept, dept)
        
        # 显示所有排班
        self.display_schedules(self.all_schedules)
        
        layout.addWidget(self.schedule_table)
        
        # 全选/取消全选按钮
        select_buttons = QHBoxLayout()
        select_all_btn = QPushButton("全选")
        select_all_btn.clicked.connect(self.select_all)
        select_buttons.addWidget(select_all_btn)
        
        deselect_all_btn = QPushButton("取消全选")
        deselect_all_btn.clicked.connect(self.deselect_all)
        select_buttons.addWidget(deselect_all_btn)
        
        layout.addLayout(select_buttons)
        
        # 按钮
        button_box = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel)
        button_box.accepted.connect(self.accept)
        button_box.rejected.connect(self.reject)
        layout.addWidget(button_box)

        # 设置按钮样式
        button_box.button(QDialogButtonBox.Ok).setStyleSheet(
            f"background-color: {MacaronColors.MINT_GREEN.name()}; color: black;")
        button_box.button(QDialogButtonBox.Cancel).setStyleSheet(
            f"background-color: {MacaronColors.ROSE_PINK.name()}; color: black;")
        select_all_btn.setStyleSheet(
            f"background-color: {MacaronColors.SKY_BLUE.name()}; color: black;")
        deselect_all_btn.setStyleSheet(
            f"background-color: {MacaronColors.ROSE_PINK.name()}; color: black;")
        
        self.original_schedules = schedules  # 存储原始数据顺序
    
    def display_schedules(self, schedules):
        """显示排班列表"""
        self.schedule_table.setRowCount(len(schedules))
        for row, schedule in enumerate(schedules):
            for col, data in enumerate(schedule[1:7]):  # 跳过ID列
                item = QTableWidgetItem(str(data))
                item.setFlags(item.flags() & ~Qt.ItemIsEditable)
                self.schedule_table.setItem(row, col, item)
    
    def filter_schedules(self):
        """过滤排班列表"""
        name_filter = self.name_filter.text().lower()
        dept_filter = self.dept_filter.currentData()
        date_filter = self.date_filter.currentData()
        
        today = QDate.currentDate()
        filtered = []
        
        for s in self.all_schedules:
            # 跳过ID列
            name, dept, pos, date, shift, remarks = s[1:7]
            
            # 应用过滤器
            if name_filter and name_filter not in name.lower():
                continue
            if dept_filter and dept != dept_filter:
                continue
            if date_filter:
                s_date = QDate.fromString(date, "yyyy-MM-dd")
                if date_filter == "today" and s_date != today:
                    continue
                elif date_filter == "week" and not (s_date >= today.addDays(-today.dayOfWeek()+1) and s_date <= today.addDays(7-today.dayOfWeek())):
                    continue
                elif date_filter == "month" and s_date.month() != today.month():
                    continue
            
            filtered.append(s)
        
        self.display_schedules(filtered)
    
    def select_all(self):
        """全选所有行"""
        self.schedule_table.selectAll()
    
    def deselect_all(self):
        """取消全选"""
        self.schedule_table.clearSelection()
    
    def get_selected_ids(self):
        """获取选中的排班ID，考虑排序后的行顺序"""
        selected_rows = set()
        for item in self.schedule_table.selectedItems():
            selected_rows.add(item.row())
        
        # 获取过滤后的排班ID
        filtered_ids = []
        
        # 获取当前排序顺序
        sort_column = self.schedule_table.horizontalHeader().sortIndicatorSection()
        sort_order = self.schedule_table.horizontalHeader().sortIndicatorOrder()
        
        # 如果有排序，需要先获取排序后的行顺序
        if sort_column >= 0:
            # 获取当前显示的所有行数据
            visible_schedules = []
            for row in range(self.schedule_table.rowCount()):
                row_data = []
                for col in range(self.schedule_table.columnCount()):
                    item = self.schedule_table.item(row, col)
                    row_data.append(item.text() if item else "")
                visible_schedules.append(row_data)
            
            # 根据原始数据找到对应的ID
            for row in selected_rows:
                if row < len(visible_schedules):
                    # 获取当前行的数据
                    row_data = visible_schedules[row]
                    # 在原始数据中查找匹配的行
                    for original_row, sched in enumerate(self.original_schedules):
                        # 比较除ID外的所有列
                        if list(sched[1:7]) == row_data:
                            filtered_ids.append(sched[0])
                            break
        else:
            # 没有排序，直接使用行索引
            for row in selected_rows:
                if row < len(self.schedule_ids):
                    filtered_ids.append(self.schedule_ids[row])
        
        return filtered_ids




class ScheduleManager(QMainWindow):
    def __init__(self):
        super().__init__()
        # 初始化默认大小
        self.default_month_size = QSize(800, 600)
        self.default_year_size = QSize(1000, 800)
        self.default_two_year_size = QSize(1200, 800)

        # 初始化当前视图大小
        self.month_view_size = self.default_month_size
        self.year_size = self.default_year_size
        self.two_year_size = self.default_two_year_size

        # 跟踪当前视图类型
        self.current_view_type = 'month'  # 初始为月视图

        # 添加新的显示模式状态
        self.show_time_block_view = False  # 是否显示时间段区块模式

        # 初始化配置
        self.settings = QSettings("Duma", "ScheduleManager")

        # 实时自动保存防抖定时器（500ms 内无更多变更才写盘）
        self._settings_save_timer = QTimer(self)
        self._settings_save_timer.setSingleShot(True)
        self._settings_save_timer.setInterval(500)
        self._settings_save_timer.timeout.connect(self._save_settings_now)

        # 加载所有持久化设置（保证下次启动沿用上次的设置和修改）
        self.load_settings()

        # 初始化用户数据库
        try:
            UserManager.init_users_db()
        except Exception as e:
            QMessageBox.critical(None, "初始化错误", str(e))
            sys.exit(1)
            
        # 显示登录对话框
        if not self.show_login_dialog():
            sys.exit(0)
            
        self.setWindowTitle(f"{ProjectInfo.NAME} {ProjectInfo.VERSION} - 当前用户: {self.current_user}")
        self.setWindowIcon(QIcon('icon.ico'))
        # 首次启动（未保存窗口几何）时使用默认大小
        if not self.settings.contains("window_geometry"):
            self.resize(1000, 600)
        
        # 初始化数据库
        self.init_db()

        # 初始化当前日期（若 load_settings 已恢复则保留）
        if not hasattr(self, 'current_date') or not self.current_date:
            self.current_date = QDate.currentDate()

        self.name_color_map = {}  # 存储姓名到颜色的映射
        self.color_list = [
            MacaronColors.SAKURA_PINK, MacaronColors.SKY_BLUE, MacaronColors.MINT_GREEN,
            MacaronColors.LEMON_YELLOW, MacaronColors.LAVENDER, MacaronColors.PEACH_ORANGE,
            MacaronColors.ROSE_PINK, MacaronColors.LILAC_MIST, MacaronColors.APPLE_GREEN,
            MacaronColors.BUTTER_CREAM, MacaronColors.TARO_PURPLE, MacaronColors.CARAMEL_CREAM
        ]        
        
        # 添加自动备份定时器
        self.backup_timer = QTimer(self)
        self.backup_timer.timeout.connect(self.auto_backup)
        self.backup_timer.start(24 * 60 * 60 * 1000)  # 每天备份一次
        
        # 首次启动时立即备份
        QTimer.singleShot(5000, self.auto_backup)        

        # 创建UI
        self.init_ui()
        
        # 加载数据
        self.load_data()

    def load_settings(self):
        """加载所有持久化设置，保证下次启动沿用上次的设置和修改"""
        # 时间显示模式
        self.show_time_block_view = self.settings.value("time_block_view", False, bool)
        # 视图状态
        self.show_year_view = self.settings.value("show_year_view", False, bool)
        self.show_two_months = self.settings.value("show_two_months", False, bool)
        self.show_two_years = self.settings.value("show_two_years", False, bool)
        self.current_view_type = self.settings.value("current_view_type", "month", str)
        self.is_calendar_view = self.settings.value("is_calendar_view", True, bool)
        # 各视图大小
        self.month_view_size = self.settings.value("month_view_size", self.default_month_size, QSize)
        self.year_size = self.settings.value("year_size", self.default_year_size, QSize)
        self.two_year_size = self.settings.value("two_year_size", self.default_two_year_size, QSize)
        # 当前日期（最后查看的年月）
        date_str = self.settings.value("current_date", "", str)
        restored_date = QDate.fromString(date_str, "yyyy-MM-dd") if date_str else QDate()
        self.current_date = restored_date if restored_date.isValid() else QDate.currentDate()
        self.current_year = self.current_date.year()
        # 窗口几何与最大化状态
        geometry = self.settings.value("window_geometry")
        if geometry:
            self.restoreGeometry(geometry)
        self._start_maximized = self.settings.value("window_maximized", False, bool)
        # 日历配置（键不存在时写入默认值）
        self.load_calendar_config()

    def _autosave_settings(self):
        """防抖自动保存设置（500ms 内无更多变更再写盘）"""
        self._settings_save_timer.start()

    def _save_settings_now(self):
        """立即把当前所有设置写入持久化存储"""
        # 时间显示模式
        self.settings.setValue("time_block_view", self.show_time_block_view)
        # 视图状态
        self.settings.setValue("show_year_view", self.show_year_view)
        self.settings.setValue("show_two_months", self.show_two_months)
        self.settings.setValue("show_two_years", self.show_two_years)
        self.settings.setValue("current_view_type", self.current_view_type)
        self.settings.setValue("is_calendar_view", self.is_calendar_view)
        # 各视图大小
        self.settings.setValue("month_view_size", self.month_view_size if self.month_view_size else self.default_month_size)
        self.settings.setValue("year_size", self.year_size if self.year_size else self.default_year_size)
        self.settings.setValue("two_year_size", self.two_year_size if self.two_year_size else self.default_two_year_size)
        # 当前日期
        if self.current_date:
            self.settings.setValue("current_date", self.current_date.toString("yyyy-MM-dd"))
        # 窗口几何与最大化状态
        self.settings.setValue("window_geometry", self.saveGeometry())
        self.settings.setValue("window_maximized", self.isMaximized())
        # 日历配置（配置对话框控件存在时取其当前值）
        if hasattr(self, 'show_date_check'):
            self.settings.setValue("calendar/show_date", self.show_date_check.isChecked())
            self.settings.setValue("calendar/show_name", self.show_name_check.isChecked())
            self.settings.setValue("calendar/show_dept", self.show_dept_check.isChecked())
            self.settings.setValue("calendar/show_shift", self.show_shift_check.isChecked())
            self.settings.setValue("calendar/date_font_size", self.date_font_size.value())
            self.settings.setValue("calendar/content_font_size", self.content_font_size.value())
            self.settings.setValue("calendar/time_block_date_font_size", self.time_block_date_font_size.value())
            self.settings.setValue("calendar/time_block_content_font_size", self.time_block_content_font_size.value())
            self.settings.setValue("calendar/no_schedule_font_size", self.no_schedule_font_size.value())
        # 立即写入磁盘
        self.settings.sync()

    def auto_backup(self):
        """自动备份数据库"""
        try:
            backup_file = UserManager.backup_db(self.user_db_file, "auto")
            print(f"[INFO] 自动备份完成: {backup_file}")
        except Exception as e:
            print(f"[ERROR] 自动备份失败: {str(e)}")

    def show_login_dialog(self):
        """显示登录对话框"""
        dialog = QDialog()
        dialog.setWindowTitle("用户登录")
        dialog.setWindowIcon(QIcon('icon.ico'))
        dialog.resize(300, 200)
        
        layout = QFormLayout(dialog)
        
        # 用户名 - 改为QComboBox
        self.username_combo = QComboBox()
        self.username_combo.setEditable(True)  # 允许用户输入新用户名
        self.username_combo.setPlaceholderText("选择或输入用户名")
        layout.addRow("用户名:", self.username_combo)
        
        # 密码
        self.password_input = QLineEdit()
        self.password_input.setPlaceholderText("输入密码(可选)")
        self.password_input.setEchoMode(QLineEdit.Password)
        layout.addRow("密码:", self.password_input)
        
        # 记住密码复选框
        self.remember_check = QCheckBox("记住密码")
        layout.addRow(self.remember_check)
        
        # 加载已注册用户
        self.load_registered_users()
        
        # 加载保存的登录配置
        username, password, remember = UserManager.load_login_config()
        if username:
            # 先尝试在下拉框中查找匹配项
            index = self.username_combo.findText(username)
            if index >= 0:
                self.username_combo.setCurrentIndex(index)
            else:
                # 如果没找到，直接设置当前文本
                self.username_combo.setEditText(username)
            
            # 只有当记住密码时才填充密码
            if remember and password:
                self.password_input.setText(password)
                self.remember_check.setChecked(True)
        
        # 按钮
        button_box = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel)
        button_box.accepted.connect(lambda: self.handle_login(dialog))
        button_box.rejected.connect(dialog.reject)
        layout.addRow(button_box)
        
        # 创建水平布局用于按钮
        button_row = QHBoxLayout()
        button_row.setSpacing(10)  # 设置按钮间距

        # 设置按钮样式
        button_box.button(QDialogButtonBox.Ok).setStyleSheet(
            f"background-color: {MacaronColors.MINT_GREEN.name()}; color: black;")
        button_box.button(QDialogButtonBox.Cancel).setStyleSheet(
            f"background-color: {MacaronColors.ROSE_PINK.name()}; color: black;")
    
        # 删除用户按钮
        delete_btn = QPushButton("删除用户")
        delete_btn.setStyleSheet(
            f"background-color: {MacaronColors.ROSE_PINK.name()}; color: black;")  # 玫瑰粉
        delete_btn.clicked.connect(lambda: self.show_delete_user_dialog(dialog))
        button_row.addWidget(delete_btn)

        # 注册按钮
        register_btn = QPushButton("注册新用户")
        register_btn.setStyleSheet(
            f"background-color: {MacaronColors.MINT_GREEN.name()}; color: black;")  # 薄荷绿
        register_btn.clicked.connect(lambda: self.show_register_dialog(dialog))
        button_row.addWidget(register_btn)

        modify_btn = QPushButton("修改用户名")
        modify_btn.setStyleSheet(
            f"background-color: {MacaronColors.LAVENDER.name()}; color: black;")  # 薰衣草紫
        modify_btn.clicked.connect(lambda: self.show_modify_username_dialog(dialog))
        button_row.addWidget(modify_btn)


        # 将水平布局添加到表单布局中
        layout.addRow(button_row)
            
        return dialog.exec_() == QDialog.Accepted


    def load_registered_users(self):
        """加载已注册用户到下拉列表"""
        try:
            conn = sqlite3.connect(UserManager.USERS_DB)
            cursor = conn.cursor()
            cursor.execute("SELECT username FROM users ORDER BY username")
            users = cursor.fetchall()
            
            self.username_combo.clear()
            for user in users:
                self.username_combo.addItem(user[0])
                
        except Error as e:
            print(f"加载用户列表失败: {str(e)}")
        finally:
            if 'conn' in locals():
                conn.close()

    def handle_login(self, dialog):
        """处理登录"""
        username = self.username_combo.currentText().strip()
        password = self.password_input.text().strip()
        remember = self.remember_check.isChecked()
        
        if not username:
            QMessageBox.warning(dialog, "输入错误", "用户名不能为空")
            return
            
        try:
            db_file = UserManager.authenticate(username, password)
            if db_file:
                self.current_user = username
                self.user_db_file = db_file
                # 总是保存用户名，但根据选择决定是否保存密码
                UserManager.save_login_config(username, password, remember)
                dialog.accept()
            else:
                QMessageBox.warning(dialog, "登录失败", "用户名或密码错误")
        except Exception as e:
            QMessageBox.critical(dialog, "登录错误", str(e))



    def show_register_dialog(self, parent_dialog):
        """显示注册对话框"""
        dialog = QDialog(parent_dialog)
        dialog.setWindowTitle("注册新用户")
        dialog.setWindowIcon(QIcon('icon.ico'))
        dialog.resize(300, 250)
        
        layout = QFormLayout(dialog)
        
        # 用户名
        new_username = QLineEdit()
        new_username.setPlaceholderText("输入新用户名")
        layout.addRow("用户名:", new_username)
        
        # 密码
        new_password = QLineEdit()
        new_password.setPlaceholderText("输入密码(可选)")
        new_password.setEchoMode(QLineEdit.Password)
        layout.addRow("密码:", new_password)
        
        # 确认密码
        confirm_password = QLineEdit()
        confirm_password.setPlaceholderText("确认密码(可选)")
        confirm_password.setEchoMode(QLineEdit.Password)
        layout.addRow("确认密码:", confirm_password)
        
        # 提示标签
        info_label = QLabel("提示: 密码是可选的，如果不设置密码，\n任何人都可以使用此用户名登录")
        info_label.setStyleSheet("color: gray;")
        layout.addRow(info_label)
        
        # 按钮
        button_box = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel)
        button_box.accepted.connect(lambda: self.handle_register(
            dialog, new_username.text(), new_password.text(), confirm_password.text()
        ))
        button_box.rejected.connect(dialog.reject)
        layout.addRow(button_box)
        
        dialog.exec_()




            
    def handle_register(self, dialog, username, password, confirm_password):
        """处理注册"""
        if not username:
            QMessageBox.warning(dialog, "输入错误", "用户名不能为空")
            return
            
        # 检查密码是否匹配(如果有密码)
        if password or confirm_password:
            if password != confirm_password:
                QMessageBox.warning(dialog, "输入错误", "两次输入的密码不匹配")
                return
                
        try:
            if UserManager.create_user(username, password):
                QMessageBox.information(dialog, "注册成功", "用户注册成功，请登录")
                # 注册成功后刷新用户列表
                self.load_registered_users()
                dialog.accept()
        except Exception as e:
            QMessageBox.critical(dialog, "注册错误", str(e))

    def show_delete_user_dialog(self, parent_dialog):
        """显示删除用户对话框"""
        dialog = QDialog(parent_dialog)
        dialog.setWindowTitle("删除用户")
        dialog.setWindowIcon(QIcon('icon.ico'))
        dialog.resize(300, 150)
        
        layout = QFormLayout(dialog)
        
        # 用户名选择
        username_combo = QComboBox()
        try:
            conn = sqlite3.connect(UserManager.USERS_DB)
            cursor = conn.cursor()
            cursor.execute("SELECT username FROM users ORDER BY username")
            users = cursor.fetchall()
            
            for user in users:
                username_combo.addItem(user[0])
        except Error as e:
            QMessageBox.critical(dialog, "错误", f"无法加载用户列表: {str(e)}")
            return
        finally:
            if 'conn' in locals():
                conn.close()
        
        layout.addRow("选择用户:", username_combo)
        
        # 密码验证
        password_input = QLineEdit()
        password_input.setPlaceholderText("输入密码验证")
        password_input.setEchoMode(QLineEdit.Password)
        layout.addRow("密码验证:", password_input)
        
        # 按钮
        button_box = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel)
        button_box.accepted.connect(lambda: self.handle_delete_user(
            dialog, username_combo.currentText(), password_input.text()
        ))
        button_box.rejected.connect(dialog.reject)
        layout.addRow(button_box)
        
        dialog.exec_()

    def handle_delete_user(self, dialog, username, password):
        """处理用户删除请求"""
        if not username:
            QMessageBox.warning(dialog, "错误", "请选择要删除的用户")
            return
            
        try:
            # 验证密码
            conn = sqlite3.connect(UserManager.USERS_DB)
            cursor = conn.cursor()
            cursor.execute(
                "SELECT password FROM users WHERE username=?",
                (username,)
            )
            result = cursor.fetchone()
            
            if not result:
                QMessageBox.warning(dialog, "错误", "用户不存在")
                return
                
            stored_password = result[0]
            
            # 如果有密码但未提供密码，或密码不匹配
            if stored_password and (not password or stored_password != password):
                QMessageBox.warning(dialog, "错误", "密码验证失败")
                return
                
            # 确认删除
            reply = QMessageBox.question(
                dialog, "确认删除",
                f"确定要永久删除用户 {username} 吗？此操作不可撤销！",
                QMessageBox.Yes | QMessageBox.No, QMessageBox.No
            )
            
            if reply == QMessageBox.Yes:
                if UserManager.delete_user(username):
                    QMessageBox.information(dialog, "成功", "用户已删除")
                    dialog.accept()
                    # 刷新登录对话框的用户列表
                    self.load_registered_users()
                else:
                    QMessageBox.warning(dialog, "错误", "删除用户失败")
        except Exception as e:
            print(f"[DEBUG] 删除用户时出错: {str(e)}")
            QMessageBox.critical(dialog, "错误", f"删除用户时出错: {str(e)}")


    def init_db(self):
        """初始化数据库 - 修改为使用用户特定的数据库文件"""
        try:
            # 使用用户特定的数据库文件
            self.conn = sqlite3.connect(self.user_db_file)
            self.cursor = self.conn.cursor()
            
            # 创建部门表
            self.cursor.execute('''
                CREATE TABLE IF NOT EXISTS departments (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    name TEXT NOT NULL UNIQUE
                )
            ''')
            
            # 插入默认部门
            default_depts = ["销售部", "技术部", "人事部", "财务部", "市场部", "客服部"]
            for dept in default_depts:
                try:
                    self.cursor.execute("INSERT OR IGNORE INTO departments (name) VALUES (?)", (dept,))
                except Error as e:
                    print(f"插入部门 {dept} 时出错: {str(e)}")
            
            # 创建排班表
            self.cursor.execute('''
                CREATE TABLE IF NOT EXISTS schedules (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    employee_name TEXT NOT NULL,
                    department TEXT NOT NULL,
                    position TEXT NOT NULL,
                    work_date TEXT NOT NULL,
                    shift_type TEXT NOT NULL,
                    remarks TEXT,
                    FOREIGN KEY(department) REFERENCES departments(name)
                )
            ''')
            
            # 创建自定义班次表
            self.cursor.execute('''
                CREATE TABLE IF NOT EXISTS custom_shifts (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    shift_name TEXT NOT NULL,
                    start_time TEXT NOT NULL,
                    end_time TEXT NOT NULL,
                    UNIQUE(shift_name)
                )
            ''')
            
            # 插入默认班次
            default_shifts = [
                ("早班", "08:00", "16:00"),
                ("中班", "16:00", "24:00"),
                ("晚班", "00:00", "08:00"),
                ("全天班", "08:00", "20:00"),
                ("早班(模糊)", "", ""),
                ("晚班(模糊)", "", "")
            ]
            for shift in default_shifts:
                try:
                    self.cursor.execute("INSERT OR IGNORE INTO custom_shifts (shift_name, start_time, end_time) VALUES (?, ?, ?)", shift)
                except Error as e:
                    print(f"插入班次 {shift[0]} 时出错: {str(e)}")
            
            self.conn.commit()
        except Error as e:
            QMessageBox.critical(self, "数据库错误", f"无法初始化数据库:\n{str(e)}")
            raise
    
    def init_ui(self):
        """初始化用户界面"""
        # 主窗口部件
        main_widget = QWidget()
        self.setCentralWidget(main_widget)
        
        # 主布局
        main_layout = QVBoxLayout()
        main_widget.setLayout(main_layout)

        # 添加月份导航和视图切换
        top_bar_layout = QHBoxLayout()
        main_layout.addLayout(top_bar_layout)
        
        # 月份导航
        month_nav_layout = QHBoxLayout()
        top_bar_layout.addLayout(month_nav_layout)
        
        self.prev_month_btn = QPushButton("◀ 上个月")
        self.prev_month_btn.clicked.connect(self.prev_month)
        month_nav_layout.addWidget(self.prev_month_btn)
        
        self.month_label = QLabel()
        self.month_label.setAlignment(Qt.AlignCenter)
        self.month_label.setStyleSheet("font-size: 16px; font-weight: bold;")
        month_nav_layout.addWidget(self.month_label)
        
        self.next_month_btn = QPushButton("下个月 ▶")
        self.next_month_btn.clicked.connect(self.next_month)
        month_nav_layout.addWidget(self.next_month_btn)

        # 添加新的显示模式按钮
        self.time_block_btn = QPushButton("时间显示: " + ("区块" if self.show_time_block_view else "文本"))
        self.time_block_btn.setCheckable(True)
        self.time_block_btn.setChecked(self.show_time_block_view)
        self.time_block_btn.clicked.connect(self.toggle_time_block_view)
        month_nav_layout.addWidget(self.time_block_btn)

        # 添加两个月视图切换按钮
        self.two_month_btn = QPushButton("显示两个月")
        self.two_month_btn.setCheckable(True)
        self.two_month_btn.setChecked(self.show_two_months)
        self.two_month_btn.setText("显示单月" if self.show_two_months else "显示两个月")
        self.two_month_btn.clicked.connect(self.toggle_two_month_view)
        month_nav_layout.addWidget(self.two_month_btn)
        
        # 添加年份视图切换按钮
        self.year_view_btn = QPushButton("切换年视图")
        self.year_view_btn.setCheckable(True)
        self.year_view_btn.setChecked(self.show_year_view)
        self.year_view_btn.setText("切换月视图" if self.show_year_view else "切换年视图")
        self.year_view_btn.clicked.connect(self.toggle_year_view)
        month_nav_layout.addWidget(self.year_view_btn)

        # 添加双年视图切换按钮
        self.two_year_btn = QPushButton("显示双年视图")
        self.two_year_btn.setCheckable(True)
        self.two_year_btn.setChecked(self.show_two_years)
        self.two_year_btn.setText("显示单年视图" if self.show_two_years else "显示双年视图")
        self.two_year_btn.clicked.connect(self.toggle_two_year_view)
        month_nav_layout.addWidget(self.two_year_btn)

        # 添加状态变量（若 load_settings 已恢复则保留）
        if not hasattr(self, 'show_two_years'):
            self.show_two_years = False

        # 添加状态变量（若 load_settings 已恢复则保留）
        if not hasattr(self, 'show_year_view'):
            self.show_year_view = False
        self.current_year = self.current_date.year()

        # 添加间隔
        top_bar_layout.addStretch()

        # 添加状态变量（若 load_settings 已恢复则保留）
        if not hasattr(self, 'show_two_months'):
            self.show_two_months = False

        # 添加间隔
        top_bar_layout.addStretch()
        
        # 视图切换按钮（按保存的视图状态设置文本）
        self.view_toggle_btn = QPushButton("切换为月历视图" if not self.is_calendar_view else "切换为列表视图")
        self.view_toggle_btn.clicked.connect(self.toggle_view)
        top_bar_layout.addWidget(self.view_toggle_btn)
        
        # 添加日历配置按钮
        self.calendar_config_btn = QPushButton("日历配置")
        self.calendar_config_btn.clicked.connect(self.show_calendar_config_dialog)
        top_bar_layout.addWidget(self.calendar_config_btn)

        # 在顶部工具栏添加备份按钮
        backup_layout = QHBoxLayout()
        top_bar_layout.addLayout(backup_layout)
        
        self.backup_btn = QPushButton("手动备份")
        self.backup_btn.clicked.connect(self.manual_backup)
        backup_layout.addWidget(self.backup_btn)
        
        self.restore_btn = QPushButton("恢复备份")
        self.restore_btn.clicked.connect(self.show_restore_dialog)
        backup_layout.addWidget(self.restore_btn)
        # 设置按钮样式
        self.backup_btn.setStyleSheet(
            f"background-color: {MacaronColors.MINT_GREEN.name()}; color: black;")
        self.restore_btn.setStyleSheet(
            f"background-color: {MacaronColors.SKY_BLUE.name()}; color: black;")

        self.switch_user_btn = QPushButton(f"切换用户 ({self.current_user})")
        self.switch_user_btn.clicked.connect(self.switch_user)
        top_bar_layout.addWidget(self.switch_user_btn)

        # 当前视图状态（若 load_settings 已恢复则保留）
        if not hasattr(self, 'is_calendar_view'):
            self.is_calendar_view = True
        
        # 日历视图容器
        self.calendar_container = QWidget()
        self.calendar_layout = QVBoxLayout(self.calendar_container)
        self.calendar_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.addWidget(self.calendar_container)
        
        # 列表视图容器
        self.list_container = QWidget()
        self.list_layout = QVBoxLayout(self.list_container)
        self.list_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.addWidget(self.list_container)
        self.list_container.hide()
        
        # 初始化列表视图
        self.init_list_view()
        
        # 设置当前月份（若 load_settings 已恢复则保留）
        if not hasattr(self, 'current_date') or not self.current_date:
            self.current_date = QDate.currentDate()
        
        # 加载日历配置（键不存在时写入默认值）
        self.load_calendar_config()

        # 根据保存的视图状态显示对应的视图容器
        if self.is_calendar_view:
            self.calendar_container.show()
            self.list_container.hide()
            self.update_calendar_view()
        else:
            self.calendar_container.hide()
            self.list_container.show()
            self.view_toggle_btn.setText("切换为月历视图")
        
        # 状态栏
        self.statusBar().showMessage("就绪")

        # 设置按钮样式
        self.set_button_styles()

    def show_calendar_config_dialog(self):
        """显示日历配置对话框"""
        dialog = QDialog(self)
        dialog.setWindowTitle("日历视图配置")
        dialog.resize(400, 350)
        
        layout = QVBoxLayout()
        dialog.setLayout(layout)
        
        # 显示内容配置
        content_group = QGroupBox("显示内容")
        content_layout = QVBoxLayout()
        
        self.show_date_check = QCheckBox("显示日期")
        self.show_name_check = QCheckBox("显示员工姓名")
        self.show_dept_check = QCheckBox("显示部门")
        self.show_shift_check = QCheckBox("显示班次类型")
        
        # 从设置加载当前状态
        self.show_date_check.setChecked(self.settings.value("calendar/show_date", True, bool))
        self.show_name_check.setChecked(self.settings.value("calendar/show_name", True, bool))
        self.show_dept_check.setChecked(self.settings.value("calendar/show_dept", True, bool))
        self.show_shift_check.setChecked(self.settings.value("calendar/show_shift", True, bool))
        
        content_layout.addWidget(self.show_date_check)
        content_layout.addWidget(self.show_name_check)
        content_layout.addWidget(self.show_dept_check)
        content_layout.addWidget(self.show_shift_check)
        content_group.setLayout(content_layout)
        layout.addWidget(content_group)
        
        # 字体大小配置
        font_group = QGroupBox("字体设置")
        font_layout = QFormLayout()
        
        self.date_font_size = QSpinBox()
        self.date_font_size.setRange(6, 50) # 设置日期字体大小范围
        self.date_font_size.setValue(self.settings.value("calendar/date_font_size", 12, int))
        
        self.content_font_size = QSpinBox()
        self.content_font_size.setRange(6, 50) # 设置内容字体大小范围
        self.content_font_size.setValue(self.settings.value("calendar/content_font_size", 10, int))

        # 添加时间区块模式下的字体大小设置
        self.time_block_date_font_size = QSpinBox()
        self.time_block_date_font_size.setRange(6, 50)
        self.time_block_date_font_size.setValue(self.settings.value("calendar/time_block_date_font_size", 12, int))

        self.time_block_content_font_size = QSpinBox()
        self.time_block_content_font_size.setRange(6, 50)
        self.time_block_content_font_size.setValue(self.settings.value("calendar/time_block_content_font_size", 9, int))
        
        self.no_schedule_font_size = QSpinBox()
        self.no_schedule_font_size.setRange(6, 50)
        self.no_schedule_font_size.setValue(self.settings.value("calendar/no_schedule_font_size", 12, int))
        
        font_layout.addRow("普通视图日期字体大小:", self.date_font_size)
        font_layout.addRow("普通视图内容字体大小:", self.content_font_size)
        font_layout.addRow("区块视图日期字体大小:", self.time_block_date_font_size)
        font_layout.addRow("区块视图内容字体大小:", self.time_block_content_font_size)
        font_layout.addRow("无排班日期的字体大小:", self.no_schedule_font_size)

        font_group.setLayout(font_layout)
        layout.addWidget(font_group)

        # 实时自动保存：控件变化立即防抖写盘，无需点击确定
        self.show_date_check.toggled.connect(self._autosave_settings)
        self.show_name_check.toggled.connect(self._autosave_settings)
        self.show_dept_check.toggled.connect(self._autosave_settings)
        self.show_shift_check.toggled.connect(self._autosave_settings)
        self.date_font_size.valueChanged.connect(self._autosave_settings)
        self.content_font_size.valueChanged.connect(self._autosave_settings)
        self.time_block_date_font_size.valueChanged.connect(self._autosave_settings)
        self.time_block_content_font_size.valueChanged.connect(self._autosave_settings)
        self.no_schedule_font_size.valueChanged.connect(self._autosave_settings)
        
        # 按钮
        button_box = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel)
        button_box.accepted.connect(lambda: self.save_calendar_config(dialog))
        button_box.rejected.connect(dialog.reject)
        layout.addWidget(button_box)
        
        dialog.exec_()

    def save_calendar_config(self, dialog):
        """保存日历配置"""
        # 原有设置
        self.settings.setValue("calendar/show_date", self.show_date_check.isChecked())
        self.settings.setValue("calendar/show_name", self.show_name_check.isChecked())
        self.settings.setValue("calendar/show_dept", self.show_dept_check.isChecked())
        self.settings.setValue("calendar/show_shift", self.show_shift_check.isChecked())
        
        # 字体大小设置
        self.settings.setValue("calendar/date_font_size", self.date_font_size.value())
        self.settings.setValue("calendar/content_font_size", self.content_font_size.value())
        self.settings.setValue("calendar/time_block_date_font_size", self.time_block_date_font_size.value())
        self.settings.setValue("calendar/time_block_content_font_size", self.time_block_content_font_size.value())
        self.settings.setValue("calendar/no_schedule_font_size", self.no_schedule_font_size.value())
        
        dialog.accept()
        self.update_calendar_view()


    def load_calendar_config(self):
        """加载日历配置"""
        # 如果配置不存在，设置默认值
        if not self.settings.contains("calendar/show_date"):
            self.settings.setValue("calendar/show_date", True)
            self.settings.setValue("calendar/show_name", True)
            self.settings.setValue("calendar/show_dept", True)
            self.settings.setValue("calendar/show_shift", True)
            self.settings.setValue("calendar/date_font_size", 12)
            self.settings.setValue("calendar/content_font_size", 10)

    def prev_month(self):
        """切换到上个月/上一年"""
        if self.show_year_view:
            self.current_year -= 1
        else:
            self.current_date = self.current_date.addMonths(-1)
        self.update_calendar_view()
        self._autosave_settings()

    def next_month(self):
        """切换到下个月/下一年"""
        if self.show_year_view:
            self.current_year += 1
        else:
            self.current_date = self.current_date.addMonths(1)
        self.update_calendar_view()
        self._autosave_settings()

    def toggle_two_month_view(self):
        """切换是否显示两个月"""
        # print("[DEBUG] 切换两个月视图")
        # 保存当前视图大小
        if self.show_two_months:  # 当前是双月视图，切换回单月视图
            # print("[DEBUG] 切换到单月视图")
            self.month_view_size = self.size()
            # print(f"[DEBUG] 保存单月视图大小: {self.month_view_size}")
        else:  # 当前是单月视图，切换到双月视图
            # 只在从单月视图切换到双月视图时保存
            if not self.show_two_months and not self.show_year_view:
                # print("[DEBUG] 保存双月视图大小")
                self.month_view_size = self.size()
                # print(f"[DEBUG] 保存双月视图大小: {self.month_view_size}")
        
        # 切换视图状态
        self.show_two_months = self.two_month_btn.isChecked()
        self.two_month_btn.setText("显示两个月" if not self.show_two_months else "显示单月")
        
        # 恢复目标视图大小
        if self.show_two_months and self.two_year_size:  # 如果有保存的双年视图大小
            self.resize(self.two_year_size)
            # print(f"[DEBUG] 恢复双年视图大小: {self.two_year_size}")
        elif not self.show_two_months and self.month_view_size:  # 恢复月视图大小
            self.resize(self.month_view_size)
            # print(f"[DEBUG] 恢复单月视图大小: {self.month_view_size}")
        
        self.update_calendar_view()
        self._autosave_settings()


    def update_single_month_view(self):
        """更新单月视图"""
        # 如果没有设置过月视图大小，设置一个默认值
        if not self.month_view_size:
            self.month_view_size = QSize(800, 600)  # 默认月视图大小
        
        # 设置月份标题
        self.month_label.setText(f"{self.current_date.year()}年{self.current_date.month()}月")
        
        # 创建日历表格
        calendar_table = self.create_calendar_table(self.current_date)
        self.calendar_layout.addWidget(calendar_table)


    def update_two_month_view(self):
        """更新双月视图"""
        # 设置月份标题
        next_month = self.current_date.addMonths(1)
        self.month_label.setText(
            f"{self.current_date.year()}年{self.current_date.month()}月 - "
            f"{next_month.year()}年{next_month.month()}月"
        )
        
        # 创建水平布局用于两个月份
        two_month_layout = QHBoxLayout()
        two_month_layout.setContentsMargins(0, 0, 0, 0)
        two_month_layout.setSpacing(20)
        
        # 添加当前月
        current_month_table = self.create_calendar_table(self.current_date)
        two_month_layout.addWidget(current_month_table)
        
        # 添加下个月
        next_month_table = self.create_calendar_table(self.current_date.addMonths(1))
        two_month_layout.addWidget(next_month_table)
        
        # 将双月布局添加到容器中
        container = QWidget()
        container.setLayout(two_month_layout)
        self.calendar_layout.addWidget(container)

    def create_calendar_table(self, date):
        """创建单个月份的日历表格"""
        # 创建日历表格
        calendar_table = QTableWidget()
        calendar_table.setEditTriggers(QTableWidget.NoEditTriggers)
        calendar_table.setSelectionMode(QTableWidget.NoSelection)
        
        # 设置表格样式
        calendar_table.setStyleSheet("""
            QTableWidget {
                gridline-color: #e0e0e0;
                font-size: 12px;
            }
            QTableWidget::item {
                padding: 5px;
                border: 1px solid #e0e0e0;
            }
        """)
        
        # 设置表格为7列(一周7天)
        calendar_table.setColumnCount(7)
        calendar_table.setHorizontalHeaderLabels(["周日", "周一", "周二", "周三", "周四", "周五", "周六"])
        
        # 设置表头样式
        calendar_table.horizontalHeader().setStyleSheet("""
            QHeaderView::section {
                background-color: #f5f5f5;
                padding: 5px;
                border: 1px solid #e0e0e0;
                font-weight: bold;
            }
        """)

        # 启用右键菜单
        calendar_table.setContextMenuPolicy(Qt.CustomContextMenu)
        calendar_table.customContextMenuRequested.connect(self.show_calendar_context_menu)

        # 计算当月天数
        month_days = date.daysInMonth()
        first_day = QDate(date.year(), date.month(), 1)
        start_day = first_day.dayOfWeek() % 7  # Qt的周日是7，我们调整为0
        
        # 计算需要的行数
        rows = ((start_day + month_days - 1) // 7) + 1
        calendar_table.setRowCount(rows)
        
        # 预先加载本月所有排班数据以确定颜色分配
        start_date = QDate(date.year(), date.month(), 1)
        end_date = QDate(date.year(), date.month(), month_days)
        
        try:
            self.cursor.execute('''
                SELECT DISTINCT employee_name 
                FROM schedules 
                WHERE work_date BETWEEN ? AND ?
                ORDER BY employee_name
            ''', (start_date.toString("yyyy-MM-dd"), end_date.toString("yyyy-MM-dd")))
            employees = self.cursor.fetchall()
            
            # 为每个员工分配颜色
            for emp in employees:
                name = emp[0]
                if name not in self.name_color_map:
                    color_idx = len(self.name_color_map) % len(self.color_list)
                    self.name_color_map[name] = self.color_list[color_idx]
        except Error as e:
            QMessageBox.critical(self, "数据库错误", f"无法加载员工列表:\n{str(e)}")
            return calendar_table
        
        # 填充日期
        for day in range(1, month_days + 1):
            current_date = QDate(date.year(), date.month(), day)
            day_of_week = current_date.dayOfWeek() % 7
            row = (start_day + day - 1) // 7
            
            # 创建空的日期单元格
            item = QTableWidgetItem()
            item.setData(Qt.UserRole, current_date)  # 存储日期对象
            item.setTextAlignment(Qt.AlignTop | Qt.AlignLeft)
            
            # 设置周末颜色
            if day_of_week == 0 or day_of_week == 6:  # 周日(0)或周六(6)
                item.setForeground(QColor(255, 0, 0))  # 红色
        
            calendar_table.setItem(row, day_of_week, item)
            
            # 根据显示模式加载数据
            if self.show_time_block_view:
                self.load_day_schedules_time_block(calendar_table, row, day_of_week, current_date)
            else:
                self.load_day_schedules(calendar_table, row, day_of_week, current_date)
        
        # 调整列宽和行高
        calendar_table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        calendar_table.verticalHeader().setSectionResizeMode(QHeaderView.Stretch)

        # 设置行高
        for row in range(calendar_table.rowCount()):
            calendar_table.setRowHeight(row, 100)  # 固定行高
        
        return calendar_table


    def toggle_view(self):
        # print("[DEBUG] 切换视图模式")
        """切换视图模式"""
        self.is_calendar_view = not self.is_calendar_view
        
        if self.is_calendar_view:
            self.calendar_container.show()
            self.list_container.hide()
            self.view_toggle_btn.setText("切换为列表视图")
            self.update_calendar_view()
        else:
            self.calendar_container.hide()
            self.list_container.show()
            self.view_toggle_btn.setText("切换为月历视图")
            self.load_data()
        self._autosave_settings()

    def update_calendar_view(self):
        """更新月历视图"""
        # print("[DEBUG] 更新月历视图")
        # 清除旧视图
        for i in reversed(range(self.calendar_layout.count())): 
            self.calendar_layout.itemAt(i).widget().setParent(None)
        
        if self.show_year_view:
            if self.show_two_years:
                self.update_two_year_view()
                # print("[DEBUG] 更新双年视图")
            else:
                self.update_year_view()
                # print("[DEBUG] 更新年视图")
        elif self.show_two_months:
            self.update_two_month_view()
            # print("[DEBUG] 更新双月视图")
        else:
            self.update_single_month_view()
            # print("[DEBUG] 更新单月视图")




    def load_day_schedules(self, table, row, col, date):
        """加载某一天的排班数据"""
        try:
            # 验证日期格式
            if not date.isValid():
                raise ValueError("无效日期")

            date_str = date.toString("yyyy-MM-dd")
            if "#" in date_str:  # 防御性检查
                raise ValueError("日期包含非法字符")

            self.cursor.execute('''
                SELECT employee_name, department, shift_type 
                FROM schedules 
                WHERE work_date = ?
                ORDER BY department, employee_name
            ''', (date_str,))
            schedules = self.cursor.fetchall()
            
            # 创建显示内容的文本
            content = QLabel()
            text = ""
            
            # 获取字体大小设置
            show_date = self.settings.value("calendar/show_date", True, bool)
            show_name = self.settings.value("calendar/show_name", True, bool)
            show_dept = self.settings.value("calendar/show_dept", True, bool)
            show_shift = self.settings.value("calendar/show_shift", True, bool)
            
            date_font_size = self.settings.value("calendar/date_font_size", 12, int)
            content_font_size = self.settings.value("calendar/content_font_size", 10, int)
            no_schedule_font_size = self.settings.value("calendar/no_schedule_font_size", 12, int)
            
            # 总是显示日期
            if show_date:
                text += f"<div style='font-weight:bold; font-size:{date_font_size}px;'>{date.day()}</div>"
            
            if schedules:
                for schedule in schedules:
                    name, dept, shift = schedule
                    # 为每个姓名分配颜色（如果尚未分配）
                    if name not in self.name_color_map:
                        color_idx = len(self.name_color_map) % len(self.color_list)
                        self.name_color_map[name] = self.color_list[color_idx]
                    
                    # 添加员工信息
                    line = []
                    if show_name and show_dept:
                        line.append(f"{name}({dept})")
                    elif show_name:
                        line.append(name)
                    elif show_dept:
                        line.append(dept)
                    
                    if show_shift:
                        line.append(shift)
                    
                    if line:
                        text += f"<div style='font-size:{content_font_size}px;'>" + " ".join(line) + "</div>"
                
                # 设置背景色 - 使用第一个员工的颜色
                first_name = schedules[0][0]
                content.setStyleSheet(f"""
                    background-color: {self.name_color_map[first_name].name()};
                    padding: 5px;
                    border-radius: 3px;
                """)
            else:
                # 无排班时的样式
                text += f"<div style='font-size:{no_schedule_font_size}px; color:gray;'>无排班</div>"
                content.setStyleSheet("""
                    padding: 5px;
                    border-radius: 3px;
                """)
            
            content.setText(text.strip())
            content.setAlignment(Qt.AlignTop | Qt.AlignLeft)
            content.setMargin(5)
            
            # 设置单元格属性
            content.setProperty("date", date_str)
            content.setProperty("has_data", bool(schedules))

            # 设置单元格部件
            table.setCellWidget(row, col, content)

        except ValueError as e:
            print(f"[DEBUG] 日期格式错误: {str(e)}")
            return
        except Error as e:
            QMessageBox.critical(self, "数据库错误", f"无法加载排班数据:\n{str(e)}")




    def init_list_view(self):
        """初始化列表视图"""
        # 顶部搜索和过滤区域
        filter_layout = QHBoxLayout()
        self.list_layout.addLayout(filter_layout)
        
        # 搜索框
        self.search_input = QLineEdit()
        self.search_input.setPlaceholderText("输入员工姓名或部门搜索...")
        self.search_input.textChanged.connect(self.load_data)
        filter_layout.addWidget(self.search_input)
        
        # 日期过滤
        filter_layout.addWidget(QLabel("开始日期:"))
        self.start_date_edit = QDateEdit(QDate.currentDate().addMonths(-1))
        self.start_date_edit.setCalendarPopup(True)
        self.start_date_edit.dateChanged.connect(self.load_data)
        filter_layout.addWidget(self.start_date_edit)
        
        filter_layout.addWidget(QLabel("结束日期:"))
        self.end_date_edit = QDateEdit(QDate.currentDate().addMonths(1))
        self.end_date_edit.setCalendarPopup(True)
        self.end_date_edit.dateChanged.connect(self.load_data)
        filter_layout.addWidget(self.end_date_edit)
        
        # 部门过滤
        self.dept_filter = QComboBox()
        self.dept_filter.addItem("所有部门", "")
        self.load_departments()
        self.dept_filter.currentIndexChanged.connect(self.load_data)
        filter_layout.addWidget(self.dept_filter)
        
        # 表格视图
        self.table_view = QTableView()
        self.table_view.setSelectionBehavior(QTableView.SelectRows)
        self.table_view.setSelectionMode(QTableView.SingleSelection)
        self.table_view.doubleClicked.connect(self.edit_record)
        
        # 设置表格模型
        self.model = QStandardItemModel()
        self.model.setHorizontalHeaderLabels(["ID", "员工姓名", "部门", "职位", "工作日期", "班次类型", "备注"])
        self.table_view.setModel(self.model)
        
        # 调整列宽
        self.table_view.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.table_view.setColumnHidden(0, True)  # 隐藏ID列
        
        self.list_layout.addWidget(self.table_view)
        
        # 按钮区域
        button_layout = QHBoxLayout()
        self.list_layout.addLayout(button_layout)
        
        # 添加按钮
        self.add_btn = QPushButton("添加排班")
        self.add_btn.clicked.connect(self.add_record)
        button_layout.addWidget(self.add_btn)
        
        # 编辑按钮
        self.edit_btn = QPushButton("编辑排班")
        self.edit_btn.clicked.connect(self.edit_record)
        button_layout.addWidget(self.edit_btn)
        
        # 删除按钮
        self.delete_btn = QPushButton("删除排班")
        self.delete_btn.clicked.connect(self.delete_record)
        button_layout.addWidget(self.delete_btn)
        
        # 刷新按钮
        self.refresh_btn = QPushButton("刷新数据")
        self.refresh_btn.clicked.connect(self.load_data)
        button_layout.addWidget(self.refresh_btn)

        # 批量添加按钮
        self.batch_add_btn = QPushButton("批量添加排班")
        self.batch_add_btn.clicked.connect(self.show_batch_add_dialog)
        button_layout.addWidget(self.batch_add_btn)

        # 批量删除按钮
        self.batch_delete_btn = QPushButton("批量删除")
        self.batch_delete_btn.clicked.connect(self.show_batch_delete_dialog)
        button_layout.addWidget(self.batch_delete_btn)        

    def show_calendar_context_menu(self, pos):
        """显示月历视图的右键菜单"""
        if self.is_calendar_view:
            table = self.sender()
            index = table.indexAt(pos)
            
            if index.isValid():
                # 获取日期数据
                item = table.item(index.row(), index.column())
                if item and item.data(Qt.UserRole):
                    date = item.data(Qt.UserRole)
                    date_str = date.toString("yyyy-MM-dd")
                    
                    # 创建菜单
                    menu = QMenu(self)
                    
                    # 添加排班
                    add_action = menu.addAction("添加排班")
                    add_action.triggered.connect(lambda: self.add_calendar_record(date_str))

                    # 批量添加排班
                    batch_add_action = menu.addAction("批量添加排班")
                    batch_add_action.triggered.connect(lambda: self.show_batch_add_dialog_for_date(date_str))


                    # 批量删除排班
                    batch_delete_action = menu.addAction("批量删除排班")
                    batch_delete_action.triggered.connect(lambda: self.show_batch_delete_dialog())

                    # 编辑/删除排班
                    try:
                        self.cursor.execute('''
                            SELECT id, employee_name, department, shift_type 
                            FROM schedules 
                            WHERE work_date = ?
                            ORDER BY department, employee_name
                        ''', (date_str,))
                        schedules = self.cursor.fetchall()
                        
                        if schedules:
                            # 添加分隔线
                            menu.addSeparator()
                            
                            # 为每个排班添加编辑和删除选项
                            for schedule in schedules:
                                sched_id, name, dept, shift = schedule
                                sub_menu = menu.addMenu(f"{name}({dept}): {shift}")
                                
                                # 编辑选项
                                edit_action = sub_menu.addAction("编辑")
                                edit_action.triggered.connect(lambda _, id=sched_id: self.edit_calendar_record(id))
                                
                                # 删除选项
                                delete_action = sub_menu.addAction("删除")
                                delete_action.triggered.connect(lambda _, id=sched_id: self.delete_calendar_record(id))

                    
                    except Error as e:
                        QMessageBox.critical(self, "数据库错误", f"无法查询排班数据:\n{str(e)}")
                        return
                    
                    # 添加刷新选项
                    menu.addSeparator()
                    refresh_action = menu.addAction("刷新数据")
                    refresh_action.triggered.connect(self.update_calendar_view)
                    
                    # 显示菜单
                    menu.exec_(table.viewport().mapToGlobal(pos))


    def add_calendar_record(self, date_str):
        """在月历视图中添加排班记录"""
        if not date_str:
            QMessageBox.warning(self, "错误", "无效日期")
            return
        dialog = ScheduleDialog(self)
        dialog.work_date.setDate(QDate.fromString(date_str, "yyyy-MM-dd"))
        if dialog.exec_() == QDialog.Accepted:
            try:
                data = dialog.get_data()
                # 更新最后选择的部门和班次类型
                ScheduleDialog.last_department = data[1]  # 部门是第二个元素
                ScheduleDialog.last_shift_type = data[4]  # 班次类型是第五个元素
                
                self.cursor.execute('''
                    INSERT INTO schedules 
                    (employee_name, department, position, work_date, shift_type, remarks)
                    VALUES (?, ?, ?, ?, ?, ?)
                ''', data)
                self.conn.commit()
                self.update_calendar_view()
                self.statusBar().showMessage("排班记录添加成功")
            except Error as e:
                QMessageBox.critical(self, "数据库错误", f"无法添加排班记录:\n{str(e)}")

    def edit_calendar_record(self, record_id):
        """在月历视图中编辑排班记录"""
        try:
            self.cursor.execute("SELECT * FROM schedules WHERE id = ?", (record_id,))
            record = self.cursor.fetchone()
            
            if record:
                dialog = ScheduleDialog(self, is_edit_mode=True)  # 设置为编辑模式
                dialog.set_data(record[1:])  # 跳过ID字段
                
                if dialog.exec_() == QDialog.Accepted:
                    data = dialog.get_data()
                    # 更新最后选择的部门和班次类型
                    ScheduleDialog.last_department = data[1]  # 部门是第二个元素
                    ScheduleDialog.last_shift_type = data[4]  # 班次类型是第五个元素
                    
                    # 添加ID到数据末尾用于WHERE条件
                    data = data + (record_id,)
                    self.cursor.execute('''
                        UPDATE schedules 
                        SET employee_name=?, department=?, position=?, work_date=?, shift_type=?, remarks=?
                        WHERE id=?
                    ''', data)
                    self.conn.commit()
                    self.update_calendar_view()
                    self.statusBar().showMessage("排班记录更新成功")
        except Error as e:
            QMessageBox.critical(self, "数据库错误", f"无法编辑排班记录:\n{str(e)}")


    def delete_calendar_record(self, record_id):
        """在月历视图中删除排班记录"""
        try:
            self.cursor.execute("SELECT employee_name, work_date FROM schedules WHERE id = ?", (record_id,))
            record = self.cursor.fetchone()
            
            if record:
                name, date = record
                reply = QMessageBox.question(
                    self, "确认删除",
                    f"确定要删除 {name} 在 {date} 的排班记录吗?",
                    QMessageBox.Yes | QMessageBox.No, QMessageBox.No
                )
                
                if reply == QMessageBox.Yes:
                    self.cursor.execute("DELETE FROM schedules WHERE id = ?", (record_id,))
                    self.conn.commit()
                    self.update_calendar_view()
                    self.statusBar().showMessage("排班记录删除成功")
        except Error as e:
            QMessageBox.critical(self, "数据库错误", f"无法删除排班记录:\n{str(e)}")










    def load_departments(self):
        """加载部门列表"""
        try:
            self.cursor.execute("SELECT DISTINCT department FROM schedules ORDER BY department")
            departments = self.cursor.fetchall()
            for dept in departments:
                self.dept_filter.addItem(dept[0], dept[0])
        except Error as e:
            QMessageBox.critical(self, "数据库错误", f"无法加载部门列表:\n{str(e)}")
    
    def load_data(self):
        """加载排班数据(列表视图)"""
        if self.is_calendar_view:
            return
            
        try:
            # 获取过滤条件
            search_text = self.search_input.text().strip()
            start_date = self.start_date_edit.date().toString("yyyy-MM-dd")
            end_date = self.end_date_edit.date().toString("yyyy-MM-dd")
            dept_filter = self.dept_filter.currentData()
            
            # 构建查询
            query = '''
                SELECT id, employee_name, department, position, work_date, shift_type, remarks 
                FROM schedules 
                WHERE work_date BETWEEN ? AND ?
            '''
            params = [start_date, end_date]
            
            # 添加搜索条件
            if search_text:
                query += " AND (employee_name LIKE ? OR department LIKE ?)"
                params.extend([f"%{search_text}%", f"%{search_text}%"])
            
            # 添加部门过滤
            if dept_filter:
                query += " AND department = ?"
                params.append(dept_filter)
            
            query += " ORDER BY work_date, department, employee_name"
            
            self.cursor.execute(query, params)
            records = self.cursor.fetchall()
            
            # 更新模型
            self.model.setRowCount(0)
        
            # 重置颜色映射（可选，如果希望每次加载都重新分配颜色）
            # self.name_color_map = {}
            
            for row_num, row_data in enumerate(records):
                self.model.insertRow(row_num)
                employee_name = str(row_data[1])  # 员工姓名在索引1的位置
                
                # 为每个姓名分配颜色（如果尚未分配）
                if employee_name not in self.name_color_map:
                    color_idx = len(self.name_color_map) % len(self.color_list)
                    self.name_color_map[employee_name] = self.color_list[color_idx]
            
                for col_num, col_data in enumerate(row_data):
                    item = QStandardItem(str(col_data))
                    item.setEditable(False)

                    # 设置背景色
                    if col_num in [1, 2, 3]:  # 姓名、部门、职位列
                        item.setBackground(self.name_color_map[employee_name])
                    
                    self.model.setItem(row_num, col_num, item)
            
            self.statusBar().showMessage(f"共加载 {len(records)} 条排班记录")
        except Error as e:
            QMessageBox.critical(self, "数据库错误", f"无法加载排班数据:\n{str(e)}")
    
    def add_record(self):
        """添加新排班记录"""
        dialog = ScheduleDialog(self)
        if dialog.exec_() == QDialog.Accepted:
            try:
                data = dialog.get_data()
                # 更新最后选择的部门和班次类型
                ScheduleDialog.last_department = data[1]  # 部门是第二个元素
                ScheduleDialog.last_shift_type = data[4]  # 班次类型是第五个元素
                
                self.cursor.execute('''
                    INSERT INTO schedules 
                    (employee_name, department, position, work_date, shift_type, remarks)
                    VALUES (?, ?, ?, ?, ?, ?)
                ''', data)
                self.conn.commit()
                if self.is_calendar_view:
                    self.update_calendar_view()
                else:
                    self.load_data()
                self.statusBar().showMessage("排班记录添加成功")
            except Error as e:
                QMessageBox.critical(self, "数据库错误", f"无法添加排班记录:\n{str(e)}")

    def edit_record(self):
        """编辑排班记录"""
        if self.is_calendar_view:
            # 在月历视图中不支持编辑
            QMessageBox.information(self, "提示", "请在列表视图中编辑排班记录")
            return
            
        selected = self.table_view.selectionModel().selectedRows()
        if not selected:
            QMessageBox.warning(self, "警告", "请先选择要编辑的排班记录")
            return
        
        row = selected[0].row()
        record_id = self.model.item(row, 0).text()
        
        try:
            self.cursor.execute("SELECT * FROM schedules WHERE id = ?", (record_id,))
            record = self.cursor.fetchone()
            
            if record:
                dialog = ScheduleDialog(self, is_edit_mode=True)  # 设置为编辑模式
                dialog.set_data(record[1:])  # 跳过ID字段
                if dialog.exec_() == QDialog.Accepted:
                    data = dialog.get_data()
                    # 更新最后选择的部门和班次类型
                    ScheduleDialog.last_department = data[1]  # 部门是第二个元素
                    ScheduleDialog.last_shift_type = data[4]  # 班次类型是第五个元素
                    
                    # 添加ID到数据末尾用于WHERE条件
                    data = data + (record_id,)
                    self.cursor.execute('''
                        UPDATE schedules 
                        SET employee_name=?, department=?, position=?, work_date=?, shift_type=?, remarks=?
                        WHERE id=?
                    ''', data)
                    self.conn.commit()
                    self.load_data()
                    self.statusBar().showMessage("排班记录更新成功")
        except Error as e:
            QMessageBox.critical(self, "数据库错误", f"无法编辑排班记录:\n{str(e)}")

    def delete_record(self):
        """删除排班记录"""
        if self.is_calendar_view:
            # 在月历视图中不支持删除
            QMessageBox.information(self, "提示", "请在列表视图中删除排班记录")
            return
            
        selected = self.table_view.selectionModel().selectedRows()
        if not selected:
            QMessageBox.warning(self, "警告", "请先选择要删除的排班记录")
            return
        
        row = selected[0].row()
        record_id = self.model.item(row, 0).text()
        employee_name = self.model.item(row, 1).text()
        work_date = self.model.item(row, 4).text()
        
        reply = QMessageBox.question(
            self, "确认删除",
            f"确定要删除 {employee_name} 在 {work_date} 的排班记录吗?",
            QMessageBox.Yes | QMessageBox.No, QMessageBox.No
        )
        
        if reply == QMessageBox.Yes:
            try:
                self.cursor.execute("DELETE FROM schedules WHERE id = ?", (record_id,))
                self.conn.commit()
                self.load_data()
                self.statusBar().showMessage("排班记录删除成功")
            except Error as e:
                QMessageBox.critical(self, "数据库错误", f"无法删除排班记录:\n{str(e)}")



    def closeEvent(self, event):
        """关闭窗口时保存所有设置并关闭数据库连接"""
        # 停止防抖定时器并强制保存所有设置
        self._settings_save_timer.stop()
        self._save_settings_now()

        self.conn.close()
        event.accept()

    def switch_user(self):
        """切换用户"""
        reply = QMessageBox.question(
            self, "切换用户", 
            "确定要切换用户吗？当前未保存的更改将会丢失。",
            QMessageBox.Yes | QMessageBox.No, QMessageBox.No
        )
        
        if reply == QMessageBox.Yes:
            # 关闭当前数据库连接
            self.conn.close()
            
            # 显示登录对话框
            if self.show_login_dialog():
                # 重新初始化数据库
                self.init_db()
                
                # 重新加载数据
                if self.is_calendar_view:
                    self.update_calendar_view()
                else:
                    self.load_data()
                
                # 更新窗口标题和按钮文本
                self.setWindowTitle(f"{ProjectInfo.NAME} {ProjectInfo.VERSION} - 当前用户: {self.current_user}")
                self.switch_user_btn.setText(f"切换用户 ({self.current_user})")
                self.statusBar().showMessage(f"已切换到用户: {self.current_user}")

    def toggle_two_year_view(self):
        """切换双年视图/单年视图"""
        # print("[DEBUG] 切换双年视图/单年视图")
        
        # 保存当前视图大小
        if self.current_view_type:
            setattr(self, f"{self.current_view_type}_size", self.size())
        
        # 切换视图状态
        self.show_two_years = not self.show_two_years
        
        # 确定目标视图类型和大小
        if self.show_two_years:
            self.two_year_btn.setText("显示单年视图")
            target_size = self.two_year_size if self.two_year_size else self.default_two_year_size
            self.current_view_type = 'two_year'
        else:
            self.two_year_btn.setText("显示双年视图")
            # 强制使用默认单年视图大小
            target_size = self.default_year_size  # 1000x800
            self.current_view_type = 'year'
        
        # 确保在年视图模式下
        if not self.show_year_view:
            self.show_year_view = True
            self.year_view_btn.setText("切换月视图")
        
        # 立即设置最小和最大尺寸，确保可以调整到目标大小
        self.setMinimumSize(target_size)
        self.setMaximumSize(target_size)
        
        # 立即调整窗口大小
        self.resize(target_size)
        
        # 延迟更新日历视图以确保布局完成
        from PyQt5.QtCore import QTimer
        QTimer.singleShot(100, self.update_calendar_view)
        
        # 重置最小和最大尺寸限制
        QTimer.singleShot(200, lambda: (
            self.setMinimumSize(0, 0),
            self.setMaximumSize(QWIDGETSIZE_MAX, QWIDGETSIZE_MAX)
        ))
        self._autosave_settings()







    def update_year_view(self):
        """更新年视图"""
        # print("[DEBUG] 更新年视图")
        # 设置标题
        self.month_label.setText(f"{self.current_year}年")
        
        # 创建4行3列的表格布局
        year_layout = QGridLayout()
        year_layout.setContentsMargins(0, 0, 0, 0)
        year_layout.setSpacing(10)
        
        # 添加12个月的日历
        for month in range(1, 13):
            month_date = QDate(self.current_year, month, 1)
            month_calendar = self.create_compact_calendar(month_date)
            row = (month - 1) // 3
            col = (month - 1) % 3
            year_layout.addWidget(month_calendar, row, col)
        
        # 将布局添加到容器中
        container = QWidget()
        container.setLayout(year_layout)
        self.calendar_layout.addWidget(container)

        # 如果没有设置过年视图大小，设置默认值
        if not self.year_size:
            self.year_size = QSize(1000, 800)  # 默认年视图大小
            print("[DEBUG] 设置默认年视图大小")

    def create_compact_calendar(self, date):
        """创建紧凑型月历(用于年视图)"""
        # print(f"[DEBUG] 创建紧凑型月历: {date.toString('yyyy-MM')}")
        # 创建容器
        container = QWidget()
        container.setFixedSize(300, 200)
        layout = QVBoxLayout(container)
        layout.setContentsMargins(5, 5, 5, 5)
        
        # 添加月份标题
        month_label = QLabel(f"{date.month()}月")
        month_label.setAlignment(Qt.AlignCenter)
        month_label.setStyleSheet("font-weight: bold;")
        layout.addWidget(month_label)
        
        # 创建紧凑日历表格
        table = QTableWidget()
        table.setEditTriggers(QTableWidget.NoEditTriggers)
        table.setSelectionMode(QTableWidget.NoSelection)
        table.setColumnCount(7)
        table.setHorizontalHeaderLabels(["日", "一", "二", "三", "四", "五", "六"])
        
        # 设置表格样式
        table.setStyleSheet("""
            QTableWidget {
                border: none;
                font-size: 10px;
            }
            QHeaderView::section {
                font-size: 10px;
                padding: 2px;
            }
        """)
        
        # 计算当月天数
        month_days = date.daysInMonth()
        first_day = QDate(date.year(), date.month(), 1)
        start_day = first_day.dayOfWeek() % 7
        
        # 计算需要的行数
        rows = ((start_day + month_days - 1) // 7) + 1
        table.setRowCount(rows)
        
        # 预先加载本月所有排班数据以确定颜色分配
        start_date = QDate(date.year(), date.month(), 1)
        end_date = QDate(date.year(), date.month(), month_days)
        
        try:
            self.cursor.execute('''
                SELECT DISTINCT employee_name 
                FROM schedules 
                WHERE work_date BETWEEN ? AND ?
                ORDER BY employee_name
            ''', (start_date.toString("yyyy-MM-dd"), end_date.toString("yyyy-MM-dd")))
            employees = self.cursor.fetchall()
            
            # 为每个员工分配颜色
            for emp in employees:
                name = emp[0]
                if name not in self.name_color_map:
                    color_idx = len(self.name_color_map) % len(self.color_list)
                    self.name_color_map[name] = self.color_list[color_idx]
        except Error as e:
            QMessageBox.critical(self, "数据库错误", f"无法加载员工列表:\n{str(e)}")
            return container
        
        # 填充日期
        for day in range(1, month_days + 1):
            current_date = QDate(date.year(), date.month(), day)
            day_of_week = current_date.dayOfWeek() % 7
            row = (start_day + day - 1) // 7
            
            # 创建日期单元格并设置日期文本
            item = QTableWidgetItem(str(day))
            item.setTextAlignment(Qt.AlignCenter)

            # 设置无排班日期的字体大小
            no_schedule_font_size = self.settings.value("calendar/no_schedule_font_size", 12, int)
            item.setFont(QFont("", no_schedule_font_size))

            # 设置周末颜色
            if day_of_week == 0 or day_of_week == 6:
                item.setForeground(QColor(255, 0, 0))
            
            table.setItem(row, day_of_week, item)
            
            # 加载当天的排班数据
            try:
                date_str = current_date.toString("yyyy-MM-dd")
                self.cursor.execute('''
                    SELECT employee_name, shift_type 
                    FROM schedules 
                    WHERE work_date = ?
                    ORDER BY employee_name
                    LIMIT 2
                ''', (date_str,))
                schedules = self.cursor.fetchall()
                
                if schedules:
                    # 获取第一个员工的颜色作为背景色
                    first_name = schedules[0][0]
                    bg_color = self.name_color_map.get(first_name, QColor(255, 255, 255))
                    
                    # 设置背景色
                    item.setBackground(bg_color)
                
                    # 创建显示内容的文本
                    text = ""
                    for i, (name, shift) in enumerate(schedules[:2]):  # 最多显示两个
                        color = self.name_color_map.get(name, QColor(255, 255, 255))
                        text += f"<span style='color:{color.name()};'>{name[:1]}</span>"  # 只显示姓名首字母
                    
                    # 创建标签显示内容
                    label = QLabel(text)
                    label.setAlignment(Qt.AlignCenter)
                    table.setCellWidget(row, day_of_week, label)
            except Error as e:
                print(f"加载排班数据出错: {str(e)}")
        
        # 调整列宽和行高
        table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        for col in range(table.columnCount()):
            table.setColumnWidth(col, 30)
        for row in range(table.rowCount()):
            table.setRowHeight(row, 20)
        
        layout.addWidget(table)
        
        # 添加右键菜单
        table.setContextMenuPolicy(Qt.CustomContextMenu)
        table.customContextMenuRequested.connect(lambda pos: self.show_month_context_menu(pos, date))
        
        return container






    def update_two_year_view(self):
        """更新双年视图"""
        # print("[DEBUG] 更新双年视图")
        # 如果没有设置过双年视图大小，设置一个默认值
        if not self.two_year_size:
            self.two_year_size = QSize(1200, 800)  # 默认双年视图大小
        
        # 设置标题
        self.month_label.setText(f"{self.current_year}-{self.current_year+1}年")
        
        # 创建水平布局用于两个年份
        two_year_layout = QHBoxLayout()
        two_year_layout.setContentsMargins(0, 0, 0, 0)
        two_year_layout.setSpacing(20)
        
        # 添加当前年
        current_year_widget = self.create_year_widget(self.current_year)
        two_year_layout.addWidget(current_year_widget)
        
        # 添加下一年
        next_year_widget = self.create_year_widget(self.current_year + 1)
        two_year_layout.addWidget(next_year_widget)
        
        # 将布局添加到容器中
        container = QWidget()
        container.setLayout(two_year_layout)
        self.calendar_layout.addWidget(container)


    def create_year_widget(self, year):
        """创建单个年份的小部件"""
        container = QWidget()
        layout = QVBoxLayout(container)
        layout.setContentsMargins(0, 0, 0, 0)
        
        # 添加年份标题
        year_label = QLabel(f"{year}年")
        year_label.setAlignment(Qt.AlignCenter)
        year_label.setStyleSheet("font-weight: bold;")
        layout.addWidget(year_label)
        
        # 创建4行3列的月份网格
        grid = QGridLayout()
        grid.setSpacing(5)
        
        for month in range(1, 13):
            month_date = QDate(year, month, 1)
            month_calendar = self.create_compact_calendar(month_date)
            row = (month - 1) // 3
            col = (month - 1) % 3
            grid.addWidget(month_calendar, row, col)
        
        layout.addLayout(grid)
        return container

    def show_month_context_menu(self, pos, date):
        """显示月份的右键菜单"""
        table = self.sender()
        index = table.indexAt(pos)
        
        if index.isValid():
            # 创建菜单
            menu = QMenu(self)
            
            # 查看完整月份
            view_action = menu.addAction(f"查看{date.month()}月详细排班")
            view_action.triggered.connect(lambda: self.view_month_detail(date))
            
            # 显示菜单
            menu.exec_(table.viewport().mapToGlobal(pos))

    def view_month_detail(self, date):
        """查看月份详细排班"""
        print(f"[DEBUG] 查看{date.month()}月详细排班")
        # 保存当前视图状态
        old_two_months = self.show_two_months
        old_two_years = self.show_two_years
        old_year_view = self.show_year_view
        
        # 切换到单月视图
        self.show_two_months = False
        self.show_two_years = False
        self.show_year_view = False
        self.current_date = date
        
        # 更新按钮状态
        self.two_month_btn.setChecked(False)
        self.two_year_btn.setChecked(False)
        self.year_view_btn.setChecked(False)
        
        # 更新视图
        self.update_calendar_view()
        
        # 恢复按钮文本
        self.two_month_btn.setText("显示两个月")
        self.two_year_btn.setText("显示双年视图")
        self.year_view_btn.setText("切换年视图")
        self._autosave_settings()

    def toggle_year_view(self):
        """切换年视图/月视图"""
        # print("[DEBUG] 切换年视图/月视图")
        
        # 保存当前视图大小
        if self.current_view_type:
            setattr(self, f"{self.current_view_type}_size", self.size())
        
        # 切换视图状态
        self.show_year_view = not self.show_year_view
        
        # 确定目标视图类型和大小
        if self.show_year_view:
            self.year_view_btn.setText("切换月视图")
            if self.show_two_years:
                target_size = self.two_year_size if self.two_year_size else self.default_two_year_size
                self.current_view_type = 'two_year'
            else:
                target_size = self.year_size if self.year_size else self.default_year_size
                self.current_view_type = 'year'
        else:
            self.year_view_btn.setText("切换年视图")
            target_size = self.month_view_size if self.month_view_size else self.default_month_size
            self.current_view_type = 'month'
            self.show_two_years = False
            self.two_year_btn.setText("显示双年视图")
        
        # 确保target_size不为None
        #if target_size is None:
        #    if self.show_year_view:
        #        target_size = self.default_two_year_size if self.show_two_years else self.default_year_size
        #    else:
        #        target_size = self.default_month_size
        
        # 延迟调整大小以确保布局完成
        from PyQt5.QtCore import QTimer
        QTimer.singleShot(100, lambda: self.resize(target_size))
        
        self.update_calendar_view()
        self._autosave_settings()


    def resizeEvent(self, event):
        """重写resizeEvent来捕获窗口大小变化"""
        super().resizeEvent(event)
        # print("[DEBUG] 窗口大小变化事件触发")
        
        # 只在视图显示且不是最小化时保存大小
        if self.isVisible() and not self.isMinimized() and self.current_view_type:
            setattr(self, f"{self.current_view_type}_size", self.size())
            # print(f"[DEBUG] 保存{self.current_view_type}视图大小: {self.size().width()}x{self.size().height()}")
            self._autosave_settings()

    def show_batch_add_dialog(self):
        """显示批量添加对话框"""
        dialog = BatchAddDialog(self)
        if dialog.exec_() == QDialog.Accepted:
            try:
                for data in dialog.get_schedule_data():
                    self.cursor.execute('''
                        INSERT INTO schedules 
                        (employee_name, department, position, work_date, shift_type, remarks)
                        VALUES (?, ?, ?, ?, ?, ?)
                    ''', data)
                self.conn.commit()
                if self.is_calendar_view:
                    self.update_calendar_view()
                else:
                    self.load_data()
                self.statusBar().showMessage(f"批量添加完成，共添加 {len(dialog.get_schedule_data())} 条排班记录")
            except Error as e:
                QMessageBox.critical(self, "数据库错误", f"批量添加排班记录失败:\n{str(e)}")

    def show_batch_add_dialog_for_date(self, date_str):
        """显示预填日期的批量添加对话框"""
        dialog = BatchAddDialog(self)
        # 设置日期为不连续模式并添加当前日期
        dialog.date_mode.setCurrentIndex(1)
        dialog.date_list.addItem(date_str)
        if dialog.exec_() == QDialog.Accepted:
            try:
                for data in dialog.get_schedule_data():
                    self.cursor.execute('''
                        INSERT INTO schedules 
                        (employee_name, department, position, work_date, shift_type, remarks)
                        VALUES (?, ?, ?, ?, ?, ?)
                    ''', data)
                self.conn.commit()
                self.update_calendar_view()
                self.statusBar().showMessage(f"批量添加完成，共添加 {len(dialog.get_schedule_data())} 条排班记录")
            except Error as e:
                QMessageBox.critical(self, "数据库错误", f"批量添加排班记录失败:\n{str(e)}")


    def show_batch_delete_dialog(self):
        """显示批量删除对话框 - 直接显示所有排班记录"""
        try:
            # 获取所有排班数据
            self.cursor.execute('''
                SELECT id, employee_name, department, position, work_date, shift_type, remarks 
                FROM schedules 
                ORDER BY work_date, department, employee_name
            ''')
            schedules = self.cursor.fetchall()
            
            if not schedules:
                QMessageBox.information(self, "提示", "当前没有排班记录")
                return
                
            dialog = BatchDeleteDialog(self, schedules)
            dialog.original_schedules = schedules  # 确保原始数据被存储
        
            # 修改按钮样式设置 - 直接使用颜色字符串而不是调用.name()
            button_box = dialog.findChild(QDialogButtonBox)
            if button_box:
                button_box.button(QDialogButtonBox.Ok).setStyleSheet(
                    f"background-color: {MacaronColors.MINT_GREEN.name()}; color: black;")
                button_box.button(QDialogButtonBox.Cancel).setStyleSheet(
                    f"background-color: {MacaronColors.ROSE_PINK.name()}; color: black;")
        
            if dialog.exec_() == QDialog.Accepted:
                selected_ids = dialog.get_selected_ids()
                if not selected_ids:
                    QMessageBox.warning(self, "警告", "请选择要删除的记录")
                    return
                    
                reply = QMessageBox.question(
                    self, "确认删除",
                    f"确定要删除选中的 {len(selected_ids)} 条排班记录吗?",
                    QMessageBox.Yes | QMessageBox.No, QMessageBox.No
                )
                
                if reply == QMessageBox.Yes:
                    self.cursor.executemany(
                        "DELETE FROM schedules WHERE id = ?",
                        [(id,) for id in selected_ids]
                    )
                    self.conn.commit()
                    if self.is_calendar_view:
                        self.update_calendar_view()
                    else:
                        self.load_data()
                    self.statusBar().showMessage(f"批量删除完成，共删除 {len(selected_ids)} 条排班记录")
        except Error as e:
            QMessageBox.critical(self, "数据库错误", f"批量删除排班记录失败:\n{str(e)}")


    def get_selected_dates_from_calendar(self, table):
        """从日历表格中获取选中的日期"""
        selected_dates = []
        for item in table.selectedItems():
            date = item.data(Qt.UserRole)
            if date and date.isValid():
                selected_dates.append(date.toString("yyyy-MM-dd"))
        return selected_dates

    def set_button_styles(self):
        """设置所有按钮的马卡龙风格样式"""
        # 导航按钮 - 天空蓝
        nav_style = f"background-color: {MacaronColors.SKY_BLUE.name()}; color: black;"
        self.prev_month_btn.setStyleSheet(nav_style)
        self.next_month_btn.setStyleSheet(nav_style)

        # 显示模式切换按钮 - 开心果绿
        self.time_block_btn.setStyleSheet(f"background-color: {MacaronColors.PISTACHIO.name()}; color: black;")

        # 视图切换按钮 - 薰衣草紫
        view_style = f"background-color: {MacaronColors.LAVENDER.name()}; color: black;"
        self.view_toggle_btn.setStyleSheet(view_style)
        self.two_month_btn.setStyleSheet(view_style)
        self.year_view_btn.setStyleSheet(view_style)
        self.two_year_btn.setStyleSheet(view_style)
        
        # 配置按钮 - 香芋紫
        self.calendar_config_btn.setStyleSheet(f"background-color: {MacaronColors.TARO_PURPLE.name()}; color: white;")
        
        # 用户按钮 - 蜜桃橙
        self.switch_user_btn.setStyleSheet(f"background-color: {MacaronColors.PEACH_ORANGE.name()}; color: black;")
        
        # 列表视图操作按钮 - 不同马卡龙颜色区分功能
        self.add_btn.setStyleSheet(f"background-color: {MacaronColors.MINT_GREEN.name()}; color: black;")  # 薄荷绿
        self.edit_btn.setStyleSheet(f"background-color: {MacaronColors.LEMON_YELLOW.name()}; color: black;")  # 柠檬黄
        self.delete_btn.setStyleSheet(f"background-color: {MacaronColors.ROSE_PINK.name()}; color: black;")  # 玫瑰粉
        self.refresh_btn.setStyleSheet(f"background-color: {MacaronColors.LILAC_MIST.name()}; color: black;")  # 淡丁香
        self.batch_add_btn.setStyleSheet(f"background-color: {MacaronColors.APPLE_GREEN.name()}; color: black;")  # 苹果绿
        self.batch_delete_btn.setStyleSheet(f"background-color: {MacaronColors.SAKURA_PINK.name()}; color: black;")  # 樱花粉

    def show_modify_username_dialog(self, parent_dialog):
        """显示修改用户名对话框"""
        dialog = QDialog(parent_dialog)
        dialog.setWindowTitle("修改用户名")
        dialog.setWindowIcon(QIcon('icon.ico'))
        dialog.resize(300, 200)
        
        layout = QFormLayout(dialog)
        
        # 原用户名 - 改为下拉菜单
        old_username_combo = QComboBox()
        try:
            conn = sqlite3.connect(UserManager.USERS_DB)
            cursor = conn.cursor()
            cursor.execute("SELECT username FROM users ORDER BY username")
            users = cursor.fetchall()
            
            for user in users:
                old_username_combo.addItem(user[0])
        except Error as e:
            QMessageBox.critical(dialog, "错误", f"无法加载用户列表: {str(e)}")
            return
        finally:
            if 'conn' in locals():
                conn.close()
        
        layout.addRow("选择用户:", old_username_combo)
        
        # 新用户名
        new_username = QLineEdit()
        new_username.setPlaceholderText("输入新用户名")
        layout.addRow("新用户名:", new_username)
        
        # 密码验证
        password_input = QLineEdit()
        password_input.setPlaceholderText("输入密码验证(如有)")
        password_input.setEchoMode(QLineEdit.Password)
        layout.addRow("密码验证:", password_input)
        
        # 按钮
        button_box = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel)
        button_box.accepted.connect(lambda: self.handle_modify_username(
            dialog, old_username_combo.currentText(), new_username.text(), password_input.text()
        ))
        button_box.rejected.connect(dialog.reject)
        layout.addRow(button_box)
        
        # 设置按钮样式
        button_box.button(QDialogButtonBox.Ok).setStyleSheet(
            f"background-color: {MacaronColors.MINT_GREEN.name()}; color: black;")
        button_box.button(QDialogButtonBox.Cancel).setStyleSheet(
            f"background-color: {MacaronColors.ROSE_PINK.name()}; color: black;")
        
        dialog.exec_()


    def handle_modify_username(self, dialog, old_username, new_username, password):
        """处理修改用户名请求"""
        if not old_username or not new_username:
            QMessageBox.warning(dialog, "输入错误", "原用户名和新用户名不能为空")
            return
            
        if old_username == new_username:
            QMessageBox.warning(dialog, "输入错误", "新用户名不能与原用户名相同")
            return
            
        try:
            if UserManager.update_username(old_username, new_username, password):
                QMessageBox.information(dialog, "成功", "用户名修改成功")
                # 刷新用户列表
                self.load_registered_users()
                
                # 如果修改的是当前登录用户，更新界面显示
                if self.username_combo.currentText() == old_username:
                    self.username_combo.setCurrentText(new_username)
                    
                dialog.accept()
        except Exception as e:
            QMessageBox.critical(dialog, "错误", f"修改用户名失败: {str(e)}")

    def manual_backup(self):
        """手动备份数据库"""
        try:
            backup_file = UserManager.backup_db(self.user_db_file, "manual")
            QMessageBox.information(self, "备份成功", f"数据库已备份到:\n{backup_file}")
        except Exception as e:
            QMessageBox.critical(self, "备份失败", f"备份数据库时出错:\n{str(e)}")

    def show_restore_dialog(self):
        """显示恢复备份对话框"""
        try:
            backups = UserManager.get_backups(self.user_db_file)
            if not backups:
                QMessageBox.information(self, "无备份", "没有找到任何备份文件")
                return
            
            dialog = QDialog(self)
            dialog.setWindowTitle("恢复备份")
            dialog.resize(600, 400)
            
            layout = QVBoxLayout()
            dialog.setLayout(layout)
            
            # 备份列表表格
            table = QTableWidget()
            table.setColumnCount(4)
            table.setHorizontalHeaderLabels(["备份时间", "备份类型", "大小(MB)", "操作"])
            table.setSelectionBehavior(QTableView.SelectRows)
            
            # 填充备份数据
            table.setRowCount(len(backups))
            for row, backup in enumerate(backups):
                # 备份时间
                time_item = QTableWidgetItem(backup["date"].strftime("%Y-%m-%d %H:%M:%S"))
                time_item.setData(Qt.UserRole, backup["path"])  # 存储完整路径
                
                # 备份类型
                backup_type = backup["type"]
                display_text = {
                    "auto": "自动",
                    "manual": "手动", 
                    "rollback": "回滚",
                }.get(backup_type, "未知")  # 添加更多类型映射
                type_item = QTableWidgetItem(display_text)
                # type_item = QTableWidgetItem("自动" if backup["type"] == "auto" else "手动")
                # 添加调试信息
                print(f"[DEBUG] 备份类型处理 - 原始类型: {backup['type']}, 显示文本: {type_item.text()}")
                print(f"[DEBUG] 备份详情 - 路径: {backup['path']}, 大小: {backup['size']} 字节, 日期: {backup['date']}")
                
                
                # 备份大小
                size_mb = backup["size"] / (1024 * 1024)
                size_item = QTableWidgetItem(f"{size_mb:.2f}")
                
                table.setItem(row, 0, time_item)
                table.setItem(row, 1, type_item)
                table.setItem(row, 2, size_item)
                
                # 恢复按钮
                restore_btn = QPushButton("恢复")
                restore_btn.clicked.connect(lambda _, path=backup["path"]: self.restore_backup(path, dialog))
                table.setCellWidget(row, 3, restore_btn)

                
            
            # 调整列宽
            table.horizontalHeader().setSectionResizeMode(0, QHeaderView.Stretch)
            table.horizontalHeader().setSectionResizeMode(1, QHeaderView.ResizeToContents)
            table.horizontalHeader().setSectionResizeMode(2, QHeaderView.ResizeToContents)
            table.horizontalHeader().setSectionResizeMode(3, QHeaderView.ResizeToContents)
            
            layout.addWidget(table)
            
            # 关闭按钮
            close_btn = QPushButton("关闭")
            close_btn.clicked.connect(dialog.reject)
            layout.addWidget(close_btn)
            
            dialog.exec_()
        except Exception as e:
            QMessageBox.critical(self, "错误", f"获取备份列表失败:\n{str(e)}")

    def restore_backup(self, backup_file, dialog):
        """从备份恢复数据库"""
        try:
            reply = QMessageBox.question(
                self, "确认恢复",
                "确定要从该备份恢复数据库吗？当前数据将被覆盖。",
                QMessageBox.Yes | QMessageBox.No, QMessageBox.No
            )
            
            if reply == QMessageBox.Yes:
                # 先创建回滚备份
                rollback_file = UserManager.restore_db(self.user_db_file, backup_file)
                
                # 重新连接数据库
                self.conn.close()
                self.init_db()
                
                # 重新加载数据
                if self.is_calendar_view:
                    self.update_calendar_view()
                else:
                    self.load_data()
                
                QMessageBox.information(
                    self, "恢复成功", 
                    f"数据库已从备份恢复。\n\n"
                    f"原数据已备份到:\n{rollback_file}\n\n"
                    f"如需回滚，请使用此备份文件。"
                )
                dialog.accept()
        except Exception as e:
            QMessageBox.critical(self, "恢复失败", f"恢复数据库时出错:\n{str(e)}")

    def toggle_time_block_view(self):
        """切换时间段区块显示模式"""
        self.show_time_block_view = not self.show_time_block_view
        self.time_block_btn.setChecked(self.show_time_block_view)
        self.time_block_btn.setText("时间显示: " + ("区块" if self.show_time_block_view else "文本")) 
        self.update_calendar_view()
        self._autosave_settings()

    def load_day_schedules_time_block(self, table, row, col, date):
        """使用时间段区块模式加载某一天的排班数据"""
        try:
            date_str = date.toString("yyyy-MM-dd")
            self.cursor.execute('''
                SELECT employee_name, department, shift_type, 
                    (SELECT start_time FROM custom_shifts WHERE shift_name = schedules.shift_type) as start_time_str,
                    (SELECT end_time FROM custom_shifts WHERE shift_name = schedules.shift_type) as end_time_str
                FROM schedules 
                WHERE work_date = ?
                ORDER BY department, employee_name
            ''', (date_str,))
            schedules = self.cursor.fetchall()
            
            # 创建容器小部件
            container = QWidget()
            layout = QVBoxLayout(container)
            layout.setContentsMargins(0, 0, 0, 0)
            layout.setSpacing(0)
            
            # 添加日期标签 - 总是显示日期
            date_label = QLabel(str(date.day()))
            date_label.setAlignment(Qt.AlignTop | Qt.AlignLeft)
            date_label.setMargin(2)
            # 应用区块视图日期字体大小
            date_font_size = self.settings.value("calendar/time_block_date_font_size", 12, int)
            date_label.setStyleSheet(f"font-size: {date_font_size}px;")
            layout.addWidget(date_label)
            
            if schedules:
                # 根据员工数量确定布局方式
                num_employees = len(schedules)
                if num_employees <= 2:
                    grid = QHBoxLayout()
                else:
                    grid = QGridLayout()
                
                # 为每个时间段创建区块
                colors = [color.name() for color in self.color_list]
                
                for i, (name, dept, shift, start_time, end_time) in enumerate(schedules):
                    # 获取或分配颜色
                    if name not in self.name_color_map:
                        self.name_color_map[name] = self.color_list[len(self.name_color_map) % len(self.color_list)]
                    color = self.name_color_map[name].name()
                    
                    # 格式化时间段显示
                    time_range = ""
                    if start_time and end_time:
                        try:
                            start_hour = int(start_time.split(':')[0])
                            end_hour = int(end_time.split(':')[0])
                            time_range = f"{start_hour}:00-{end_hour}:00"
                        except (ValueError, AttributeError):
                            time_range = shift  # 如果时间格式无效，显示班次名称
                    
                    # 创建时间段区块
                    content_font_size = self.settings.value("calendar/time_block_content_font_size", 9, int)
                    block = QLabel(f"{name}\n{time_range}")
                    block.setAlignment(Qt.AlignCenter)
                    block.setStyleSheet(f'''
                        background-color: {color};
                        margin: 1px;
                        padding: 2px;
                        border-radius: 3px;
                        font-size: {content_font_size}px;
                    ''')
                    
                    # 添加到网格布局
                    if num_employees <= 2:
                        grid.addWidget(block)
                    elif num_employees <= 4:
                        grid.addWidget(block, i // 2, i % 2)
                    else:
                        grid.addWidget(block, i // 2, i % 2)
                
                layout.addLayout(grid)
            
            table.setCellWidget(row, col, container)
            
        except Error as e:
            QMessageBox.critical(self, "数据库错误", f"无法加载排班数据:\n{str(e)}")

    def update_shifts_in_ui(self):
        """更新UI中的所有班次下拉框"""
        try:
            self.cursor.execute("SELECT shift_name || ' (' || start_time || '-' || end_time || ')' FROM custom_shifts ORDER BY shift_name")
            shifts = self.cursor.fetchall()
            shift_items = [shift[0] for shift in shifts]
            
            # 更新ScheduleDialog中的下拉框
            for widget in self.findChildren(ScheduleDialog):
                widget.shift_type.clear()
                widget.shift_type.addItems(shift_items)
                
                # 恢复最后选择的班次类型
                if ScheduleDialog.last_shift_type:
                    index = widget.shift_type.findText(ScheduleDialog.last_shift_type)
                    if index >= 0:
                        widget.shift_type.setCurrentIndex(index)
                    else:
                        widget.shift_type.setCurrentText(ScheduleDialog.last_shift_type)
            
            # 更新BatchAddDialog中的下拉框
            for widget in self.findChildren(BatchAddDialog):
                widget.shift_type.clear()
                widget.shift_type.addItems(shift_items)
                
        except Error as e:
            QMessageBox.critical(self, "数据库错误", f"无法更新班次列表:\n{str(e)}")


if __name__ == "__main__":
    app = QApplication(sys.argv)
    
    # 设置中文字体
    font = app.font()
    font.setFamily("Microsoft YaHei")
    app.setFont(font)
    
    try:
        window = ScheduleManager()
        # 按保存的最大化状态显示窗口
        if window._start_maximized:
            window.showMaximized()
        else:
            window.show()
        sys.exit(app.exec_())
    except Exception as e:
        print(f"[DEBUG] 应用程序启动失败: {str(e)}")
        QMessageBox.critical(None, "错误", f"应用程序启动失败: {str(e)}")
        sys.exit(1)