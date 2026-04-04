import re
import os
import jieba
from html import unescape
from src.config.conf import PROJECT_DIR

protected_words = [
    'http', 'https', 'ftp', 'tcp', 'file',
    'url', 'email', 'www'
]

stopwords = {
    # 助词/结构助词
    "的", "得", "地", "之", "所",

    # 连词
    "和", "与", "及", "或", "且", "而", "并", "但是", "然而", "可是", "不过",

    # 介词
    "在", "于", "向", "从", "对", "对于", "关于", "为", "为了", "由于", "因为", "被", "把", "将", "给",

    # 副词
    "也", "又", "再", "才", "就", "都", "只", "还", "更", "最", "很", "太", "极", "挺", "非常", "十分", "格外",

    # 代词
    "我", "你", "他", "她", "它", "我们", "你们", "他们", "她们", "它们", "这", "那", "这些", "那些", "此", "彼", "其", "自己", "本身",

    # 语气词
    "吗", "呢", "吧", "啊", "呀", "哒", "喽", "呗", "罢了", "而已",

    # 数量词相关
    "个", "只", "条", "件", "本", "张", "辆", "台", "片", "些", "点", "种", "样", "次", "回", "遍",

    # 其他常见无意义词汇
    "是", "有", "无", "存在", "没有", "可以", "能够", "会", "要", "应", "应该", "必须", "可能", "也许", "大概", "大约",
    "就是", "只是", "可是", "不过", "其实", "究竟", "到底", "反正", "横竖", "索性", "偏偏", "明明", "恰恰", "刚好",
    "刚才", "刚刚", "已经", "曾经", "正在", "将要", "即将", "终于", "忽然", "突然", "渐渐", "慢慢", "悄悄", "默默",
    "亲自", "亲身", "特地", "特意", "故意", "特意", "顺便", "附带", "另外", "此外", "还有", "况且", "何况", "加之",
    "包括", "包含", "例如", "比如", "诸如", "像", "如", "似", "仿佛", "犹如", "如同", "等于", "属于", "归于", "成为",
    "变成", "化为", "当作", "作为", "叫做", "称为", "认为", "以为", "觉得", "感到", "看来", "看起来", "闻起来", "听起来",
    "总之", "总而言之", "综上所述", "由此可见", "因此", "因而", "所以", "故此", "故而", "于是", "从而", "进而", "反而", "反之"
}

for word in protected_words:
    jieba.add_word(word)


def clean_text(text: str) -> str:
    if not text:
        return ""

    text = re.sub(r'<[^>]+>', '', text)

    text = unescape(text)

    # 1. 先去除干扰信息（URL、Email）
    text = re.sub(r"(https?|ftp|file)://[^\s]+", "", text)
    text = re.sub(r"[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-za-z]{2,}", "", text)

    # 2. 保留中英文和数字，将其他特殊符号替换为空格
    pattern = re.compile(r'[^\u4e00-\u9fa5a-zA-Z0-9]')
    cleaned_text = pattern.sub(' ', text)

    # 3. 合并多余空格并去除首尾空格（不要把中间空格全删了，留给 Jieba 识别）
    cleaned_text = re.sub(r'\s+', ' ', cleaned_text).strip()

    return cleaned_text


def to_query(text: str, mode: str = 'search'):
    cleaned_text = clean_text(text)
    words = None

    if mode == "full":
        words = jieba.lcut(cleaned_text, cut_all=True)
    elif mode == "exact":
        words = jieba.lcut(cleaned_text, cut_all=False)
    else:
        words = jieba.cut_for_search(cleaned_text)

    filtered_words = [word for word in words if word not in stopwords]
    result = " | ".join(filtered_words)
    return result
