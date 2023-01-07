# Загружаем необходимые модули и функции
from flask import render_template, Blueprint, request
from json import JSONDecodeError
from utils import Posts, Comments, read_file, posts_wish_teg

# Создаем блюпринт
get_blueprint = Blueprint('get_blueprint', __name__, template_folder='templates')

# Файлы json
file_posts = 'data/posts.json'
file_comments = 'data/comments.json'
file_bookmarks = 'data/bookmarks.json'

# обрабатываем ошибки
try:
    class_posts = Posts(file_posts)
    class_comments = Comments(file_comments)
except FileNotFoundError:
    @get_blueprint.route('/')
    def error():
        return f'<a>Файл не найден</a>'
except JSONDecodeError:
    @get_blueprint.route('/')
    def error():
        return f'<a>Файл не удается преобразовать</a>'


@get_blueprint.route('/')
def posts_all():
    """Главная страница со всеми постами"""
    posts = class_posts.get_posts_all()
    cnt_bookmarks_posts = len(read_file(file_bookmarks))
    posts_with_teg = posts_wish_teg(posts)
    return render_template('index.html', posts=posts_with_teg, cnt_bookmarks_posts=cnt_bookmarks_posts)


@get_blueprint.route('/posts/<int:pk>')
def post_by_pk(pk):
    """Страница с постом по его pk"""
    post = class_posts.get_post_by_pk(pk)
    list_post = []
    list_post.append(post)
    post_with_teg = posts_wish_teg(list_post)
    comments = class_comments.get_comments_by_post_id(pk, class_posts.unique_post_id)
    cnt_comments = len(comments)
    return render_template('post.html', post=post_with_teg[0], comments=comments, cnt_comments=cnt_comments)


@get_blueprint.route('/users/<username>')
def posts_for_user(username):
    """Страница с постами пользователя по имени"""
    users_posts = class_posts.get_posts_by_user(username)
    users_posts_with_teg = posts_wish_teg(users_posts)
    return render_template('user-feed.html', posts=users_posts_with_teg, username=username)


@get_blueprint.route('/search')
def search_posts_for_query():
    """Страница с постами содержашими в тексте слово S"""
    query = request.args.get("s")
    posts = class_posts.search_for_posts(query)
    posts_with_teg = posts_wish_teg(posts)
    cnt_posts = len(posts)
    return render_template('search.html', cnt_posts=cnt_posts, posts=posts_with_teg)


@get_blueprint.route('/tag/<tag_name>')
def search_posts_for_teg(tag_name):
    """"Страница с постами по тегу"""
    query = f'#{tag_name}'
    posts = class_posts.search_for_posts(query)
    posts_with_teg = posts_wish_teg(posts)
    return render_template('tag.html', posts=posts_with_teg, query=tag_name)
