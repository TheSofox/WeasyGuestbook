import datetime

from flask import Flask, flash, redirect, render_template, request, session


app = Flask(__name__)
entries = []
entry_names = []
entry_dates = []

def add_guest_post(name, entry):
    entry_names.append(name)
    entries.append(entry or '<blank>')
    entry_dates.append(datetime.datetime.now())
    
def delete_guest_post(index):
    del entries[index]
    del entry_names[index]
    del entry_dates[index]


@app.route('/')
def index():
    return render_template(
        'index.html', entries=zip(entry_names, entry_dates, entries))

@app.route('/submit', methods=['POST'])
def submit():
    if not request.form['name']:
        flash("you must provide a name!")
        return redirect('/')
    add_guest_post(request.form['name'], request.form['entry']);
    return redirect('/')

@app.route('/admin')
def admin_login():
    return render_template('login.html')


@app.route('/logout')
def admin_logout():
    session['logged_in'] = False
    return redirect('/')

@app.route('/admin', methods=['POST'])
def do_admin_login():
    if request.form['password'] == 'password':
        session['logged_in'] = True
        return redirect('/')
    else:
        flash('wrong password!')
        return admin_login()

@app.route('/moderate', methods=['POST'])
def moderate_posts():
    marked_posts = []
    for key in request.form:
        if not key.startswith('delete_'):
            continue
        marked_posts.append(int(key.partition('_')[2]))
    marked_posts.sort(reverse=True)
    for index in marked_posts:
        delete_guest_post(index)
    return redirect('/')


if __name__ == '__main__':
    import os
    app.secret_key = os.urandom(12)
    app.run(debug=True)
