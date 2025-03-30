import json
from collections import Counter
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

class StoryRecommender:
    def __init__(self, data_path="stories.json"):
        self.data_path = data_path
        self.stories = self.load_data()

    def load_data(self):
        """Load danh sách truyện từ file JSON"""
        with open(self.data_path, "r", encoding="utf-8") as file:
            return json.load(file)

    def recommend_by_genre(self, genre):
        """Gợi ý truyện theo thể loại"""
        return {story["id"]: 1.0 for story in self.stories if story["genre"] == genre}

    def recommend_by_keywords(self, keywords):
        """Gợi ý truyện theo từ khóa"""
        keyword_counts = Counter(keywords)
        scores = {}
        for story in self.stories:
            score = sum(keyword_counts[k] for k in story["keywords"] if k in keyword_counts)
            if score > 0:
                scores[story["id"]] = score
        return scores

    def recommend_by_content(self, input_story_id):
        """Gợi ý truyện dựa trên nội dung bằng TF-IDF"""
        contents = [story["content"] for story in self.stories]
        vectorizer = TfidfVectorizer().fit_transform(contents)
        similarities = cosine_similarity(vectorizer)

        story_index = next((i for i, s in enumerate(self.stories) if s["id"] == input_story_id), None)
        if story_index is None:
            return {}

        scores = {self.stories[i]["id"]: similarities[story_index][i] for i in range(len(self.stories))}
        del scores[input_story_id]  # Bỏ chính truyện đầu vào
        return scores

    def hybrid_recommend(self, genre=None, keywords=None, input_story_id=None, weight_genre=1.0, weight_keywords=1.5, weight_content=2.0):
        """Gợi ý truyện kết hợp nhiều phương pháp"""
        scores = {}

        # Gợi ý theo thể loại
        if genre:
            genre_scores = self.recommend_by_genre(genre)
            for story_id, score in genre_scores.items():
                scores[story_id] = scores.get(story_id, 0) + score * weight_genre

        # Gợi ý theo từ khóa
        if keywords:
            keyword_scores = self.recommend_by_keywords(keywords)
            for story_id, score in keyword_scores.items():
                scores
