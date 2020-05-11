# -*- coding: utf-8 -*-
from gevent import monkey
monkey.patch_all()
import os
from duck.web import DuckApp
from flask import render_template_string, url_for

app = DuckApp("")
app.flaskapp.config['SECRET_KEY'] = 'abcdefghigk'

import duck_demo

# 装载blueprint
app.mount(duck_demo)


@app.flaskapp.context_processor
def override_url_for():
    """
    使用url_for函数，endpoint为static时，为url添加version参数，
    其值为文件修改时间戳，帮助刷新浏览器缓存
    """
    def dated_url_for(endpoint, **values):
        if endpoint == 'static':
            filename = values.get('filename', None)
            if filename:
                file_path = os.path.join(app.flaskapp.static_folder, filename)
                try:
                    values['version'] = int(os.stat(file_path).st_mtime)
                except Exception as e:
                    print(e)
                    pass
        return url_for(endpoint, **values)
    return dict(url_for=dated_url_for)


@app.flaskapp.route('/favicon.ico', methods=['GET'])
def favicon_ico():
    return '', 204


@app.flaskapp.errorhandler(404)
def url_not_found(e):
    string_not_found = '''
        <title> 404 </title>
        <h1> Not Found</h1>
        <p> What you were looking for is just not there.
        <p><a href="{{ url_for('index.index') }}"> go somewhere nice</a>
    '''
    return render_template_string(string_not_found), 404


if __name__ == '__main__':
    app.run()
