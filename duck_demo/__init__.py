#!/usr/bin/env python
# -*- coding:utf-8 -*-


def init(app):
    from .view import index
    return [
        index.blueprint,
    ]
