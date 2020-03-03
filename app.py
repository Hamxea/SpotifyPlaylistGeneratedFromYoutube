from flask import Flask, render_template, redirect, url_for

from CreatePlaylist import CreatePlaylist

app = Flask(__name__)

"""
Reference: https://github.com/TheComeUpCode/SpotifyGeneratePlaylist
"""


@app.route('/')
def index():
    """ index home page"""
    # return redirect('/addsong',)
    return render_template('index.html')


@app.route('/addsong')
def song_to_playlist():
    """add song from youtube to spotify like video"""
    create_playlist = CreatePlaylist()

    add_song = create_playlist.add_song_to_playlist()

    return add_song


@app.route('/success')
def success():
    return render_template('success.html')


if __name__ == '__main__':
    app.run()
