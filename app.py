from flask import Flask, render_template, request
from wtforms import TextAreaField, Form, validators

app = Flask(__name__)


class ReviewForm(Form):
    moviereview = TextAreaField('',
                                [validators.DataRequired(), validators.length(min=15)])

def classify(review):
    prob = len(review)/150
    cls = int(prob > 0.5)
    return cls, prob

@app.route('/')
def index():
    form = ReviewForm(request.form)
    return render_template('reviewform.html', form=form)


@app.route('/results', methods=['POST'])
def results():
    form = ReviewForm(request.form)
    if request.method == 'POST' and form.validate():
        review = request.form['moviereview']
        y, proba = classify(review)
        return render_template('results.html',
                               content=review,
                               prediction=y,
                               probability=round(proba * 100, 2))
    return render_template('reviewform.html', form=form)


if __name__ == '__main__':
    app.run(debug=True)
