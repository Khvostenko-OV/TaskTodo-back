import math
import re

from flask import jsonify, request
from flask_login import current_user, login_user, logout_user
from sqlalchemy import desc

from app import app, db
from config import DEFAULT_PAGE_LIMIT
from models import Task, User


@app.after_request
def after_request(response):
    response.headers.add('Access-Control-Allow-Credentials', 'true')
    return response


@app.route('/login', methods=['post'])
def login():
    username = request.form.get('login')
    password = request.form.get('password')
    if not username or not password:
        return jsonify({'error': 400, 'message': 'Login and password required'})

    user = db.session.query(User).filter(User.username == username).first()
    if not user:
        return jsonify({'error': 404, 'message': f"User '{username}' not found"})

    if not user.check_password(password):
        return jsonify({'error': 400, 'message': 'Bad pair login/password'})

    login_user(user)

    return jsonify(user.to_dict)


@app.route('/logout', methods=['post'])
def logout():
    logout_user()
    return jsonify({'message': 'OK'})


@app.route('/tasks')
def task_list():
    page = int(request.args.get('page', 1))
    limit = int(request.args.get('limit', DEFAULT_PAGE_LIMIT)) or DEFAULT_PAGE_LIMIT
    order = request.args.get('order', 'id')
    total = db.session.query(Task).count()
    page_count = math.ceil(total/limit)
    page = min(page, page_count) or 1
    offset = page * limit - limit
    if order in ['author', 'email', 'done']:
        tasks = db.session.query(Task).order_by(order).offset(offset).limit(limit)
    elif order in ['-author', '-email', '-done']:
        tasks = db.session.query(Task).order_by(desc(order[1:])).offset(offset).limit(limit)
    else:
        tasks = db.session.query(Task).order_by('id').offset(offset).limit(limit)

    resp = {
        'page': page,
        'limit': limit,
        'count': page_count,
        'total': total,
        'tasks': [t.to_dict for t in tasks],
    }

    if current_user.is_authenticated:
        resp['user'] = current_user.to_dict
    else:
        resp['user'] = {'username': None, 'email': None, 'is_admin': False}

    return jsonify(resp)


@app.route('/tasks/add', methods=['post'])
def task_add():
    author = request.form.get('author')
    email = request.form.get('email')
    text = request.form.get('text')
    if not all([author, email, text]) or not re.match(r'^[\w\.-]+@[\w\.-]+(\.[\w]+)+$', email):
        return jsonify({'error': 400, 'message': 'Bad data'})

    task = Task(author=author, email=email, text=text)
    db.session.add(task)
    db.session.commit()
    return jsonify(task.to_dict)


@app.route('/tasks/edit/<int:pk>', methods=['post'])
def task_edit(pk):
    if not current_user.is_authenticated or not current_user.is_admin:
        return jsonify({'error': 401, 'message': 'Access denied!'})

    text = request.form.get('text')
    done = bool(request.form.get('done'))
    task = db.session.query(Task).get(pk)
    if not task:
        return jsonify({'error': 404, 'message': 'Task not found'})

    if text == task.text and done == task.done:
        return jsonify(task.to_dict)

    task.done = done
    if text != task.text:
        task.changed = True
    task.text = text
    db.session.add(task)
    db.session.commit()
    return jsonify(task.to_dict)
