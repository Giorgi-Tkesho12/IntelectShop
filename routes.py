from flask import Flask, request, render_template, redirect, flash
from flask_login import login_required, login_user, logout_user, current_user
from forms import AddProductForm, RegisterForm, AddWriterCategory, EditProductForm, LoginForm, CommentForm
from ext import app, db, path
from models import Writeri, WriterCategory, User, Comments



@app.route("/")
def index():
    mwerlebi = Writeri.query.all()

    return render_template("index.html", writers=mwerlebi)


@app.route("/mwerali/<int:mwerali_id>")
def about(mwerali_id):
    chosen_writer = Writeri.query.get(mwerali_id)
    return render_template("writer.html", writers = chosen_writer)

@app.route("/edit_writer/<int:mwerali_id>", methods = ["POST", "GET"])
@login_required
def edit_writer(mwerali_id):
    chosen_writer = Writeri.query.get(mwerali_id)
    form = EditProductForm(name=chosen_writer.name, description=chosen_writer.description, category_id=chosen_writer.category_id)

    if current_user.role != "admin":
        return redirect("/")

    if form.validate_on_submit():
        chosen_writer.name = form.name.data
        chosen_writer.description = form.description.data
        chosen_writer.category_id = form.category.data
        flash("მწერლის რედაქტირება წარმატებით დასრულდა!", "info")
        
        if form.img.data:
            chosen_writer.img = form.img.data.filename
            file_directory = path.join(app.root_path, "static", form.img.data.filename)
            form.img.data.save(file_directory)

        chosen_writer.save()
        flash("მწერლის რედაქტირება წარმატებით დასრულდა!", "info")
        return redirect("/")
    else:
        print(form.errors)

    return render_template("add_writers.html", form=form)

@app.route("/delete_writer/<int:mwerali_id>", methods = ["POST", "GET"])
@login_required
def delete_writer(mwerali_id):
    chosen_writer = Writeri.query.get(mwerali_id)

    if current_user.role != "admin":
        return redirect("/")
    chosen_writer.delete()
    flash("მწერალი წარმატებით წაიშალა", "warning")

    return redirect("/")


@app.route("/add_writer", methods = ["POST", "GET"])
@login_required
def add_writ():
    form = AddProductForm()
    if current_user.role != "admin":
        return redirect("/")

    if form.validate_on_submit():
        new_writer = Writeri(name=form.name.data, img=form.img.data.filename, description=form.description.data, category_id=form.category.data)
        db.session.add(new_writer)
        db.session.commit()
        flash("მწერალი წარმატებით დაემატა!", "success")

        file_directory = path.join(app.root_path, "static", form.img.data.filename)
        form.img.data.save(file_directory)
        return redirect("/")
    else:
        print(form.errors)
    
    
    return render_template("add_writers.html", form = form)

@app.route("/search/<string:name>")
@login_required
def search(name):
    mwerlebi = Writeri.query.filter(Writeri.name.ilike(f"%{name}%")).all()
    return render_template("search.html", writers=mwerlebi)

@app.route("/category/<int:category_id>")
def category(category_id):
    mwerlebi = Writeri.query.filter(Writeri.category_id == category_id).all()
    return render_template("category.html", writers=mwerlebi)


@app.route("/registration", methods = ["GET", "POST"])
def reg():
    form = RegisterForm()
    if form.validate_on_submit():
        existing_user=User.query.filter_by(username=form.username.data).first()
        if existing_user:
            flash("ასეთი მომხმარებელი უკვე არსებობს! სცადეთ თავიდან!", "warning")
            return redirect("/registration")
        else:
            new_user = User(username=form.username.data, password=form.password.data, role="user")
            new_user.create()
            flash("თქვენ წარმატებით გაიარეთ რეგისტრაცია!", "info")
            return redirect("/authorization")

    
    return render_template("reg.html", form=form)

@app.route("/authorization", methods = ["GET", "POST"])
def auth():
    form=LoginForm()
    if form.validate_on_submit():
        user=User.query.filter(User.username == form.username.data).first()
        if user and user.password == form.password.data:
            login_user(user)
            flash("თქვენ წარმატებით გაიარეთ ავტორიზაცია!", "info")
            return redirect("/")
        else:
            flash("თქვენ მიერ ჩაწერილი ინფორმაცია არასწორია! სცადეთ თავიდან!", "error")
            return redirect("/authorization")
    return render_template("auth.html", form=form)

@app.route("/logout")
def logout():
    logout_user()
    return redirect("/")

@app.route("/add_comment", methods=["GET", "POST"])
@login_required
def add_comment():
    form=CommentForm()
    if form.validate_on_submit():
        commenter=current_user.id
        comments=Comments(content=form.content.data, commented_id=commenter)
        comments.create()
        flash("კომენტარი წარმატებით დაემატა ფორუმს!", "success")
        return redirect("/forum")
    return render_template("add_comment.html", form=form)

@app.route("/forum", methods=["GET", "POST"])
@login_required
def forum():
    comments = Comments.query.order_by(Comments.date_commented)
    return render_template("forum.html", comments=comments)

@app.route("/edit_comments/<int:comment_id>", methods=["GET", "POST"])
@login_required
def edit_comment(comment_id):
    chosen_comment=Comments.query.get(comment_id)
    if current_user.id != chosen_comment.commented_id:
        flash("თქვენ არ გაქვთ წვდომა სხვა მომხმარებლების ინფორმაციაზე!", "error")
        return redirect("/forum")
    else:
        form = CommentForm()
        if form.validate_on_submit():
            chosen_comment.content = form.content.data
            chosen_comment.save()
            flash("კომენტარი წარმატებით დარედაქტირდა!", "info")
            return redirect("/forum")
        else:
            print(form.errors)
        form.content.data=chosen_comment.content
    return render_template("/add_comment.html", form=form, comments=chosen_comment)

@app.route("/delete_comments/<int:comment_id>", methods = ["POST", "GET"])
@login_required
def delete_comment(comment_id):
    chosen_comment = Comments.query.get(comment_id)
    comment_id=current_user.id

    if comment_id == chosen_comment.commenter.id or current_user.role == "admin":
        chosen_comment.delete()
        flash("კომენტარი წარმატებით წაიშალა!", "info")
    else:
        flash("თქვენ არ გაქვთ წვდომა სხვა მომხმარებლების ინფორმაციაზე!", "error")

    return redirect("/forum")

@app.route("/about_me")
def about_me():
    return render_template("about_me.html")