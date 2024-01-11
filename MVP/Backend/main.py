from flask import Flask, jsonify
from threading import Thread
from webCrawler.newsGrabber import run_crawler

app = Flask(__name__)

@app.route('/get_news', methods=['GET'])
def start_crawler():
    thread = Thread(target=run_crawler)
    thread.start()
    return jsonify({"message": "Crawler started"})

# ... (existing Flask code)

@app.route('/update_news', methods=['GET'])
def update_news():
    news_data = fetch_news()
    return jsonify(news_data)


if __name__ == "__main__":
    app.run(debug=True)
