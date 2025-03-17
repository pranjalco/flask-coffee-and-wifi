from flask import Flask, abort, render_template, redirect, url_for, flash, request
from flask_bootstrap import Bootstrap5
import csv
from forms import LoginForm, RegisterForm, CafeForm
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import relationship, DeclarativeBase, Mapped, mapped_column
from sqlalchemy import Integer, String, Text
from functools import wraps
from flask_login import UserMixin, login_user, LoginManager, current_user, logout_user, login_required
from werkzeug.security import generate_password_hash, check_password_hash

'''
8-2-2025
project 35
On Windows type:
python -m pip install -r requirements.txt
'''

app = Flask(__name__)
app.config['SECRET_KEY'] = '8BYkEfBA6O6donzWlSihBXox7C0sKR6b'
# bootstrap = Bootstrap5(app)
Bootstrap5(app)

login_manager = LoginManager()
login_manager.init_app(app)


# Creating user loader callback
@login_manager.user_loader
def load_user(user_id):
    return db.session.get(User, user_id)


# Creating database
class Base(DeclarativeBase):
    pass


app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///cafe_data.db'
db = SQLAlchemy(model_class=Base)
db.init_app(app)


class User(UserMixin, db.Model):
    __tablename__ = "users"
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(String(250), nullable=False)
    email: Mapped[str] = mapped_column(String(250), unique=True, nullable=False)
    password: Mapped[str] = mapped_column(String(250), nullable=False)

    bookmarks = relationship("Bookmark", back_populates="parent_user")


class Cafe(db.Model):
    __tablename__ = "cafes"
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    cafe_name: Mapped[str] = mapped_column(String(250), nullable=False)
    location: Mapped[str] = mapped_column(String(500), nullable=False)
    open_time: Mapped[str] = mapped_column(String(50), nullable=False)
    close_time: Mapped[str] = mapped_column(String(50), nullable=False)
    coffee: Mapped[str] = mapped_column(String(10), nullable=False)  # Storing ☕️☕️☕️ etc.
    wifi: Mapped[str] = mapped_column(String(10), nullable=False)  # Storing 💪💪💪 etc.
    power: Mapped[str] = mapped_column(String(10), nullable=False)  # Storing 🔌🔌🔌 etc.

    bookmarks = relationship("Bookmark", back_populates="parent_cafe")

    def to_dict(self):
        return {column.name: getattr(self, column.name) for column in self.__table__.columns}


class Bookmark(db.Model):
    __tablename__ = "bookmarks"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)

    user_id: Mapped[int] = mapped_column(Integer, db.ForeignKey("users.id"), nullable=False)
    cafe_id: Mapped[int] = mapped_column(Integer, db.ForeignKey("cafes.id"), nullable=False)

    parent_user = relationship("User", back_populates="bookmarks")
    parent_cafe = relationship("Cafe", back_populates="bookmarks")


with app.app_context():
    db.create_all()


# all Flask routes below
@app.route("/")
def home():
    return render_template("index.html")


@app.route('/add', methods=["GET", "POST"])
def add_cafe():
    if not current_user.is_authenticated:
        flash("Please login here to add new cafe.")
        return redirect(url_for('login'))
    form = CafeForm()
    if form.validate_on_submit():
        cafe_name = form.cafe.data
        location = form.location.data
        open = form.open_time.data
        close = form.close_time.data
        coffee_rating = form.coffee_rating.data
        wifi_rating = form.wifi_rating.data
        power_socket = form.power_socket.data
        # add_data_csv(cafe_name, location, open, close, coffee_rating, wifi_rating, power_socket)

        new_cafe = Cafe(cafe_name=cafe_name,
                        location=location,
                        open_time=open,
                        close_time=close,
                        coffee=coffee_rating,
                        wifi=wifi_rating,
                        power=power_socket)

        db.session.add(new_cafe)
        db.session.commit()

        print("True")
        return redirect(url_for("cafes"))

    # Exercise:
    # Make the form write a new row into cafe-data.csv
    # with   if form.validate_on_submit()
    return render_template('add.html', form=form)


@app.route('/cafes')
def cafes():
    all_cafes = db.session.execute(db.select(Cafe)).scalars().all()
    # for cafe in all_cafes:
    #     print(cafe.to_dict())

    if not all_cafes:
        flash("Please add new cafe from here, right now no cafe is added to cafe list.")
        return redirect(url_for('add_cafe'))

    return render_template('cafes.html', all_cafes=all_cafes, current_user=current_user)


@app.route("/login", methods=["GET", "POST"])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        email = form.email.data
        password = form.password.data
        user = db.session.execute(db.select(User).where(User.email == email)).scalar()

        if not user:
            flash("This email does not exist, please try again.")
            return redirect(url_for("login"))
        elif not check_password_hash(user.password, password):
            flash("Password is incorrect, please try again.")
            return redirect(url_for("login"))
        else:
            login_user(user)
            return redirect(url_for("home"))
    return render_template("login.html", form=form, current_user=current_user)


@app.route('/register', methods=["GET", "POST"])
def register():
    form = RegisterForm()
    if form.validate_on_submit():
        email = form.email.data
        check_mail_present = db.session.execute(db.select(User).where(User.email == email)).scalar()
        if check_mail_present:
            flash("You already did signed up with this email, instead using this email login here!")
            return redirect(url_for('login'))

        hash_and_salted_password = generate_password_hash(
            form.password.data,
            method='pbkdf2:sha256',
            salt_length=8
        )
        new_user = User(
            email=form.email.data,
            name=form.name.data,
            password=hash_and_salted_password
        )
        db.session.add(new_user)
        db.session.commit()

        # This line will authenticate the user with Flask-Login
        login_user(new_user)
        return redirect(url_for("home"))
    return render_template("register.html", form=form, current_user=current_user)


@app.route("/bookmarks")
def bookmarks():
    if not current_user.is_authenticated:
        flash("Please login here to see your bookmarks.")
        return redirect(url_for('login'))

    # Get the logged-in user's bookmarked cafes
    result = db.session.execute(db.select(Cafe).join(Bookmark).filter(Bookmark.user_id == current_user.id))
    bookmarked_cafe = result.scalars().all()
    if not bookmarked_cafe:
        flash("You did not have added any bookmarks to your list, please add first by clicking on 🔖 on See all cafe page.")
        return render_template("bookmarks.html", current_user=current_user, all_cafes=False)
    return render_template("bookmarks.html", current_user=current_user, all_cafes=bookmarked_cafe)


@app.route("/add_bookmark/<int:cafe_id>")
@login_required
def add_bookmark(cafe_id):
    # Check if bookmark is present or not
    existing_bookmark = db.session.execute(
        db.select(Bookmark).filter_by(cafe_id=cafe_id, user_id=current_user.id)).first()

    if existing_bookmark:
        flash("This bookmark already present")
        print("Yes")
        return redirect(url_for('cafes'))

    else:
        new_bookmark = Bookmark(user_id=current_user.id, cafe_id=cafe_id)
        db.session.add(new_bookmark)
        db.session.commit()
        flash("Bookmark done successfully!")
        return redirect(url_for('cafes'))


@app.route("/delete_bookmark/<int:cafe_id>")
@login_required
def delete_bookmark(cafe_id):
    bookmark_to_delete = db.session.execute(db.select(Bookmark).filter(
        Bookmark.user_id == current_user.id,
        Bookmark.cafe_id == cafe_id)).scalar_one_or_none()

    db.session.delete(bookmark_to_delete)
    db.session.commit()
    flash("Bookmark removed successfully!")

    return redirect(url_for("bookmarks"))


@app.route("/logout")
def logout():
    logout_user()
    return redirect(url_for('home'))


if __name__ == '__main__':
    app.run(debug=True)
