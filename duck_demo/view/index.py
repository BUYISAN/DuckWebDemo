#!/usr/bin/env python
# -*- coding:utf-8 -*-
from flask import Blueprint

blueprint = Blueprint('index', __name__)


@blueprint.route('/')
def index():
    return 'Hello World'
