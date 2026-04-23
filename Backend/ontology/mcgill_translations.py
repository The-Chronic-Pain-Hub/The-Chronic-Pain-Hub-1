"""
McGill Pain Questionnaire - Multilingual Translations

Standard McGill pain descriptors translated into Chinese, Korean, Spanish, and Hmong.
These translations are INDEPENDENT from the system's multilingual_pain_data.json dictionary.

**Purpose:** 
Auxiliary semantic matching when system dictionary doesn't have a match.
Uses BioLORD for same-language medical semantic understanding.

**Architecture:**
Chinese patient "蚂蚁爬" → BioLORD → Chinese McGill "蚁爬感" → English "formication"
Korean patient "개미 감각" → BioLORD → Korean McGill "개미가 기어가는 느낌" → English "formication"

**McGill Standard Reference:** 
Melzack, R. (1975). The McGill Pain Questionnaire: Major properties and scoring methods.
"""

# Chinese McGill Pain Descriptors (中文麦吉尔疼痛问卷)
CHINESE_MCGILL = {
    # Sensory - Neuropathic (神经性疼痛)
    "灼烧感": {"english": "burning", "type": "neuropathic", "dimension": "sensory",
               "aliases": ["火烧火燎", "灼热感", "烧灼感", "火辣辣的疼", "辣的疼"]},
    "刺痛": {"english": "tingling", "type": "neuropathic", "dimension": "sensory"},
    "麻木": {"english": "numbness", "type": "neuropathic", "dimension": "sensory"},
    "蚁爬感": {"english": "formication", "type": "neuropathic", "dimension": "sensory", 
               "aliases": ["蚂蚁爬", "像蚂蚁在爬", "虫爬感"]},
    "针刺感": {"english": "pins and needles", "type": "neuropathic", "dimension": "sensory",
               "aliases": ["针扎感", "针刺样"]},
    "电击感": {"english": "electric shock", "type": "neuropathic", "dimension": "sensory",
               "aliases": ["电击样", "像电击一样", "触电感"]},
    "放射痛": {"english": "shooting", "type": "neuropathic", "dimension": "sensory"},
    "刀刺样痛": {"english": "stabbing", "type": "neuropathic", "dimension": "sensory"},
    "锐痛": {"english": "sharp", "type": "neuropathic", "dimension": "sensory"},
    "穿刺样痛": {"english": "piercing", "type": "neuropathic", "dimension": "sensory"},
    "蛰刺感": {"english": "stinging", "type": "neuropathic", "dimension": "sensory",
               "aliases": ["蚊虫叮咬样", "刺痒感"]},
    
    # Sensory - Nociceptive (伤害性疼痛)
    "酸痛": {"english": "aching", "type": "nociceptive", "dimension": "sensory"},
    "跳痛": {"english": "throbbing", "type": "nociceptive", "dimension": "sensory",
             "aliases": ["搏动性疼痛", "一跳一跳疼"]},
    "捶击样痛": {"english": "pounding", "type": "nociceptive", "dimension": "sensory"},
    "敲打样痛": {"english": "beating", "type": "nociceptive", "dimension": "sensory"},
    "脉冲样痛": {"english": "pulsing", "type": "nociceptive", "dimension": "sensory"},
    "绞痛": {"english": "cramping", "type": "nociceptive", "dimension": "sensory",
             "aliases": ["痉挛性疼痛"]},
    "啃咬样痛": {"english": "gnawing", "type": "nociceptive", "dimension": "sensory"},
    "压榨样痛": {"english": "crushing", "type": "nociceptive", "dimension": "sensory",
                 "aliases": ["像被大象踩一样", "像被压碎", "像被车碾过", "压着的感觉"]},
    "压迫感": {"english": "pressing", "type": "nociceptive", "dimension": "sensory",
               "aliases": ["像被石头压着", "压着痛", "压痛"]},
    "挤压感": {"english": "squeezing", "type": "nociceptive", "dimension": "sensory",
               "aliases": ["被挤压", "紧缩感"]},
    "牵拉痛": {"english": "pulling", "type": "nociceptive", "dimension": "sensory"},
    "撕裂痛": {"english": "tearing", "type": "nociceptive", "dimension": "sensory"},
    "裂开样痛": {"english": "splitting", "type": "nociceptive", "dimension": "sensory"},
    "痛楚": {"english": "sore", "type": "nociceptive", "dimension": "sensory"},
    "触痛": {"english": "tender", "type": "nociceptive", "dimension": "sensory"},
    "钝痛": {"english": "dull", "type": "nociceptive", "dimension": "sensory"},
    "沉重感": {"english": "heavy", "type": "nociceptive", "dimension": "sensory",
               "aliases": ["重的感觉", "像被重物压着", "沉甸甸"]},
    
    # Thermal (温度性)
    "发热感": {"english": "hot", "type": "nociceptive", "dimension": "sensory",
               "aliases": ["热痛", "火辣辣", "烫痛"]},
    "冷痛": {"english": "cold", "type": "nociceptive", "dimension": "sensory"},
    "冰冷刺痛": {"english": "freezing", "type": "nociceptive", "dimension": "sensory"},
    "灼热痛": {"english": "scalding", "type": "nociceptive", "dimension": "sensory"},
    
    # Affective (情感性)
    "令人疲惫": {"english": "exhausting", "type": "affective", "dimension": "affective"},
    "令人劳累": {"english": "tiring", "type": "affective", "dimension": "affective"},
    "麻烦的": {"english": "troublesome", "type": "affective", "dimension": "affective"},
    "悲惨的": {"english": "miserable", "type": "affective", "dimension": "affective"},
    "无法忍受": {"english": "unbearable", "type": "affective", "dimension": "affective"},
    "可怕的": {"english": "frightful", "type": "affective", "dimension": "affective"},
    "恐怖的": {"english": "terrifying", "type": "affective", "dimension": "affective"},
    "残酷的": {"english": "cruel", "type": "affective", "dimension": "affective"},
    "凶恶的": {"english": "vicious", "type": "affective", "dimension": "affective"},
    "折磨人": {"english": "punishing", "type": "affective", "dimension": "affective"},
    
    # Evaluative (评价性)
    "恼人的": {"english": "annoying", "type": "evaluative", "dimension": "evaluative"},
    "纠缠不休": {"english": "nagging", "type": "evaluative", "dimension": "evaluative"},
    "强烈的": {"english": "intense", "type": "evaluative", "dimension": "evaluative"},
}

# Korean McGill Pain Descriptors (한국어 맥길 통증 설문지)
KOREAN_MCGILL = {
    # Sensory - Neuropathic
    "타는 느낌": {"english": "burning", "type": "neuropathic", "dimension": "sensory"},
    "따끔거림": {"english": "tingling", "type": "neuropathic", "dimension": "sensory"},
    "무감각": {"english": "numbness", "type": "neuropathic", "dimension": "sensory"},
    "개미가 기어가는 느낌": {"english": "formication", "type": "neuropathic", "dimension": "sensory",
                      "aliases": ["개미 감각", "벌레 기어가는"]},
    "바늘로 찌르는": {"english": "pins and needles", "type": "neuropathic", "dimension": "sensory"},
    "전기 충격": {"english": "electric shock", "type": "neuropathic", "dimension": "sensory"},
    "쏘는": {"english": "shooting", "type": "neuropathic", "dimension": "sensory"},
    "칼로 찌르는": {"english": "stabbing", "type": "neuropathic", "dimension": "sensory"},
    "날카로운": {"english": "sharp", "type": "neuropathic", "dimension": "sensory"},
    "꿰뚫는": {"english": "piercing", "type": "neuropathic", "dimension": "sensory"},
    "쏘는 통증": {"english": "stinging", "type": "neuropathic", "dimension": "sensory"},
    
    # Sensory - Nociceptive
    "쑤시는": {"english": "aching", "type": "nociceptive", "dimension": "sensory"},
    "욱신거리는": {"english": "throbbing", "type": "nociceptive", "dimension": "sensory"},
    "두드리는": {"english": "pounding", "type": "nociceptive", "dimension": "sensory"},
    "때리는": {"english": "beating", "type": "nociceptive", "dimension": "sensory"},
    "맥박": {"english": "pulsing", "type": "nociceptive", "dimension": "sensory"},
    "경련": {"english": "cramping", "type": "nociceptive", "dimension": "sensory"},
    "갉아먹는": {"english": "gnawing", "type": "nociceptive", "dimension": "sensory"},
    "으스러지는": {"english": "crushing", "type": "nociceptive", "dimension": "sensory"},
    "누르는": {"english": "pressing", "type": "nociceptive", "dimension": "sensory"},
    "조이는": {"english": "squeezing", "type": "nociceptive", "dimension": "sensory"},
    "당기는": {"english": "pulling", "type": "nociceptive", "dimension": "sensory"},
    "찢어지는": {"english": "tearing", "type": "nociceptive", "dimension": "sensory"},
    "갈라지는": {"english": "splitting", "type": "nociceptive", "dimension": "sensory"},
    "아픈": {"english": "sore", "type": "nociceptive", "dimension": "sensory"},
    "압통": {"english": "tender", "type": "nociceptive", "dimension": "sensory"},
    "둔한": {"english": "dull", "type": "nociceptive", "dimension": "sensory"},
    "무거운": {"english": "heavy", "type": "nociceptive", "dimension": "sensory"},
    
    # Thermal
    "뜨거운": {"english": "hot", "type": "nociceptive", "dimension": "sensory"},
    "차가운": {"english": "cold", "type": "nociceptive", "dimension": "sensory"},
    "얼어붙는": {"english": "freezing", "type": "nociceptive", "dimension": "sensory"},
    "데는": {"english": "scalding", "type": "nociceptive", "dimension": "sensory"},
    
    # Affective
    "지치게 하는": {"english": "exhausting", "type": "affective", "dimension": "affective"},
    "피곤하게 하는": {"english": "tiring", "type": "affective", "dimension": "affective"},
    "귀찮은": {"english": "troublesome", "type": "affective", "dimension": "affective"},
    "비참한": {"english": "miserable", "type": "affective", "dimension": "affective"},
    "참을 수 없는": {"english": "unbearable", "type": "affective", "dimension": "affective"},
    "무서운": {"english": "frightful", "type": "affective", "dimension": "affective"},
    "공포스러운": {"english": "terrifying", "type": "affective", "dimension": "affective"},
    "잔인한": {"english": "cruel", "type": "affective", "dimension": "affective"},
    "악의적인": {"english": "vicious", "type": "affective", "dimension": "affective"},
    "처벌하는": {"english": "punishing", "type": "affective", "dimension": "affective"},
    
    # Evaluative
    "짜증나는": {"english": "annoying", "type": "evaluative", "dimension": "evaluative"},
    "괴롭히는": {"english": "nagging", "type": "evaluative", "dimension": "evaluative"},
    "강렬한": {"english": "intense", "type": "evaluative", "dimension": "evaluative"},
}

# Spanish McGill Pain Descriptors (Cuestionario de Dolor McGill en Español)
SPANISH_MCGILL = {
    # Sensory - Neuropathic
    "ardiente": {"english": "burning", "type": "neuropathic", "dimension": "sensory",
                 "aliases": ["quemante", "que arde"]},
    "hormigueo": {"english": "tingling", "type": "neuropathic", "dimension": "sensory"},
    "entumecimiento": {"english": "numbness", "type": "neuropathic", "dimension": "sensory",
                       "aliases": ["adormecimiento"]},
    "sensación de hormigas": {"english": "formication", "type": "neuropathic", "dimension": "sensory",
                              "aliases": ["como hormigas caminando", "hormigueo intenso"]},
    "alfileres y agujas": {"english": "pins and needles", "type": "neuropathic", "dimension": "sensory"},
    "choque eléctrico": {"english": "electric shock", "type": "neuropathic", "dimension": "sensory",
                         "aliases": ["descarga eléctrica"]},
    "punzante": {"english": "shooting", "type": "neuropathic", "dimension": "sensory"},
    "apuñalante": {"english": "stabbing", "type": "neuropathic", "dimension": "sensory"},
    "agudo": {"english": "sharp", "type": "neuropathic", "dimension": "sensory"},
    "perforante": {"english": "piercing", "type": "neuropathic", "dimension": "sensory"},
    "punzada": {"english": "stinging", "type": "neuropathic", "dimension": "sensory"},
    
    # Sensory - Nociceptive
    "dolor sordo": {"english": "aching", "type": "nociceptive", "dimension": "sensory"},
    "pulsátil": {"english": "throbbing", "type": "nociceptive", "dimension": "sensory",
                 "aliases": ["latiendo", "palpitante"]},
    "martilleante": {"english": "pounding", "type": "nociceptive", "dimension": "sensory"},
    "golpeante": {"english": "beating", "type": "nociceptive", "dimension": "sensory"},
    "pulsante": {"english": "pulsing", "type": "nociceptive", "dimension": "sensory"},
    "calambre": {"english": "cramping", "type": "nociceptive", "dimension": "sensory"},
    "roedor": {"english": "gnawing", "type": "nociceptive", "dimension": "sensory"},
    "aplastante": {"english": "crushing", "type": "nociceptive", "dimension": "sensory"},
    "presión": {"english": "pressing", "type": "nociceptive", "dimension": "sensory"},
    "apretante": {"english": "squeezing", "type": "nociceptive", "dimension": "sensory"},
    "tirante": {"english": "pulling", "type": "nociceptive", "dimension": "sensory"},
    "desgarrante": {"english": "tearing", "type": "nociceptive", "dimension": "sensory"},
    "dividiendo": {"english": "splitting", "type": "nociceptive", "dimension": "sensory"},
    "adolorido": {"english": "sore", "type": "nociceptive", "dimension": "sensory"},
    "sensible": {"english": "tender", "type": "nociceptive", "dimension": "sensory"},
    "sordo": {"english": "dull", "type": "nociceptive", "dimension": "sensory"},
    "pesado": {"english": "heavy", "type": "nociceptive", "dimension": "sensory"},
    
    # Thermal
    "caliente": {"english": "hot", "type": "nociceptive", "dimension": "sensory"},
    "frío": {"english": "cold", "type": "nociceptive", "dimension": "sensory"},
    "congelante": {"english": "freezing", "type": "nociceptive", "dimension": "sensory"},
    "escaldante": {"english": "scalding", "type": "nociceptive", "dimension": "sensory"},
    
    # Affective
    "agotador": {"english": "exhausting", "type": "affective", "dimension": "affective"},
    "cansador": {"english": "tiring", "type": "affective", "dimension": "affective"},
    "problemático": {"english": "troublesome", "type": "affective", "dimension": "affective"},
    "miserable": {"english": "miserable", "type": "affective", "dimension": "affective"},
    "insoportable": {"english": "unbearable", "type": "affective", "dimension": "affective"},
    "espantoso": {"english": "frightful", "type": "affective", "dimension": "affective"},
    "aterrador": {"english": "terrifying", "type": "affective", "dimension": "affective"},
    "cruel": {"english": "cruel", "type": "affective", "dimension": "affective"},
    "vicioso": {"english": "vicious", "type": "affective", "dimension": "affective"},
    "castigador": {"english": "punishing", "type": "affective", "dimension": "affective"},
    
    # Evaluative
    "molesto": {"english": "annoying", "type": "evaluative", "dimension": "evaluative"},
    "persistente": {"english": "nagging", "type": "evaluative", "dimension": "evaluative"},
    "intenso": {"english": "intense", "type": "evaluative", "dimension": "evaluative"},
}

# Hmong McGill Pain Descriptors (Hmong McGill Mob Nug)
HMONG_MCGILL = {
    # Sensory - Neuropathic
    "kub hnyiab": {"english": "burning", "type": "neuropathic", "dimension": "sensory"},
    "tub nkeeg": {"english": "tingling", "type": "neuropathic", "dimension": "sensory"},
    "loog": {"english": "numbness", "type": "neuropathic", "dimension": "sensory"},
    "zoo li ntsaum nkag": {"english": "formication", "type": "neuropathic", "dimension": "sensory",
                           "aliases": ["zoo li kab nkag", "ntsaum taug kev"]},
    "koob thiab tus pin": {"english": "pins and needles", "type": "neuropathic", "dimension": "sensory"},
    "mob hluav taw xob": {"english": "electric shock", "type": "neuropathic", "dimension": "sensory"},
    "tua": {"english": "shooting", "type": "neuropathic", "dimension": "sensory"},
    "ntaus ntaj": {"english": "stabbing", "type": "neuropathic", "dimension": "sensory"},
    "ntse": {"english": "sharp", "type": "neuropathic", "dimension": "sensory"},
    "piercing": {"english": "piercing", "type": "neuropathic", "dimension": "sensory"},
    "tom": {"english": "stinging", "type": "neuropathic", "dimension": "sensory"},
    
    # Sensory - Nociceptive
    "mob": {"english": "aching", "type": "nociceptive", "dimension": "sensory"},
    "dhia": {"english": "throbbing", "type": "nociceptive", "dimension": "sensory"},
    "ntaus": {"english": "pounding", "type": "nociceptive", "dimension": "sensory"},
    "ntaus": {"english": "beating", "type": "nociceptive", "dimension": "sensory"},
    "pulsing": {"english": "pulsing", "type": "nociceptive", "dimension": "sensory"},
    "cramping": {"english": "cramping", "type": "nociceptive", "dimension": "sensory"},
    "zom": {"english": "gnawing", "type": "nociceptive", "dimension": "sensory"},
    "tsoo": {"english": "crushing", "type": "nociceptive", "dimension": "sensory"},
    "nias": {"english": "pressing", "type": "nociceptive", "dimension": "sensory"},
    "nyem": {"english": "squeezing", "type": "nociceptive", "dimension": "sensory"},
    "rub": {"english": "pulling", "type": "nociceptive", "dimension": "sensory"},
    "tsuas": {"english": "tearing", "type": "nociceptive", "dimension": "sensory"},
    "sib cais": {"english": "splitting", "type": "nociceptive", "dimension": "sensory"},
    "mob": {"english": "sore", "type": "nociceptive", "dimension": "sensory"},
    "rhiab": {"english": "tender", "type": "nociceptive", "dimension": "sensory"},
    "dull": {"english": "dull", "type": "nociceptive", "dimension": "sensory"},
    "hnyav": {"english": "heavy", "type": "nociceptive", "dimension": "sensory"},
    
    # Thermal
    "kub": {"english": "hot", "type": "nociceptive", "dimension": "sensory"},
    "txias": {"english": "cold", "type": "nociceptive", "dimension": "sensory"},
    "khov": {"english": "freezing", "type": "nociceptive", "dimension": "sensory"},
    "scalding": {"english": "scalding", "type": "nociceptive", "dimension": "sensory"},
    
    # Affective
    "nkees": {"english": "exhausting", "type": "affective", "dimension": "affective"},
    "nkees": {"english": "tiring", "type": "affective", "dimension": "affective"},
    "teeb meem": {"english": "troublesome", "type": "affective", "dimension": "affective"},
    "tu siab": {"english": "miserable", "type": "affective", "dimension": "affective"},
    "tsis tau": {"english": "unbearable", "type": "affective", "dimension": "affective"},
    "ntshai": {"english": "frightful", "type": "affective", "dimension": "affective"},
    "txaus ntshai": {"english": "terrifying", "type": "affective", "dimension": "affective"},
    "siab phem": {"english": "cruel", "type": "affective", "dimension": "affective"},
    "phem": {"english": "vicious", "type": "affective", "dimension": "affective"},
    "rau txim": {"english": "punishing", "type": "affective", "dimension": "affective"},
    
    # Evaluative
    "ntxhov siab": {"english": "annoying", "type": "evaluative", "dimension": "evaluative"},
    "nagging": {"english": "nagging", "type": "evaluative", "dimension": "evaluative"},
    "muaj zog": {"english": "intense", "type": "evaluative", "dimension": "evaluative"},
}
