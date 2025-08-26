from flask import Flask, jsonify, request, send_from_directory, url_for
from flask_cors import CORS
from flask_jwt_extended import JWTManager, create_access_token, jwt_required, get_jwt_identity
from models import db, User, Article, Comment
from datetime import timedelta
import os

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///blog.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['JWT_SECRET_KEY'] = os.environ.get('JWT_SECRET_KEY', 'dev-secret-change-me')
app.config['JWT_ACCESS_TOKEN_EXPIRES'] = timedelta(days=7)
app.config['UPLOAD_FOLDER'] = os.path.join(os.path.dirname(__file__), 'uploads')
app.config['MAX_CONTENT_LENGTH'] = 5 * 1024 * 1024  # 5MB

# 允许本地与 ngrok 临时域名访问
# CORS(app, resources={r"/api/*": {"origins": [
#     "http://localhost:5173",
#     "http://127.0.0.1:5173",
#     r"https://.*\.ngrok-free\.app"
# ]}}, supports_credentials=True)

CORS(app)

# 初始化扩展
jwt = JWTManager(app)
db.init_app(app)

# 确保上传目录存在
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

# ---- 初始化数据库 & demo 数据 ----
def init_db():
    with app.app_context():
        db.create_all()
        if not Article.query.first():
                # 创建示例文章
                a1 = Article(title='Hello, Mini Blog', content='我的第一篇文章！')
                a2 = Article(title='开发计划', content='目标功能：文章列表、详情、登录注册、评论。')
                db.session.add_all([a1, a2])
                db.session.commit()
init_db()

# ---- 健康检查 ----
@app.get('/api/health')
def health():
    return jsonify(ok=True), 200

@app.post('/api/register')
def register():
    data = request.get_json() or {}
    username = (data.get('username') or '').strip()
    password = data.get('password') or ''
    if not username or not password:
        return jsonify(message='用户名和密码不能为空'), 400

    if User.query.filter_by(username=username).first():
        return jsonify(message='用户名已存在'), 409

    user = User(username=username)
    user.set_password(password)
    db.session.add(user)
    db.session.commit()
    return jsonify(message='注册成功'), 201

@app.post('/api/login')
def login():
    data = request.get_json() or {}
    username = data.get('username') or ''
    password = data.get('password') or ''

    user = User.query.filter_by(username=username).first()
    if not user or not user.check_password(password):
        return jsonify(message='用户名或密码错误'), 401

    token = create_access_token(identity=user.id)
    return jsonify(access_token=token, username=user.username), 200

@app.get('/api/articles')
def list_articles():
    articles = Article.query.order_by(Article.created_at.desc()).all()
    def brief(a: Article):
        text = (a.content or '')
        excerpt = (text[:120] + '...') if len(text) > 120 else text
        return {
            'id': a.id,
            'title': a.title,
            'excerpt': excerpt,
            'created_at': a.created_at.isoformat(),
            'author': a.user.username if getattr(a, 'user', None) else None
        }
    return jsonify([brief(a) for a in articles])

@app.post('/api/articles')
@jwt_required()
def create_article():
    data = request.get_json() or {}
    title = (data.get('title') or '').strip()
    content = (data.get('content') or '').strip()
    if not title or not content:
        return jsonify(message='标题和内容不能为空'), 400
    uid = get_jwt_identity()
    a = Article(title=title, content=content, user_id=uid)
    db.session.add(a)
    db.session.commit()
    return jsonify(id=a.id, message='发表成功'), 201

# ---- 用户信息 ----
@app.get('/api/me')
@jwt_required()
def get_me():
    uid = get_jwt_identity()
    u = User.query.get_or_404(uid)
    return jsonify({
        'id': u.id,
        'username': u.username,
        'avatar_url': u.avatar_url,
        'created_at': u.created_at.isoformat()
    })

@app.patch('/api/me')
@jwt_required()
def update_me():
    uid = get_jwt_identity()
    u = User.query.get_or_404(uid)
    data = request.get_json() or {}
    username = (data.get('username') or '').strip()
    avatar_url = (data.get('avatar_url') or '').strip() or None
    if username:
        if username != u.username and User.query.filter_by(username=username).first():
            return jsonify(message='用户名已存在'), 409
        u.username = username
    u.avatar_url = avatar_url
    db.session.commit()
    return jsonify(message='更新成功')

@app.post('/api/me/avatar')
@jwt_required()
def upload_avatar():
    uid = get_jwt_identity()
    u = User.query.get_or_404(uid)
    if 'file' not in request.files:
        return jsonify(message='未找到文件'), 400
    f = request.files['file']
    if not f.filename:
        return jsonify(message='文件名无效'), 400
    ext = os.path.splitext(f.filename)[1].lower()
    if ext not in ['.png', '.jpg', '.jpeg', '.gif', '.webp']:
        return jsonify(message='不支持的文件类型'), 400
    filename = f"avatar_{uid}{ext}"
    save_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
    f.save(save_path)
    # 对外可访问 URL
    public_url = url_for('serve_upload', filename=filename, _external=True)
    u.avatar_url = public_url
    db.session.commit()
    return jsonify(url=public_url, message='上传成功')

@app.get('/uploads/<path:filename>')
def serve_upload(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)

@app.get('/api/me/articles')
@jwt_required()
def my_articles():
    uid = get_jwt_identity()
    arts = Article.query.filter_by(user_id=uid).order_by(Article.created_at.desc()).all()
    return jsonify([
        {
            'id': a.id,
            'title': a.title,
            'created_at': a.created_at.isoformat()
        } for a in arts
    ])

@app.get('/api/articles/<int:aid>')
def article_detail(aid: int):
    a = Article.query.get_or_404(aid)
    return jsonify({
        'id': a.id,
        'title': a.title,
        'content': a.content,
        'created_at': a.created_at.isoformat(),
        'author': a.user.username if getattr(a, 'user', None) else None,
        'author_id': a.user.id if getattr(a, 'user', None) else None
    })

@app.patch('/api/articles/<int:aid>')
@jwt_required()
def update_article(aid: int):
    uid = get_jwt_identity()
    a = Article.query.get_or_404(aid)
    if a.user_id != uid:
        return jsonify(message='无权修改该文章'), 403
    data = request.get_json() or {}
    title = (data.get('title') or '').strip()
    content = (data.get('content') or '').strip()
    if not title or not content:
        return jsonify(message='标题和内容不能为空'), 400
    a.title = title
    a.content = content
    db.session.commit()
    return jsonify(message='更新成功')

@app.delete('/api/articles/<int:aid>')
@jwt_required()
def delete_article(aid: int):
    uid = get_jwt_identity()
    a = Article.query.get_or_404(aid)
    if a.user_id != uid:
        return jsonify(message='无权删除该文章'), 403
    db.session.delete(a)
    db.session.commit()
    return jsonify(message='删除成功')

@app.get('/api/articles/<int:aid>/comments')
def get_comments(aid: int):
    Article.query.get_or_404(aid)
    comments = Comment.query.filter_by(article_id=aid).order_by(Comment.created_at.asc()).all()
    return jsonify([
        {
            'id': c.id,
            'user': c.user.username,
            'content': c.content,
            'created_at': c.created_at.isoformat()
        } for c in comments
    ])

@app.post('/api/articles/<int:aid>/comments')
@jwt_required()
def post_comment(aid: int):
    Article.query.get_or_404(aid)
    uid = get_jwt_identity()
    data = request.get_json() or {}
    content = (data.get('content') or '').strip()
    if not content:
        return jsonify(message='评论内容不能为空'), 400
    c = Comment(article_id=aid, user_id=uid, content=content)
    db.session.add(c)
    db.session.commit()
    return jsonify(message='评论成功', id=c.id), 201

if __name__ == '__main__':
    # python backend/app.py
    app.run(host='0.0.0.0', port=5000, debug=True)