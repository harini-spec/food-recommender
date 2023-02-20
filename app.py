from flask import Flask, render_template, request
import model 

app = Flask(__name__)

@app.route('/', methods = ['GET', 'POST'])
def home():

    return render_template('form.html')


@app.route('/submit', methods = ['GET', 'POST'])
def submit():

    if request.method == 'POST':

        song = request.values.get("song")

        songs = model.main(song)

        print(songs)

        return render_template('form.html', songs=songs)
    return render_template('form.html', songs=songs)


if __name__== "__main__":
    app.run(host="0.0.0.0", debug = True, port = 5003)