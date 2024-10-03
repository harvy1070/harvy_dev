import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

# 자카드 유사도
def jaccard_similarity(set1, set2):
    intersection = len(set1.intersection(set2))
    union = len(set1.union(set2))
    return intersection / union

# 코사인 유사도
def cosine_similarity(text1, text2):
    vec = TfidfVectorizer()
    tfidf_matrix = vec.fit_transform([text1, text2])
    return cosine_similarity(tfidf_matrix[0:1], tfidf_matrix[1:2])[0][0]

# 처음은 쓰레시홀드를 50%로 설정하여 진행
def is_similar(text1, text2, threshold=0.5, method='cosine'):
    if method == 'jaccard':
        set1 = set(text1.lower().split())
        set2 = set(text2.lower().split())
        similarity = jaccard_similarity(set1, set2)
    elif method == 'cosine':
        similarity =cosine_similarity(text1, text2)
    else:
        raise ValueError("지원하지 않는 유사도 측정 방법임")
    
    return similarity >= threshold, similarity