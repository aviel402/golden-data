# קובץ: api/index.py
# זהו הקוד המלא של "שרת הנתונים"

from flask import Flask, request, jsonify
import json
import os

app = Flask(__name__)

# הנתיב לקובץ הנתונים שלנו בתוך הסביבה הזמנית של Vercel
DB_FILE_PATH = '/tmp/golden_forest_db.json'

# --- פעולת קריאת הנתונים (GET) ---
@app.route('/', methods=['GET'])
def get_data():
    try:
        # בודקים אם הקובץ בכלל קיים
        if not os.path.exists(DB_FILE_PATH):
            # אם לא, זה אומר שאין נתונים עדיין. נחזיר אובייקט ריק.
            return jsonify({}), 200

        with open(DB_FILE_PATH, 'r', encoding='utf-8') as f:
            data = json.load(f)
            return jsonify(data), 200

    except Exception as e:
        print(f"Error reading data: {e}")
        return jsonify(error="שגיאה בקריאת הנתונים מהשרת"), 500

# --- פעולת כתיבת/עדכון הנתונים (POST) ---
@app.route('/', methods=['POST'])
def save_data():
    try:
        # מקבלים את המידע החדש מגוף הבקשה
        new_data = request.json
        if new_data is None:
            return jsonify(error="לא נשלח מידע לעדכון"), 400

        with open(DB_FILE_PATH, 'w', encoding='utf-8') as f:
            # דורסים את כל הקובץ במידע החדש
            json.dump(new_data, f, indent=4, ensure_ascii=False)
            
        return jsonify(message="הנתונים נשמרו בהצלחה"), 200

    except Exception as e:
        print(f"Error saving data: {e}")
        return jsonify(error="שגיאה בשמירת הנתונים בשרת"), 500
