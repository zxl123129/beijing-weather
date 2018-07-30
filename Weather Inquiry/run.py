#coding:utf-8
from flask import Flask, render_template, request, redirect, url_for, session, flash
from flask_bootstrap import Bootstrap

from flask_wtf import Form 
from wtforms import StringField, SubmitField 
from wtforms.validators import Required 
 
from city_code_xml_parse import get_city_code
from weather_reptile import get_weather_data

class NameForm(Form): 
    name = StringField('请输入待查询天气的城市', validators=[Required()]) 
    submit = SubmitField('查询')

app=Flask(__name__)
bootstrap=Bootstrap(app)
app.config['SECRET_KEY'] = 'hard to guess string'

@app.route('/', methods=['GET', 'POST']) 
def index(): 
    form = NameForm() 
    if form.validate_on_submit():
        if form.name.data in city_dict:
            session['name'] = form.name.data                
            return redirect(url_for('index')) 
        else:
            flash('请输入正确的中国城市名！')
            return redirect(url_for('index')) 
    else:
        if 'name' in session: 
            name = session.get('name') 
        else: 
            name = '北京'
        city_code = city_dict.get(name)
        weather = get_weather_data(city_code)
        weather = weather[1]
        return render_template('index.html', form = form, name = name, weather = " ".join('%s'%id for id in weather))

#变量保存在用户会话中，即 session['name']，所以在两次请求之间也能记住输入的值

@app.errorhandler(404)  
def page_not_found(e):  
    return render_template('404.html'), 404  

if __name__=="__main__":
    city_dict = get_city_code()
    app.run(debug=True)