from flask import Flask, render_template, request, jsonify
import sqlite3
from datetime import datetime

app = Flask(__name__)

# Initialize the database
def init_db():
    conn = sqlite3.connect('nozzle.db')
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS nozzle_data (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            date TEXT,
            day TEXT,
            petrol_rate REAL,
            nozzle_1 REAL,
            nozzle_2 REAL,
            nozzle_3 REAL,
            nozzle_4 REAL,
            nozzle_5 REAL,
            nozzle_6 REAL,
            nozzle_7 REAL,
            nozzle_8 REAL
        )
    ''')
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS nozzle_difference_data (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            date TEXT,
            day TEXT,
            petrol_rate_diff REAL,
            nozzle_1_diff REAL,
            nozzle_2_diff REAL,
            nozzle_3_diff REAL,
            nozzle_4_diff REAL,
            nozzle_5_diff REAL,
            nozzle_6_diff REAL,
            nozzle_7_diff REAL,
            nozzle_8_diff REAL
        )
    ''')
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS sales_data (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            date TEXT,
            day TEXT,
            petrol_rate REAL,
            nozzle_1_sale REAL,
            nozzle_2_sale REAL,
            nozzle_3_sale REAL,
            nozzle_4_sale REAL,
            nozzle_5_sale REAL,
            nozzle_6_sale REAL,
            nozzle_7_sale REAL,
            nozzle_8_sale REAL
        )
    ''')
    conn.commit()
    conn.close()

# Calculate differences and insert into the difference table
def calculate_and_insert_differences(new_row):
    conn = sqlite3.connect('nozzle.db')
    cursor = conn.cursor()
    
    cursor.execute('SELECT * FROM nozzle_data ORDER BY id DESC LIMIT 2')
    rows = cursor.fetchall()
    
    if len(rows) < 2:
        cursor.execute('''
            INSERT INTO nozzle_difference_data (date, day, petrol_rate_diff, nozzle_1_diff, nozzle_2_diff, nozzle_3_diff, nozzle_4_diff, nozzle_5_diff, nozzle_6_diff, nozzle_7_diff, nozzle_8_diff)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', (new_row[1], new_row[2], 0, 0, 0, 0, 0, 0, 0, 0, 0))
    else:
        prev_row = rows[1]
        differences = [
            new_row[3] - prev_row[3],  # petrol_rate_diff
            new_row[4] - prev_row[4],  # nozzle_1_diff
            new_row[5] - prev_row[5],  # nozzle_2_diff
            new_row[6] - prev_row[6],  # nozzle_3_diff
            new_row[7] - prev_row[7],  # nozzle_4_diff
            new_row[8] - prev_row[8],  # nozzle_5_diff
            new_row[9] - prev_row[9],  # nozzle_6_diff
            new_row[10] - prev_row[10],  # nozzle_7_diff
            new_row[11] - prev_row[11]  # nozzle_8_diff
        ]
        
        cursor.execute('''
            INSERT INTO nozzle_difference_data (date, day, petrol_rate_diff, nozzle_1_diff, nozzle_2_diff, nozzle_3_diff, nozzle_4_diff, nozzle_5_diff, nozzle_6_diff, nozzle_7_diff, nozzle_8_diff)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', (new_row[1], new_row[2], *differences))

    conn.commit()
    conn.close()

# Calculate sale and insert into the sales table
def calculate_sale(new_row):
    conn = sqlite3.connect('nozzle.db')
    cursor = conn.cursor()
    
    # Get the previous row to calculate the differences
    cursor.execute('SELECT * FROM nozzle_data ORDER BY id DESC LIMIT 2')
    rows = cursor.fetchall()
    
    if len(rows) < 2:
        # If there's no previous data, insert zeros
        cursor.execute('''
            INSERT INTO sales_data (date, day, petrol_rate, nozzle_1_sale, nozzle_2_sale, nozzle_3_sale, nozzle_4_sale, nozzle_5_sale, nozzle_6_sale, nozzle_7_sale, nozzle_8_sale)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', (new_row[1], new_row[2], new_row[3], 0, 0, 0, 0, 0, 0, 0, 0))
    else:
        prev_row = rows[1]
        sales = [
            (new_row[4] - prev_row[4]) * new_row[3],  # nozzle_1_sale
            (new_row[5] - prev_row[5]) * new_row[3],  # nozzle_2_sale
            (new_row[6] - prev_row[6]) * new_row[3],  # nozzle_3_sale
            (new_row[7] - prev_row[7]) * new_row[3],  # nozzle_4_sale
            (new_row[8] - prev_row[8]) * new_row[3],  # nozzle_5_sale
            (new_row[9] - prev_row[9]) * new_row[3],  # nozzle_6_sale
            (new_row[10] - prev_row[10]) * new_row[3],  # nozzle_7_sale
            (new_row[11] - prev_row[11]) * new_row[3]  # nozzle_8_sale
        ]
        
        cursor.execute('''
            INSERT INTO sales_data (date, day, petrol_rate, nozzle_1_sale, nozzle_2_sale, nozzle_3_sale, nozzle_4_sale, nozzle_5_sale, nozzle_6_sale, nozzle_7_sale, nozzle_8_sale)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', (new_row[1], new_row[2], new_row[3], *sales))

    conn.commit()
    conn.close()

# Route to render the main page
@app.route('/')
def index():
    return render_template('index.html')

# Route to handle form submission
@app.route('/submit_sales', methods=['POST'])
def submit_sales():
    data = request.json
    date = datetime.now().strftime('%Y-%m-%d')
    day = datetime.now().strftime('%A')
    petrol_rate = data['petrol_rate']
    nozzles = data['nozzles']

    if len(nozzles) != 8:
        return jsonify({'status': 'error', 'message': 'Invalid number of nozzles'}), 400

    nozzles = [float(n) for n in nozzles]

    conn = sqlite3.connect('nozzle.db')
    cursor = conn.cursor()
    cursor.execute('''
        INSERT INTO nozzle_data (date, day, petrol_rate, nozzle_1, nozzle_2, nozzle_3, nozzle_4, nozzle_5, nozzle_6, nozzle_7, nozzle_8)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    ''', (date, day, petrol_rate, *nozzles))
    new_row = cursor.execute('SELECT * FROM nozzle_data ORDER BY id DESC LIMIT 1').fetchone()
    conn.commit()
    conn.close()

    calculate_and_insert_differences(new_row)
    calculate_sale(new_row)  # Add this line

    return jsonify({'status': 'success'})

# Route to fetch database content
@app.route('/fetch_db')
def fetch_db():
    conn = sqlite3.connect('nozzle.db')
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM nozzle_data')
    rows = cursor.fetchall()
    conn.close()
    
    data = []
    for row in rows:
        data.append({
            'id': row[0],
            'date': row[1],
            'day': row[2],
            'petrol_rate': row[3],
            'nozzle_1': row[4],
            'nozzle_2': row[5],
            'nozzle_3': row[6],
            'nozzle_4': row[7],
            'nozzle_5': row[8],
            'nozzle_6': row[9],
            'nozzle_7': row[10],
            'nozzle_8': row[11],
        })
    
    return jsonify(data)

# Route to fetch differences database content
@app.route('/fetch_differences_db')
def fetch_differences_db():
    conn = sqlite3.connect('nozzle.db')
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM nozzle_difference_data')
    rows = cursor.fetchall()
    conn.close()
    
    data = []
    for row in rows:
        data.append({
            'id': row[0],
            'date': row[1],
            'day': row[2],
            'petrol_rate_diff': row[3],
            'nozzle_1_diff': row[4],
            'nozzle_2_diff': row[5],
                        'nozzle_3_diff': row[6],
            'nozzle_4_diff': row[7],
            'nozzle_5_diff': row[8],
            'nozzle_6_diff': row[9],
            'nozzle_7_diff': row[10],
            'nozzle_8_diff': row[11],
        })
    
    return jsonify(data)

# Route to fetch sales database content
@app.route('/fetch_sales_db')
def fetch_sales_db():
    conn = sqlite3.connect('nozzle.db')
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM sales_data')
    rows = cursor.fetchall()
    conn.close()
    
    data = []
    for row in rows:
        data.append({
            'id': row[0],
            'date': row[1],
            'day': row[2],
            'petrol_rate': row[3],
            'nozzle_1_sale': row[4],
            'nozzle_2_sale': row[5],
            'nozzle_3_sale': row[6],
            'nozzle_4_sale': row[7],
            'nozzle_5_sale': row[8],
            'nozzle_6_sale': row[9],
            'nozzle_7_sale': row[10],
            'nozzle_8_sale': row[11],
        })
    
    return jsonify(data)

if __name__ == '__main__':
    init_db()
    app.run(debug=True)
