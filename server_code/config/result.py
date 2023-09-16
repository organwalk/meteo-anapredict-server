"""
    定义响应处理
    by organwalk 2023-08-15
"""
from collections import OrderedDict
from flask import Response
import json

_SUCCESS_CODE = 200
_NOT_FOUND_CODE = 404
_ERROR_CODE = 500
_FAIL_ENTITY_CODE = 422
_FAIL_METHOD_CODE = 405


def success(msg: str, data: any) -> Response:
    return Response(
        json.dumps(
            OrderedDict([
                ('code', _SUCCESS_CODE),
                ('msg', msg),
                ('data', data)
            ])
        ),
        mimetype='application/json'
    )


def not_found(msg: str) -> Response:
    return Response(
        json.dumps(
            OrderedDict([
                ('code', _NOT_FOUND_CODE),
                ('msg', msg)
            ])
        ),
        mimetype='application/json'
    )


def error(msg: str) -> Response:
    return Response(
        json.dumps(
            OrderedDict([
                ('code', _ERROR_CODE),
                ('msg', msg)
            ])
        ),
        mimetype='application/json'
    )


def fail_entity(msg: str) -> Response:
    return Response(
        json.dumps(
            OrderedDict([
                ('code', _FAIL_ENTITY_CODE),
                ('msg', msg)
            ])
        ),
        mimetype='application/json'
    )


def fail_method(msg: str) -> Response:
    return Response(
        json.dumps(
            OrderedDict([
                ('code', _FAIL_METHOD_CODE),
                ('msg', msg)
            ])
        ),
        mimetype='application/json'
    )
