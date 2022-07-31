"""
    render_template: dùng cho việc hiển thị file html (có thể thêm tham số) => dùng trực tiếp trên path
    redirect: dùng cho việc chuyển hướng trang - kèm theo use_for(tên_hàm, giá trị các biến nếu có)
    request: nhận thông tin từ phía người dùng truyền đến
    flash: tạo tin nhắn thông báo (tùy chỉnh lúc sử dụng)
    
    session: sử dụng cho việc tạo phiên đăng nhập, không cho phép đăng nhập chồng lặp
    timedelta: thiết lập thời gian giới hạn cho một phiên đăng nhập (tự thoát khỏi ứng dụng)
    
    flask_sqlalchemy: thư viện hỗ trợ sử dụng SQLAlchemy của Flask
    SQLAlchemy: ORM dạng Data Mapper
    
    path: sử dụng để lấy đường dẫn gốc
"""     
from datetime import timedelta
from flask import Flask, flash, render_template, redirect, url_for, request, session
from flask_sqlalchemy import SQLAlchemy
from os import path


app = Flask(__name__)

# key for session
app.config["SECRET_KEY"] = "SUNFLYNF"
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///data/user.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False # Theo dõi thông tin (bao gồm warning)
# timeout for session
app.permanent_session_lifetime = timedelta(minutes=10)


# Khai báo databases
db = SQLAlchemy(app)


# region entities
"""
    Sử dụng trực tiếp class làm dòng trong bảng
    - <Model>.query.<lệnh>[.<lựa chọn dòng>]
    - db.query(<Model>).<lệnh>[.<lựa chọn dòng>]
    
    Việc tương tác thực hiện trực tiếp trên class
    - Lấy toàn bộ dòng: User.query.all() hoặc db.query(User).all()
    - Lấy theo điều kiện: User.query.filter_by(thuộc_tính_1=giá_trị_1, thuộc_tính_2=giá_trị_2).first(), có thể thay first thành all, count
    - Thêm: db.session.add(user) => db.session.commit()
    - Sửa:
        1. Thay đổi trực tiếp thông tin user (xem như thay đổi trực tiếp dòng)
        2. db.session.commit()
    - Xóa: db.session.delete(user) hoặc User.query.filter_by(username=user.username).delete() => db.session.commit()
"""
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), unique=False, nullable=False)
    email = db.Column(db.String(255), unique=True, nullable=False)
    phone = db.Column(db.String(12), unique=False, nullable=False)
    username = db.Column(db.String(30), unique=True, nullable=False)
    password = db.Column(db.String(30), unique=False, nullable=False)
    job = db.relationship('Job', backref='person', lazy=True)
    
    def __init__(self, name, email, phone, username, password):
        self.name = name
        self.email = email
        self.phone = phone
        self.username = username
        self.password = password
        
        
class Job(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=True)
    title = db.Column(db.String(255), unique=False, nullable=False)
    content = db.Column(db.Text, unique=False, nullable=True)
    complete = db.Column(db.Boolean, default=False)
    
    def __init__(self, user_id, title, content):
        self.user_id = user_id
        self.title = title
        self.content = content
        self.complete = False
# endregion


if not path.exists("data/user.db"):
    db.create_all(app=app) 


# region controller Basic_and_User
@app.errorhandler(404)
def page_not_found(error):
    return render_template('404.html')


@app.route('/')
def home_page():
    if "username" in session:
        user = User.query.filter_by(username=session["username"]).first()
        job_list = Job.query.filter_by(user_id=user.id).all()
    else:
        job_list = []
    return render_template('index.html', job_list=job_list)


@app.route('/admin')
def admin_page():
    if "username" in session and session["username"] == "admin":
        list = User.query.all()
        return render_template('admin.html', list_user=list)
    return redirect(url_for('home_page')) 


@app.route('/user', methods=['GET', 'POST'])
def user_page():
    if request.method == 'POST':
        pass
    if 'username' in session:
        username = session['username']
        user = User.query.filter_by(username=username).first()
        return render_template('user.html', user=user)
    else:
        flash('You need to login first!', 'info')
    return redirect(url_for('login'))
    
    
# @app.route('/profile/<int:user_id>')
# def user_profile(user_id):
#     return '<h1>Your user id: {user_id}</h1>'.format(user_id=user_id)    


@app.route('/login', methods=['GET', 'POST'])
def login():
    # Xây dựng phương thức khi đăng nhập
    # POST được thiết lập khi người dùng nhấn phím Submit trên form
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        session.permanent = True        
        # Kiểm tra vai trò người dùng
        if username == 'admin' and password == 'admin':
            session['username'] = username
            return redirect(url_for('admin_page'))
        
        #Kiểm tra thông tin người dùng
        user_found = User.query.filter_by(username=username, password=password).first()
        if user_found:
            session['username'] = username
            return redirect(url_for('user_page'))
        else:
            flash('Invalid username or password!', 'error')
            
    # Kiểm tra phiên đăng nhập đã có người dùng chưa (đã khởi tạo)
    if "username" in session:
        username = session['username']
        flash ('You already login!', 'info') # Message
        return redirect(url_for('user_page'))
    return render_template('login.html')


@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':    
        name = request.form["fullname"]
        email = request.form["email"]
        phone = request.form["phone"]
        username = request.form['username']
        password = request.form['password']
        confirm_password = request.form['confirm_password']
        # Kiểm tra thông tin: mật khẩu xác thực
        if password != confirm_password:
            flash ('Confirmed password not correct!', 'info')
        else:
            # Kiểm tra thông tin: tên người dùng hoặc email đã tồn tại?
            if User.query.filter_by(username=username).first():
                flash('Your username is already taken!', 'info')
            elif User.query.filter_by(email=email).first():
                flash('Your email username is already taken!', 'info')
            else:
                user = User(name, email, phone, username, password)
                db.session.add(user) # thêm dữ liệu
                db.session.commit() # xác nhận thêm
                return redirect(url_for('login'))
            
    if "username" in session:
        username = session["username"]
        # Kiểm tra người dùng đang đăng nhập
        flash ('You need to log out first!', 'info')
        return redirect(url_for('user_page'))   
    return render_template('register.html')


@app.route('/logout')
def logout():
    # Thiết lập cho việc kết thúc phiên đăng nhập
    session.pop('username', None)
    return redirect(url_for('login'))


@app.route('/delete')
def delete_user():
    if session["username"] == "admin":
        return redirect(url_for('home_page'))
    User.query.filter_by(username=session['username']).delete()
    db.session.commit()
    session.pop('username', None)
    flash('User deleted successfully! Hope to see you soon!', 'info')
    return redirect(url_for('login'))
# endregion


# region controller Job_list
@app.route('/add_job', methods=['POST'])
def add_job():
    # Kiểm tra đăng nhập
    if not "username" in session:
        flash('You need to login to use this feature!', 'error')
        return redirect(url_for('login'))
    
    title = request.form.get('title')
    content = request.form.get('content')
    user = User.query.filter_by(username=session['username']).first()
    new_job = Job(user_id=user.id, title=title, content=content)
    db.session.add(new_job)
    db.session.commit()
    return redirect(url_for('home_page'))


@app.route('/update_job/<int:job_id>')
def update_job(job_id: int):
    job = Job.query.filter_by(id=job_id).first()
    job.complete = not job.complete
    db.session.commit()
    return redirect(url_for('home_page'))
    

@app.route('/delete_job/<int:job_id>')
def delete_job(job_id: int):
    Job.query.filter_by(id=job_id).delete()
    db.session.commit()
    return redirect(url_for('home_page'))
# endregion


# if __name__ == '__main__':
#     # Kiểm tra databases và khởi tạo nếu chưa có
#     if not path.exists("data/user.db"):
#         db.create_all(app=app)    
#     app.run(debug=True)