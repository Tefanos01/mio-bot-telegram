from flask import Flask

app = Flask(__name__)

@app.route('/')
def index():
    return "Bot is running!"

if __name__ == '__main__':
    # usa la porta che Render assegna
    import os
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
