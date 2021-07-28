import json
import os

import requests
from auth_data import TOKEN


def get_wall_posts(group_name, count, version):
    url = f'https://api.vk.com/method/wall.get?domain={group_name}&count={count}&access_token={TOKEN}&v={version}'
    req = requests.get(url=url)
    src = req.json()

    # проверяем существует ли директория с именем группы
    if os.path.exists(f'{group_name}'):
        print(f'Директория с именем {group_name} уже существует')
    else:
        os.mkdir(group_name)

    # Сохраняем полученные данные в json файл, чтобы видеть структуру
    with open(f'{group_name}/{group_name}.json', 'w', encoding='utf-8') as file:
        json.dump(src, file, indent=4, ensure_ascii=False)

    # Собираем id новых постов в список
    fresh_posts_id = []
    posts = src['response']['items']

    for fresh_post_id in posts:
        fresh_post_id = fresh_post_id['id']
        fresh_posts_id.append(str(fresh_post_id))

    """Проверка, если файла не существует, значит это первый парсинг группы
    (отправляем все новые посты). Иначе начинаем проверку и отправляем
    только новые посты"""

    if not os.path.exists(f'{group_name}/exist_post_{group_name}.txt'):
        print('Файла с ID постов не существует, создаем файл!')
        with open(f'{group_name}/exist_post_{group_name}.txt', 'w') as file:
            for item in fresh_posts_id:
                file.write(str(item) + '\n')

    else:
        print('Файл с ID постов найден, начинаем выборку свежин постов!')
        history_posts = []
        with open(f'{group_name}/exist_post_{group_name}.txt', 'r') as file:
            for line in file:
                history_posts.append(line.rstrip())
        new_posts = list(set(fresh_posts_id) - set(history_posts))

        # print(f'Полученные посты из запроса: {fresh_posts_id}')
        # print(f'Посты из файла: {history_posts}')

        if not new_posts:
            print("Новых постов нет")
        else:
            print(f"Есть новые посты, вот их ID: {new_posts}")
            # Дописываем в историю новые посты
            with open(f'{group_name}/exist_post_{group_name}.txt', 'a') as file:
                for item in new_posts:
                    file.write(item + '\n')
            # Получаем информацию нового поста для дальнейших операций с новым постом:

def main():
    group_name = 'bugry_official'
    count = 10
    version = '5.52'
    get_wall_posts(group_name=group_name, count=count, version=version)


if __name__ == '__main__':
    main()