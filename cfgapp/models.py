import os
from flask import *
from flask_sqlalchemy import SQLAlchemy
import pandas as pd
import numpy as np
from matplotlib import pyplot as plt


basedir = os.path.abspath(os.path.dirname(__file__))

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'data.sqlite')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

class Country(db.Model):

    # If you don't provide this, the default table name will be the class name
    __tablename__ = 'countries'

    id = db.Column(db.Integer,primary_key=True)
    country_name = db.Column(db.String, nullable=False,index=True)
    country_code= db.Column(db.String, nullable=False,index=True)
    

    # This sets what an instance in this table will have
    # Note the id will be auto-created for us later, so we don't add it here!
    def __init__(self,country_name,country_code):
        self.country_name = country_name
        self.country_code= country_code


db.create_all()

AF=Country('Afghanistan','AF')
AU=Country('Australia','AU')
BE=Country('Belgium','BE')
BH=Country('Bhutan','BH')
BR=Country('Brazil','BR')
CA=Country('Canada','CA')
CN=Country('China','CN')
DE=Country('Germany','DE')
FR=Country('France','FR')
IT=Country('Italy','IT')
JP=Country('Japan','JP')
MX=Country('Mexico','MX')
MY=Country('Malaysia','MY')
NZ=Country('New Zealand','NZ')
PT=Country('Portugal','PT')
ES=Country('Spain','ES')
US=Country('United States of America','US')
PK=Country('Pakistan','PK')
SY=Country('Syria','SY')

db.session.add_all([AF,AU,BE,BH,BR,CA,CN,DE,FR,IT,JP,MX,MY,NZ,PT,ES,US,PK,SY])
db.session.commit()

@app.route('/')
def main():
    return render_template('main.html')

@app.route('/supplyMap')
def supplyMap():
    return render_template('supplyMap.html')

@app.route('/demandMap')
def demandMap():
    return render_template('demandMap.html')

@app.route('/supply/<var>',methods=['GET','POST'])
def supply(var):
    user=Country.query.filter_by(var=Country.country_code).first()
    id1=user.id
    plotgraph(id1)
    return render_template('supply.html',id=var)


@app.route('/demand/<var>')
def demand(var):
    return render_template('demand.html',id=var)


def plotgraph(id):
    eggs = pd.read_csv("eggs.csv")
    eggs = eggs.drop(columns = ["Code"])
    eggs.columns

    countries = pd.get_dummies(eggs['Entity']).columns

    country_data = []
    for country in countries:
        df = eggs[eggs['Entity'] == country].drop(columns = ['Entity'])
        country_data.append([country, df])
    
    
    afg = country_data[id]
    x = afg[1]['Year']
    y = afg[1]['Egg supply per person (kilograms per year)']
    plt.plot(x,y)
    plt.show()


if __name__=="__main__":

    app.run(debug=True)


