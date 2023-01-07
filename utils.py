import json


def posts_wish_teg(content, key_name='content'):
    """
    Принимает список из словарей и ключ поля,
    ищет в элементе словаря с ключем  key_name слова начинающиеся с #
    записывает такие слова в список
    довляет этот список в славарь и выводит его
    :param content:
    :param key_name:
    :return post_wish_teg:
    """
    for post in content:
        teg_words = []
        if '#' in post[key_name]:
            word_in_post = post[key_name].split(" ")
            for word in word_in_post:
                if word[0] == '#':
                    teg_words.append(word[1:])
        post['teg_words'] = teg_words
    post_wish_teg = content
    return post_wish_teg


def read_file(file_name):
    """
    Читает файл file_name
    :param file_name:
    :return:
    """
    with open(file_name, 'r', encoding="utf-8") as file:
        raw_content = file.read()
        content = json.loads(raw_content)
    return content


def write_file_json(file_name, content):
    """
    Переписывает файл file_name данными content
    :param file_name:
    :param content:
    :return:
    """
    with open(file_name, 'w', encoding="utf-8") as file:
        json.dump(content, file, ensure_ascii=False)


def add_post_in_bookmarks(post, file_name='data/bookmarks.json'):
    """
    Добавляет данные post в файл file_name
    :param post:
    :param file_name:
    :return:
    """
    content = read_file(file_name)
    if post['pk'] not in unique_values(content, 'pk'):
        content.append(post)
        write_file_json(file_name, content)


def del_post_from_bookmarks(post_id, file_name='data/bookmarks.json'):
    """
    Удаляет пост по его ID
    :param post_id:
    :param file_name:
    :return:
    """
    content = read_file(file_name)
    if post_id in unique_values(content, 'pk'):
        new_content = []
        for post in content:
            if post['pk'] != post_id:
                new_content.append(post)
        write_file_json(file_name, new_content)


def unique_values(values, key):
    """
    В списке из словарей ищет элемент с ключем key
    и возвращает уникальные элементы
    :param values:
    :param key:
    :return:
    """
    data_list = []
    for value in values:
        data_list.append(value[key])
    unique_value = set(data_list)
    return unique_value


class Posts:
    """
    Класс для работы с постами
    """

    def __init__(self, file_name):
        content = read_file(file_name)
        unique_users_name = unique_values(content, 'poster_name')
        unique_post_id = unique_values(content, 'pk')

        self.content = content
        self.unique_users_name = unique_users_name
        self.unique_post_id = unique_post_id
        self.file_name = file_name

    def get_posts_all(self):
        """Выводит все посты"""
        return self.content

    def all_posts_id(self):
        """Выводит все уникальные id постов"""
        return self.unique_post_id

    def get_posts_by_user(self, user_name):
        """Выводит посты пользователя по его имени
        , если имя не существует выдает ошибку"""
        if user_name in self.unique_users_name:
            post_for_user = []
            content = self.content
            for post in content:
                if post['poster_name'].lower() == user_name.lower():
                    post_for_user.append(post)
            return post_for_user
        raise ValueError(f'Пользователя с именем {user_name} не существует')

    def search_for_posts(self, query):
        """Выводит посты в тексте которых присутствует query"""
        posts_for_query = []
        content = self.content
        for post in content:
            if query.lower() in post['content'].lower():
                posts_for_query.append(post)
        return posts_for_query

    def get_post_by_pk(self, post_id):
        """Выводит пост по id"""
        content = self.content
        for post in content:
            if post['pk'] == post_id:
                return post


class Comments:
    """Класс для работы с комментариями"""

    def __init__(self, file_name):
        content = read_file(file_name)
        self.content = content

    def get_comments_all(self):
        """Выводит все комментарии"""
        return self.content

    def get_comments_by_post_id(self, post_id, all_posts_id):
        """Выводит коментарии к посту по его id
        если поста с таким id нет выводит ошибку"""
        if post_id in all_posts_id:
            content = self.get_comments_all()
            comments_for_post_id = []
            for comment in content:
                if comment['post_id'] == post_id:
                    comments_for_post_id.append(comment)
            return comments_for_post_id
        raise ValueError(f'Поста с id {post_id} не существует')
