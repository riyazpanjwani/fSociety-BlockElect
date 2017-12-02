from block import block
from flask import render_template
from flask import request

@block.route('/')
@block.route('/index')
def index():
    return render_template('index.html')