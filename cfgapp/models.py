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

AF=Country('Afghanistan','AFG')
AU=Country('Australia','AUS')
BE=Country('Belgium','BEL')
BH=Country('Bhutan','BHA')
BR=Country('Brazil','BRA')
CA=Country('Canada','CAN')
CN=Country('China','CHN')
DE=Country('Germany','DEU')
FR=Country('France','FRA')
IT=Country('Italy','ITA')
JP=Country('Japan','JPN')
MX=Country('Mexico','MEX')
MY=Country('Malaysia','MYS')
NZ=Country('New Zealand','NZ')
PT=Country('Portugal','PRT')
ES=Country('Spain','ESP')
US=Country('United States of America','USA')
PK=Country('Pakistan','PAK')
SY=Country('Syria','SYR')

db.session.add_all([AF,AU,BE,BH,BR,CA,CN,DE,FR,IT,JP,MX,MY,NZ,PT,ES,US,PK,SY])
db.session.commit()

@app.route('/')
def main():
    return render_template('main.html')

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
    plt.savefig('new_plot.png')

def plotgraph2(id):
    data = pd.read_csv("egg-production-thousand-tonnes.csv")
    data = data.drop(columns = ['Code'])
    data.columns

    countries = pd.get_dummies(data['Entity']).columns
    values= data.Entity
    v=sorted(set(values))
    country_data = []
    for country in countries:
        df = data[data['Entity'] == country].drop(columns = ['Entity'])
        country_data.append([country, df])

    afg = country_data[id]
    print(v[id])
    x = afg[1]['Year']
    y = afg[1]['Livestock Primary - Eggs Primary - 1783 - Production - 5510 - tonnes (tonnes)']
    plt.plot(x,y)
    plt.savefig('new_plot1.png')

################################################

@app.route('/supplyMap')
def supplyMap():
    return render_template('supplyMap.html')


@app.route('/display')
def display():
    return render_template('display.html')

@app.route('/display1')
def display1():
    return render_template('display1.html')

@app.route('/demandMap')
def demandMap():
    return render_template('demandMap.html')

@app.route('/supply/<code>',methods=['GET','POST'])
def supply(code):
    try:
        user=Country.query.filter_by(country_code=code).first()
        id=user.id
        plotgraph2(id)
        return redirect(url_for('display1'))
    except:
        pass
    
    return render_template('supply.html',supply=user.country_code)


@app.route('/demand/<code>')
def demand(code):
    try:
        user=Country.query.filter_by(country_code=code).first()
        id=user.id
        plotgraph(id)
        return redirect(url_for('display'))
    except:
        pass
    
    return render_template('demand.html',supply=user.country_code)

@app.route('/compare')
def compare():
    return render_template('compare.html')

@app.route('/compareGraphs')
def compareGraphs():
    return render_template('compareGraphs.html')


if __name__=="__main__":

    app.run(debug=True)


