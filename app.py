from flask import Flask, jsonify, request
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy

# Flaskインスタンスの作成
app = Flask(__name__)
CORS(app)

# データベースの接続情報を指定
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///my_database.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# データベースのインスタンスを作成
db = SQLAlchemy(app)


class Item(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), nullable=False)

    def __init__(self, name):
        self.name = name

    def __repr__(self):
        return f'<Item {self.name}>'


# テーブル作成
with app.app_context():
    db.create_all()


@app.route('/')
def hello():
    return 'Hello Flask'


@app.route('/items', methods=['GET'])
# Item情報を全て取得し、返却
def get_items():
    items = Item.query.all()
    return jsonify([str(item) for item in items])


@app.route('/items', methods=['POST'])
# Itemにデータを追加
def add_item():
    name = request.json['name']
    item = Item(name=name)

    # データを一時保存(DBには保存されない)
    db.session.add(item)
    # ここでDBに保存される
    db.session.commit()
    return jsonify(str(item)), 201


if __name__ == '__main__':
    app.run(debug=True)  # debug=True 開発用サーバ
