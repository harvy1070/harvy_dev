import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity as sklearn_cosine_similarity

def jaccard_similarity(set1, set2):
    intersection = len(set1.intersection(set2))
    union = len(set1.union(set2))
    return intersection / union if union != 0 else 0

def cosine_similarity(text1, text2):
    vec = TfidfVectorizer().fit([text1, text2])
    tfidf = vec.transform([text1, text2])
    return sklearn_cosine_similarity(tfidf[0:1], tfidf[1:2])[0][0]

def is_similar(text1, text2, threshold=0.5, method='cosine'):
    # 입력이 문자열인지 확인
    if not isinstance(text1, str) or not isinstance(text2, str):
        raise ValueError("입력은 반드시 문자열이어야 합니다.")
    
    # 소문자 변환 및 공백 제거
    text1 = text1.lower().strip()
    text2 = text2.lower().strip()
    
    if method == 'jaccard':
        set1 = set(text1.split())
        set2 = set(text2.split())
        similarity = jaccard_similarity(set1, set2)
    elif method == 'cosine':
        similarity = cosine_similarity(text1, text2)
    else:
        raise ValueError("지원하지 않는 유사도 측정 방법입니다.")
    
    return similarity >= threshold, similarity