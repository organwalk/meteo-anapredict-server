"""
    定义响应处理
    by organwalk 2023-08-15
"""
from collections import OrderedDict
from flask import Response
import json

__SUCCESS_CODE = 200
__NOT_FOUND_CODE = 404
__ERROR_CODE = 500
__FAIL_ENTITY_CODE = 422
__FAIL_METHOD_CODE = 405


def success(msg, data):
    return Response(
        json.dumps(
            OrderedDict([
                ('code', __SUCCESS_CODE),
                ('msg', msg),
                ('data', data)
            ])
        ),
        mimetype='application/json'
    )


def not_found(msg):
    return Response(
        json.dumps(
            OrderedDict([
                ('code', __NOT_FOUND_CODE),
                ('msg', msg)
            ])
        ),
        mimetype='application/json'
    )


def error(msg):
    return Response(
        json.dumps(
            OrderedDict([
                ('code', __ERROR_CODE),
                ('msg', msg)
            ])
        ),
        mimetype='application/json'
    )


def fail_entity(msg):
    return Response(
        json.dumps(
            OrderedDict([
                ('code', __FAIL_ENTITY_CODE),
                ('msg', msg)
            ])
        ),
        mimetype='application/json'
    )


def fail_method(msg):
    return Response(
        json.dumps(
            OrderedDict([
                ('code', __FAIL_METHOD_CODE),
                ('msg', msg)
            ])
        ),
        mimetype='application/json'
    )