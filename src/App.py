import json
import os

import requests
from auth_data import TOKEN


def get_wall_posts_from_server(group_name, count, version):
    """Получает JSON ответ от vk_api"""

    url = f'https://api.vk.com/method/wall.get?domain={group_name}&count={count}&access_token={TOKEN}&v={version}'
    req = requests.get(url=url)
    src = req.json()
    return src

def get_wall_posts_from_json_file(group_name):
    """Читаем JSON ответ из файла"""

    with open(f'{group_name}/{group_name}.json', 'r', encoding='utf-8') as file:
        src = json.load(file)
        return src


def save_response_json_to_disk(src, group_name):
    """Сохраняет JSON ответ от vk_api на диск group_name.json"""

    # проверяем существует ли директория с именем группы
    if os.path.exists(f'{group_name}'):
        print(f'[INFO] - Директория с именем {group_name} уже существует')
    else:
        os.mkdir(group_name)

    # Сохраняем полученные данные в json файл, чтобы видеть структуру
    with open(f'{group_name}/{group_name}.json', 'w', encoding='utf-8') as file:
        json.dump(src, file, indent=4, ensure_ascii=False)
        print(f'[INFO] - {group_name}/{group_name}.json saved.')

def get_posts_ID_from_response(src_json):
    """Возвращает список из ID постов которые пришли в ответе от vk_api"""

    # Собираем id новых постов в список
    fresh_posts_id = []
    posts = src_json['response']['items']

    for fresh_post_id in posts:
        fresh_post_id = fresh_post_id['id']
        fresh_posts_id.append(str(fresh_post_id))

    return fresh_posts_id


# def get_wall_posts(group_name, count, version):


    # else:
    #     print('Файл с ID постов найден, начинаем выборку свежин постов!')
    #     history_posts = []
    #     with open(f'{group_name}/exist_post_{group_name}.txt', 'r') as file:
    #         for line in file:
    #             history_posts.append(line.rstrip())
    #     new_posts = list(set(fresh_posts_id) - set(history_posts))
    #
    #     # print(f'Полученные посты из запроса: {fresh_posts_id}')
    #     # print(f'Посты из файла: {history_posts}')
    #---
    #     if not new_posts:
    #         print("Новых постов нет")
    #     else:
    #         print(f"Есть новые посты, вот их ID: {new_posts}")
    #         # Дописываем в историю новые посты
    #         with open(f'{group_name}/exist_post_{group_name}.txt', 'a') as file:
    #             for item in new_posts:
    #                 file.write(item + '\n')
    #
    #         # Получаем информацию нового поста для дальнейших операций с новым постом:
    #         postы_to_send = []
    #
    #         for post in posts:
    #             if str(post['id']) in new_posts:
    #                 post_id = post['id']
    #                 post_date = post['date']
    #                 post_text = post['text']
    #                 post_likes = post['likes']['count']
    #                 print(f'{post_id}:{post_date}:{post_likes} - {post_text}')


def check_fresh_posts(group_name, posts_id_from_response):
    """Сравнивает список ID с exist_posts и возвращает список только тех ID постов
    которые нужно отправить пользователю."""


    """Если это первый парсинг группы то сохраняем список ID в exist_post_{group_name}.txt, 
    и возвращаем весь список как новый"""
    if not os.path.exists(f'{group_name}/exist_post_{group_name}.txt'):
        print('Файла с ID постов не существует, создаем файл!')
        with open(f'{group_name}/exist_post_{group_name}.txt', 'w') as file:
            for item in posts_id_from_response:
                file.write(str(item) + '\n')

        # Отправляем сисок всех ID постов пользователю, так как это первый парсинг группы.
        return posts_id_from_response
    else:
        """Иначе проверяем какие посты новые, возвращаем список только новых ID постов и 
        дописываем посты в exist_post_{group_name}.txt"""
        print('\n[INFO] - Файл с ID постов найден, начинаем выборку свежин постов!')
        exist_posts = []
        with open(f'{group_name}/exist_post_{group_name}.txt', 'r') as file:
            for line in file:
                exist_posts.append(line.rstrip())
        id_posts_to_send = list(set(posts_id_from_response) - set(exist_posts))

        print(f'\n[INFO] - Полученные посты из запроса: {posts_id_from_response}')
        print(f'[INFO] - NEW POSTS (ID постов для отправки пользователю): {id_posts_to_send}')

        with open(f'{group_name}/exist_post_{group_name}.txt', 'a') as file:
            for item in posts_id_from_response:
                file.write(str(item) + '\n')

        remove_duplicate_posts_history(group_name=group_name)
        return id_posts_to_send

def remove_duplicate_posts_history(group_name):
    """Удаляет дубликаты в exist_post_{group_name}.txt"""

    exist_posts = []
    with open(f'{group_name}/exist_post_{group_name}.txt', 'r') as file:
        for line in file:
            exist_posts.append(line.rstrip())
    new_list = list(set(exist_posts))

    with open(f'{group_name}/exist_post_{group_name}.txt', 'w') as file:
        for item in new_list:
            file.write(str(item) + '\n')

def main():
    group_name = 'bugry_official'
    count = 7
    version = '5.52'

    # Чтобы не спамить сервак запросами для отладки обращаемся к json файлу
    src_json = get_wall_posts_from_json_file(group_name=group_name)

    # src_json = get_wall_posts_from_server(group_name=group_name, count=count, version=version)
    # save_response_json_to_disk(src=src_json, group_name=group_name)
    posts_id_from_server_response = get_posts_ID_from_response(src_json=src_json)
    id_posts_to_send_user = check_fresh_posts(group_name=group_name, posts_id_from_response=posts_id_from_server_response)
    print(id_posts_to_send_user)



if __name__ == '__main__':
    main()