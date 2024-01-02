from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileRequired, FileAllowed, FileSize
from wtforms.fields import StringField, SubmitField, TextAreaField, PasswordField, RadioField, DateField, SelectMultipleField
from wtforms.validators import DataRequired, length, equal_to

class AddWriterCategory(FlaskForm):
    name = StringField("კატეგორიის სახელი", validators=[DataRequired(message="ადმინო, კატეგორიის სახელი ნუ გავიწყდებათ!")])
    submit = SubmitField("დამატება")


class EditProductForm(FlaskForm):
    name = StringField("მწერლის სახელი")
    img = FileField("მწერლის სურათი",
                    validators=[
                        FileAllowed(["jpg", "png", "jpeg"], message="ადმინო, სურათი მიიღება მხოლოდ შემდეგ ფორმატებში: 'jpg', 'jpeg' ან 'png'"),
                        FileSize(max_size= 1024*1024*4, message="ადმინო, ეს სურათი აღემატება 4MB-ს, გთხოვთ აირჩიოთ სხვა სურათი!")])
                      
    description = TextAreaField("მწერლის დახასიათება")
    category = RadioField("აირჩიეთ მწერლის კატეგორია", choices=[(1, "ქართველი"), (2, "უცხოელი")], validators=[DataRequired(message="ნუ გავიწყდებათ კატეგორიის არჩევა")])

    submit = SubmitField("დამატება")


class AddProductForm(FlaskForm):
    name = StringField("მწერლის სახელი", validators=[DataRequired(message="ადმინო, სახელი ნუ გავიწყდებათ!")])
    img = FileField("მწერლის სურათი", 
                    validators=[
                        FileRequired(message="ადმინო, სურათის ატვირთვა ნუ გავიწყდებათ!"),
                        FileAllowed(["jpg", "png", "jpeg"], message="ადმინო, სურათი მიიღება მხოლოდ შემდეგ ფორმატებში: 'jpg', 'jpeg' ან 'png'"),
                        FileSize(max_size= 1024*1024*4, message="ადმინო, ეს სურათი აღემატება 4MB-ს, გთხოვთ აირჩიოთ სხვა სურათი!")])
                      
    description = TextAreaField("მწერლის დახასიათება", validators=[DataRequired(message="ადმინო, აღწერის დაწერა ნუ გავიწყდებათ!")])
    category = RadioField("აირჩიეთ მწერლის კატეგორია", choices=[(1, "ქართველი"), (2, "უცხოელი")], validators=[DataRequired(message="ნუ გავიწყდებათ კატეგორიის არჩევა")])

    submit = SubmitField("დამატება")


class RegisterForm(FlaskForm):
    username = StringField("სახელი:", validators=[DataRequired(message="ნუ გავიწყდებათ სახელის დაწერა!")])
    password = PasswordField("პაროლი: ", validators=[length(min=8, max=30), DataRequired(message="ნუ გავიწყდებათ პაროლის დაწერა")])
    repeat_password = PasswordField("გაიმეორეთ პაროლი: ", validators=[equal_to("password", message="პაროლები ერთმანეთს უნდა ემთხვეოდეს! სცადეთ თავიდან")])
    sex = RadioField("სქესი", choices=["მდედრობითი", "მამრობითი", "სხვა"])
    birthday = DateField("დაბადების წელი")

    submit = SubmitField("დარეგისტრირება")

class LoginForm(FlaskForm):
    username = StringField("სახელი:", validators=[DataRequired(message="ნუ გავიწყდებათ სახელის დაწერა!")])
    password = PasswordField("პაროლი:", validators=[length(min=8, max=30), DataRequired(message="ნუ გავიწყდებათ პაროლის დაწერა!")])
    submit = SubmitField("ავტორიზაცია")

class CommentForm(FlaskForm):
    content = TextAreaField("კომენტარი", validators=[DataRequired(message="კომენტარის დაწერისას აუცილებელია დაწეროთ მინიმუმ ერთი სიტყვა მაინც!")])
    # author = StringField("ავტორი")
    submit = SubmitField("დამატება")