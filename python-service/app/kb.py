from pathlib import Path
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

class KnowledgeBase:
    def __init__(self, root: str):
        self.docs=[]
        for p in Path(root).glob('*.md'):
            self.docs.append({'title': p.stem.replace('_',' ').title(), 'text': p.read_text()})
        self.vectorizer=TfidfVectorizer(stop_words='english')
        self.matrix=self.vectorizer.fit_transform([d['text'] for d in self.docs]) if self.docs else None

    def search(self, query: str, k: int=3):
        if not self.docs: return []
        q=self.vectorizer.transform([query])
        scores=cosine_similarity(q,self.matrix)[0]
        idx=scores.argsort()[::-1][:k]
        return [{**self.docs[i], 'score': float(scores[i])} for i in idx if scores[i] > 0]
