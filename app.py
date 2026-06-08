from flask import Flask, jsonify
import trend_check

app = Flask(__name__)

@app.route('/get-data')
def get_data():
    return jsonify({
        "total_big": trend_check.total_big,
        "total_small": trend_check.total_small,
        "max_big": trend_check.max_big,
        "max_small": trend_check.max_small
    })

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=10000)