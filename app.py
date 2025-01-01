from flask import Flask, request, jsonify, send_from_directory
from openai import OpenAI
import os
from dotenv import load_dotenv

# .envファイルから環境変数を読み込む
load_dotenv()

app = Flask(__name__, static_folder='static')

# OpenAI APIクライアントの初期化
client = OpenAI(api_key=os.environ.get('OPENAI_API_KEY'))

# ルートエンドポイントを定義し、index.htmlを返す
@app.route('/naming_app/')
def serve_index():
    return app.send_static_file('index.html')

# 名前生成用APIエンドポイント
@app.route('/naming_app/generate_name', methods=['POST'])
def generate_name():
    data = request.get_json()
    query = data.get('query', '')

    if not query:
        return jsonify({'error': 'クエリが空です。'}), 400

    try:
        # GPT-4o-miniモデルを使用して名前を生成
        response = client.chat.completions.create(
            model="gpt-4o-mini",  # 明示的に指定されたモデル名
            messages=[
                {"role": "system", "content": "あなたは英語のプログラム名、変数名、関数名を提案するアシスタントです。"},
                {"role": "user", "content": f"以下の説明に合った適切な英語のプログラム名、変数名、または関数名を考えてください：'{query}'"}
            ],
            max_tokens=50,
            temperature=0.7,
        )

        # レスポンスから結果を取得（ドット記法でアクセス）
        result = response.choices[0].message.content.strip()
        return jsonify({'result': result})
    except Exception as e:
        print(f'Error: {e}')
        return jsonify({'error': '名前の生成中にエラーが発生しました。'}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5050, debug=True)
