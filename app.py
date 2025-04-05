from flask import Flask, render_template
from db import init_db
from routes import register_routes

app = Flask(__name__)
app.secret_key = "your_secret_key"

# Initialize DB
init_db(app)

# Register routes
register_routes(app)

# Default route (Index Page)
@app.route('/')
def index():
    return render_template('index.html')

if __name__ == "__main__":
    app.run(debug=True)
