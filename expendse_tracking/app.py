from flask import Flask, render_template, redirect
from datetime import datetime
from flask_wtf import FlaskForm
from wtforms import StringField, DecimalField, SubmitField, DateField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError

all_expense = [
  {
    "id":1,
    "title":"Headphones",
    "category":"Electronics",
    "amount":100,
    "date": datetime.strptime("22-02-2019",'%d-%m-%Y')
  },
  {
    "id":2,
    "title":"BBQ and Bacons",
    "category":"Food",
    "amount":200,
    "date": datetime.strptime("23-03-2019",'%d-%m-%Y')
  },
  {
    "id":3,
    "title":"Beer",
    "category":"Drinks",
    "amount":400,
    "date": datetime.strptime("20-03-2019",'%d-%m-%Y')
  }
]

class ExpenseForm(FlaskForm):
    title = StringField('Title', validators=[DataRequired])
    category = StringField('Category', validators=[DataRequired()])
    amount = DecimalField('Amount', validators=[DataRequired()])
    date = DateField('Date')
    submit = SubmitField('Submit')

    def __repr__(self):
      return f"ExpenseForm('{self.title}','{self.category}','{self.amount}','{self.date}')"


app = Flask(__name__)
app.config['SECRET_KEY'] = 'a_secret_key. You may change it later'

@app.route('/home',)
@app.route('/')
def home():
  return render_template('home.html', expenses=all_expense)

@app.route('/add', methods=['GET','POST'])
def add():
    form = ExpenseForm()
    if form.validate_on_submit():
        all_expenses.append({
          'title': form.title.data,
          'category': form.category.data,
          'amount': form.amount.data,
          'date': form.date.data
        })
        return redirect('home.html')
    form.date.data = datetime.utcnow()
    return render_template('add.html', form=form)

if __name__ == '__main__':
  app.run(host='127.0.0.1', port=5000, debug=True)

