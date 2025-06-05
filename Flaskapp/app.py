# app.py
from flask import Flask, render_template, request, redirect, url_for, flash, jsonify
from datetime import datetime

app = Flask(__name__)
app.secret_key = 'HuuTin@123'  # Thay đổi key này trong production

# Dữ liệu mẫu (trong thực tế nên dùng database)
posts = [
    {
        'id': 1,
        'title': 'Chào mừng đến với Flask',
        'content': 'Đây là bài viết đầu tiên trên website Flask của chúng ta!',
        'author': 'Admin',
        'date': datetime(2025, 1, 1)
    },
    {
        'id': 2,
        'title': 'Học Flask cùng Python',
        'content': 'Flask là một micro web framework rất mạnh mẽ và dễ học.',
        'author': 'Developer',
        'date': datetime(2025, 1, 5)
    }
]

users = []  # Danh sách người dùng đăng ký

@app.route('/')
def home():
    """Trang chủ"""
    return render_template('index.html', posts=posts)

@app.route('/about')
def about():
    """Trang giới thiệu"""
    return render_template('about.html')

@app.route('/blog')
def blog():
    """Trang blog"""
    return render_template('blog.html', posts=posts)

@app.route('/post/<int:post_id>')
def post_detail(post_id):
    """Chi tiết bài viết"""
    post = next((p for p in posts if p['id'] == post_id), None)
    if not post:
        flash('Bài viết không tồn tại!', 'error')
        return redirect(url_for('blog'))
    return render_template('post_detail.html', post=post)

@app.route('/contact', methods=['GET', 'POST'])
def contact():
    """Trang liên hệ"""
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        message = request.form['message']
        
        # Trong thực tế, bạn sẽ lưu vào database hoặc gửi email
        flash(f'Cảm ơn {name}! Tin nhắn của bạn đã được gửi thành công.', 'success')
        return redirect(url_for('contact'))
    
    return render_template('contact.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    """Đăng ký người dùng"""
    if request.method == 'POST':
        username = request.form['username']
        email = request.form['email']
        password = request.form['password']
        
        # Kiểm tra xem user đã tồn tại chưa
        if any(u['username'] == username for u in users):
            flash('Tên người dùng đã tồn tại!', 'error')
        else:
            users.append({
                'username': username,
                'email': email,
                'password': password,  # Trong thực tế cần hash password
                'date_joined': datetime.now()
            })
            flash('Đăng ký thành công!', 'success')
            return redirect(url_for('home'))
    
    return render_template('register.html')

@app.route('/api/posts')
def api_posts():
    """API trả về danh sách bài viết (JSON)"""
    return jsonify([{
        'id': p['id'],
        'title': p['title'],
        'author': p['author'],
        'date': p['date'].strftime('%Y-%m-%d')
    } for p in posts])

@app.route('/add_post', methods=['GET', 'POST'])
def add_post():
    """Thêm bài viết mới"""
    if request.method == 'POST':
        title = request.form['title']
        content = request.form['content']
        author = request.form['author']
        
        new_post = {
            'id': len(posts) + 1,
            'title': title,
            'content': content,
            'author': author,
            'date': datetime.now()
        }
        posts.append(new_post)
        flash('Bài viết đã được thêm thành công!', 'success')
        return redirect(url_for('blog'))
    
    return render_template('add_post.html')

@app.errorhandler(404)
def not_found(error):
    """Trang lỗi 404"""
    return render_template('404.html'), 404

if __name__ == '__main__':
    app.run(debug=True)