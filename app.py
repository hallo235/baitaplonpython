from flask import Flask, request, jsonify
from recommend import StoryRecommender

app = Flask(__name__)
recommender = StoryRecommender()

@app.route("/recommend", methods=["GET"])
def recommend():
    genre = request.args.get("genre")
    keywords = request.args.get("keywords")
    story_id = request.args.get("story_id", type=int)

    # Chuyển keywords từ chuỗi sang danh sách
    keywords_list = keywords.split(",") if keywords else None

    result = recommender.hybrid_recommend(genre=genre, keywords=keywords_list, input_story_id=story_id)

    return jsonify(result)

if __name__ == "__main__":
    app.run(debug=True)
