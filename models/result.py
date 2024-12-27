from flask import jsonify


class Result:
    @staticmethod
    def success(message, data=None):
        return jsonify({
            'status': 'success',  # code: 200
            'message': message,
            'data': data
        })

    @staticmethod
    def error(message):
        return jsonify({
            'status': 'error',
            'message': message,
        })
