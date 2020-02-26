from flask import Flask

app = Flask(__name__)

"""
Reference: https://github.com/TheComeUpCode/SpotifyGeneratePlaylist
"""


@app.route('/')
def hello_world():
    return 'Hello World!'


if __name__ == '__main__':
    app.run()
