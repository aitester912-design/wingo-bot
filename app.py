from flask import Flask, jsonify
import trend_check_2  # Aapki original file

app = Flask(__name__)

@app.route('/get-data')
def get_data():
    # trend_check_2.py ke variables yahan access honge
    return jsonify({
        "total_big": trend_check_2.total_big,
        "total_small": trend_check_2.total_small,
        "max_big_streak": trend_check_2.max_big,
        "max_small_streak": trend_check_2.max_small
    })

if __name__ == '__main__':
    app.run(debug=True)