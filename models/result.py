from flask import jsonify


class Result:
    @staticmethod
    def success(message='success', data=None):
        return jsonify({
            'code': 200,
            'message': message,
            'data': data
        })

    @staticmethod
    def error(message):
        return jsonify({
            'code': 500,
            'message': message,
        })
