from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///game.db'
db = SQLAlchemy(app)

class Player(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    score = db.Column(db.Integer, default=0)

@app.route('/')
def index():
    players = Player.query.all()
    return render_template('index.html', players=players)

@app.route('/register', methods=['POST'])
def register():
    name = request.form['name']
    new_player = Player(name=name)
    db.session.add(new_player)
    db.session.commit()
    return redirect(url_for('index'))

@app.route('/update_score', methods=['POST'])
def update_score():
    player_id = request.form['player_id']
    score = request.form['score']
    player = Player.query.get(player_id)
    player.score = score
    db.session.commit()
    return redirect(url_for('index'))

if __name__ == '__main__':
    with app.app_context():
        db.create_all()  # Initialize the database
    app.run(debug=True)
