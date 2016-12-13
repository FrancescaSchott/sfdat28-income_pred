from flask import Flask, render_template, session, redirect, url_for
from flask.ext.wtf import Form
from wtforms import IntegerField, StringField, SubmitField, SelectField, DecimalField
from wtforms.validators import Required
import pickle
from sklearn import datasets

# Initialize Flask App
app = Flask(__name__)


print "loading my model"
with open('model.pkl', 'rb') as handle:
    machine_learning_model = pickle.load(handle)
print "model loaded"


# Initialize Form Class
class theForm(Form):
    param1 = DecimalField(label='Exercise (no:1 yes:2):', places=2, validators=[Required()])
    param2 = DecimalField(label='Food Amount (not enough:1, sometimes enough:2, enough:3):', places=2, validators=[Required()])
    param3 = DecimalField(label='Occupation Category (1-6):', places=2, validators=[Required()])
    param4 = DecimalField(label='Stores (1-5):', places=2, validators=[Required()])
    submit = SubmitField('Submit')


@app.route('/', methods=['GET', 'POST'])
def home():
    print session
    form = theForm(csrf_enabled=False)
    if form.validate_on_submit():  # activates this if when i hit submit!
        # Retrieve values from form
        session['exercise'] = form.param1.data
        session['food_amount'] = form.param2.data
        session['cat_occ'] = form.param3.data
        session['stores'] = form.param4.data
        # Create array from values
        income_instance = [(session['exercise']), (session['food_amount']), (session['cat_occ']),
                           (session['stores'])]

        # Return only the Predicted iris species
        income = ['above 185%', 'below 185%']
        session['prediction'] = income[machine_learning_model.predict(income_instance)[0]]

        # Implement Post/Redirect/Get Pattern
        return redirect(url_for('home'))

    return render_template('home.html', form=form, **session)


# Handle Bad Requests
@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404

app.secret_key = 'super_secret_key_shhhhhh'
if __name__ == '__main__':
    app.run(debug=True)
