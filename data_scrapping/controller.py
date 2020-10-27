from flask import Flask, render_template, request
import ETL_jobs, constants.tiki_information as tiki_info
import psycopg2, json, sys, os, math
from packages.object_scrapping import category
import threading


controller = Flask(__name__, static_folder='custom')
conn = psycopg2.connect(tiki_info.db_connection)

@controller.route('/')
@controller.route('/home')
def home():
    return render_template('home.html')

@controller.route('/scrapping')
def scrapping():
    all_categories = category.category().get_parent_category(conn)
    return render_template('scrapping.html', all_categories = all_categories)

@controller.route('/dashboard')
def dashboard():
    return render_template('dashboard.html')

@controller.route('/scrap_all_categories')
def scrap_all_categories():   
    result = ETL_jobs.extract_all_category(tiki_info.tiki_url, conn)
    return result        

@controller.route('/scrap')
def scrap_category():
    args = request.args.to_dict()
    ETL_jobs.extract_content_category(args['category_id'], args['category_name'], conn)
    return ('scrap category: ', request.args)

@controller.route('/cancel_job')
def cancel_job():    
    print('Starting pause job: ')
    ETL_jobs.pause_jobs()
    print('After pause. ')
    all_categories = category.category().get_parent_category(conn)
    return render_template('scrapping.html', all_categories = all_categories)

if __name__ == '__main__':
    controller.run(debug=True)