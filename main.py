from flask import Flask, render_template
from flask_bootstrap import Bootstrap
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired
import requests
from bs4 import BeautifulSoup


app = Flask(__name__)
app.config['SECRET_KEY'] = '123'
bootstrap = Bootstrap(app)

class FormCharacter(FlaskForm):
	name = StringField('Ingresa un nombre de personaje', validators=[DataRequired()])
	submit = SubmitField('Submit')

# api
@app.route('/search/', methods=['POST', 'GET'])
def search():
	form = FormCharacter()
	results = []
	if form.validate_on_submit():
		name = form.name.data
		results = requests.get(f"https://www.breakingbadapi.com/api/characters?name={name}").json()
	return render_template('search.html', form=form, results=results)


#scrap
@app.route('/episodes/')
def episodes():
	URL = "https://en.wikipedia.org/wiki/List_of_Breaking_Bad_episodes"
	page = requests.get(URL)

	soup = BeautifulSoup(page.content, "html.parser")

	episodes = []
	tables = soup.find_all("table", class_="wikitable plainrowheaders wikiepisodetable")
	for table in tables:
		tabletbody = table.tbody
		rows = tabletbody.find_all("tr", class_="vevent")
		for row in rows:
			try:
				title = row.find("td", class_="summary")
				episodes.append(title.text)
			except:
				continue

	return render_template('episodes.html', episodes=episodes)
