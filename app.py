import sqlite3
from flask import Flask, render_template, request, flash, redirect, url_for

app = Flask(__name__)
app.secret_key = 'shubham_secret_key'  # Needed for flashing session messages
DATABASE = 'portfolio.db'

def get_db_connection():
    """Establishes a connection to the SQLite database."""
    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row  # Allows accessing columns by name like a dictionary
    return conn

def init_db():
    """Creates the contact messages table if it doesn't already exist."""
    conn = get_db_connection()
    conn.execute('''
        CREATE TABLE IF NOT EXISTS messages (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            email TEXT NOT NULL,
            message TEXT NOT NULL,
            submitted_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    conn.commit()
    conn.close()

# Initialize the database table on application start
init_db()

PROJECTS_DATA = [
    {
        "title": "Depression Support Chatbot",
        "duration": "Jul 2025 - Sep 2025",
        "tech": ["Flask/Django", "Scikit-learn", "NLTK", "Bootstrap 5"],
        "desc": "An AI-powered emotional support chatbot featuring TF-IDF and Logistic Regression for intent detection, dual-mode theme, and a crisis-response feature. [cite: 19, 20, 21, 22]"
    },
    {
        "title": "Stock Master",
        "duration": "Sep 2025 - Nov 2025",
        "tech": ["Python", "Django", "MySQL", "Bootstrap 5"],
        "desc": "An inventory management system featuring PDF report generation, search filtering, and smooth operational capabilities for small-to-medium scale industries. [cite: 23, 25, 26, 27]"
    },
    {
        "title": "Care Bridge",
        "duration": "Recent",
        "tech": ["Python", "Django", "SQL", "HTML5/CSS3"],
        "desc": "Full-stack web application focused on delivering a clean digital experience. Deployed successfully on production cloud environments. [cite: 28, 29, 30]"
    }
]

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/projects')
def projects():
    return render_template('projects.html', projects=PROJECTS_DATA)

@app.route('/contact', methods=['GET', 'POST'])
def contact():
    if request.method == 'POST':
        name = request.form.get('name')
        email = request.form.get('email')
        message = request.form.get('message')
        
        # Backend validation check
        if not name or not email or not message:
            flash("All fields are required!", "danger")
            return redirect(url_for('contact'))
        
        try:
            # Insert the form submission into the SQLite database
            conn = get_db_connection()
            conn.execute(
                'INSERT INTO messages (name, email, message) VALUES (?, ?, ?)',
                (name, email, message)
            )
            conn.commit()
            conn.close()
            
            flash(f"Thank you, {name}! Your message has been saved successfully.", "success")
        except Exception as e:
            flash("An error occurred while saving your message. Please try again.", "danger")
            print(f"Database Error: {e}")
            
        return redirect(url_for('contact'))
        
    return render_template('contact.html')

# Optional: Admin route to securely view messages locally
@app.route('/admin/messages')
def view_messages():
    conn = get_db_connection()
    messages = conn.execute('SELECT * FROM messages ORDER BY submitted_at DESC').fetchall()
    conn.close()
    return render_template('admin_messages.html', messages=messages)

if __name__ == '__main__':
    app.run(debug=True)