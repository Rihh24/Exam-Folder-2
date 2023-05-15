from flask import render_template, request, flash, redirect, session
from flask_app import app
from flask_app.models.user import User
from flask_app.models.tree import Tree

@app.route('/trees')
def homepage():
    if 'user_id' not in session:
        return redirect('/')
    user = User.get_id({"id":session['user_id']})
    if not user:
        return redirect('/logout')
        
    return render_template('homepage.html', user=user, trees =Tree.get_all_trees())

@app.route('/trees/user')
def user_trees():
    if 'user_id' not in session:
        return redirect('/')
    user = User.get_id({"id":session['user_id']})
    if not user:
        return redirect('/logout')
    return render_template("user_trees.html", user=user, trees=Tree.get_all_trees())


@app.route('/trees/create')
def create_tree():
    if 'user_id' not in session:
        return redirect('/')
    user = User.get_id({"id":session['user_id']})
    if not user:
        return redirect('/logout')
    return render_template('new_tree.html', user=user)

@app.route('/trees/create/submit', methods =['POST'])
def submit_tree():
    if 'user_id' not in session:
        return redirect('/')
    if not Tree.validate_new_tree(request.form):
        return redirect('/trees/create')

    data = {
        'species': request.form['species'],
        'location': request.form['location'],
        'reason': request.form['reason'],
        'date_planted': request.form['date_planted'],
        'user_id': session['user_id']
    }
    Tree.save_tree(data)
    return redirect('/trees')


@app.route('/trees/update/<int:id>')
def update_tree_page(id):
    if 'user_id' not in session:
        return redirect('/')
    user = User.get_id({"id":session['user_id']})
    if not user:
        return redirect('/logout')
    return render_template('update_tree.html',user=user, tree=Tree.get_tree_id({'id': id}))

@app.route('/trees/update/submit/<int:id>', methods=['POST'])
def submit_update_tree(id):
    if 'user_id' not in session:
        return redirect('/')
    if not Tree.validate_new_tree(request.form):
        return redirect(f'/trees/update/{id}')
    data={
        'id': id,
        'species': request.form['species'],
        'location': request.form['location'],
        'reason': request.form['reason'],
        'date_planted': request.form['date_planted'],
    }
    Tree.update_tree(data)
    return redirect('/trees')

@app.route('/trees/show/<int:id>')
def detail_page(id):
    if 'user_id' not in session:
        return redirect('/')
    user = User.get_id({"id":session['user_id']})
    if not user:
        return redirect('/logout')
    data = {
        'id': id
    }
    return render_template("view_tree.html",user=user,tree=Tree.get_one_tree(data))

@app.route('/trees/destroy/<int:id>')
def destroy(id):
    data ={
        'id': id
    }
    Tree.destroy(data)
    return redirect('/trees/user')
