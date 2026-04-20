"""
Language Detection Utility
Detects the language of input text for multilingual pain assessment
Supports: Chinese, Korean, Spanish, Hmong, English
"""
import re
from typing import Literal

LanguageCode = Literal['zh', 'ko', 'es', 'hmong', 'en']

def detect_language(text: str) -> LanguageCode:
    """
    Detect the primary language of the input text.
    
    Uses character-based heuristics:
    - Chinese: CJK Unified Ideographs (U+4E00–U+9FFF)
    - Korean: Hangul Syllables (U+AC00–U+D7A3)
    - Spanish: Spanish-specific characters (ñ, á, é, í, ó, ú, ü, ¿, ¡)
    - Hmong: Latin script with specific patterns
    - English: Default fallback
    
    Args:
        text: Input text to detect language from
        
    Returns:
        Language code: 'zh', 'ko', 'es', 'hmong', or 'en'
    """
    if not text or not text.strip():
        return 'en'
    
    # Count characters by script
    chinese_chars = len(re.findall(r'[\u4e00-\u9fff]', text))
    korean_chars = len(re.findall(r'[\uac00-\ud7a3]', text))
    spanish_chars = len(re.findall(r'[ñáéíóúü¿¡]', text, re.IGNORECASE))
    
    # Total characters (excluding whitespace)
    total_chars = len(re.findall(r'\S', text))
    
    if total_chars == 0:
        return 'en'
    
    # Chinese detection (>30% CJK characters)
    if chinese_chars / total_chars > 0.3:
        return 'zh'
    
    # Korean detection (>30% Hangul characters)
    if korean_chars / total_chars > 0.3:
        return 'ko'
    
    # Spanish detection (Spanish-specific characters OR common Spanish words)
    spanish_keywords = [
        'tengo', 'dolor', 'muy', 'que', 'para', 'con', 'por',
        'esta', 'tiene', 'cuando', 'donde', 'como', 'agudo', 'punzante'
    ]
    text_lower = text.lower()
    spanish_word_matches = sum(1 for kw in spanish_keywords if f' {kw} ' in f' {text_lower} ')
    
    if spanish_chars > 0 or spanish_word_matches >= 2:
        return 'es'
    
    # Hmong detection (heuristic: common Hmong words)
    hmong_keywords = [
        'mob', 'txoj', 'kev', 'kuv', 'koj', 'nws', 'lawv',
        'ntawm', 'rau', 'los', 'thiab', 'muaj', 'yog', 'tsis'
    ]
    text_lower = text.lower()
    hmong_matches = sum(1 for kw in hmong_keywords if kw in text_lower)
    
    if hmong_matches >= 2:  # At least 2 Hmong keywords
        return 'hmong'
    
    # Default to English
    return 'en'

def get_language_name(code: LanguageCode) -> str:
    """
    Get full language name from language code.
    
    Args:
        code: Language code
        
    Returns:
        Full language name
    """
    names = {
        'zh': 'Chinese',
        'ko': 'Korean',
        'es': 'Spanish',
        'hmong': 'Hmong',
        'en': 'English'
    }
    return names.get(code, 'Unknown')

# Test cases
if __name__ == '__main__':
    test_cases = [
        ("我有火辣辣的疼痛", "zh"),
        ("허리가 따끔거리듯이 아프다", "ko"),
        ("Tengo un dolor agudo y punzante", "es"),
        ("Kuv mob mob heev", "hmong"),
        ("I have a sharp stabbing pain", "en"),
        ("My back hurts so bad", "en"),
    ]
    
    print("Language Detection Tests:")
    print("=" * 60)
    for text, expected in test_cases:
        detected = detect_language(text)
        status = "✅" if detected == expected else "❌"
        print(f"{status} '{text}'")
        print(f"   Expected: {expected}, Detected: {detected} ({get_language_name(detected)})")
        print()
