import vk_api
from vk_api.longpoll import VkLongPoll, VkEventType

def get_post(link): # инфа о посте
    link = link.split("wall")[1] # получаем айди стены и поста через _ (было vk.com/wall-162028149_588640 - стало 162028149_588640)
    wall, post = link.split("_") # отделяем их друг от друга
    return wall, post

def get_msgs(filename = "msgs.mudr"): # получаем сообщения
    db = open(filename, mode='r')
    msgs = db.read().split(';')
    for msg in msgs:
        if msg.startswith('//'):
            chmsg = msg.split('\n')[1]
            index = msgs.index(msg)
            msgs.remove(msg)
            msgs.append(chmsg)
        elif msg == "": # убираем последнее сообщение из-за ; в конце(её можно кста на ставить в конце)
            msgs.remove(msg)
    return msgs

#чтение файла c токенами
def get_tokens(filename = "tokens.mudr"):
    db = open(filename, mode="r")
    tokens = db.read().split('\n')
    comments = []
    for word in tokens:             #убираем комментарии
        if word.startswith('//'):
            comments.append(word)
        elif word == "": 
            comments.append(msg)
    for comment in comments:
        tokens.remove(comment)
    tokens = list(set(tokens)) # убираем повторы
    print(f"Количество токенов - {len(tokens)}")
    if len(tokens) <= 0:
        print("Нету токенов! Добавьте их в tokens.islam и запустите программу снова")
        exit(1)
    db.close()
    return tokens

#Проверка токенов
def checking(tok):
    check = False
    vk = vk_api.VkApi(token = tok).get_api()
    print("Проверка токена...")
    try: # проверка токенов
        vk.account.getInfo()
        check = True
    except:
        print(f"{tok} токен не верен!")
        delete = 'y'
        delete = input("Удалить данный токен из конфига? (Y\\n): ").lower()
        if delete == 'n':
            print("Пропускаем...")
            return
        with open("tokens.mudr", "r") as f:
            lines = f.readlines() # читаем файл в переменную f
        with open("tokens.mudr", "w") as f:
            for line in lines:
                if line.strip("\n") != tok: # записываем файл обратно, НО если это тот токен то убираем
                    f.write(line)
        
    if check: print("Токен верен!")

def mydromet(tokens, wall, post, msgs):
    for tok in tokens:
        vk = vk_api.VkApi(token = tok).get_api()
        for msg in msgs: # каждое сообщение
            vk.wall.createComment(
                owner_id=wall,
                post_id=post,
                message=msg
            )
            


def main():
    print("\t---МУДРОКОМ---\ngithub.com/kravandir")
    msgs = get_msgs()
    tokens = get_tokens()
    print(tokens)
    check = 'y'
    check = input("Запустить проверку токенов? (Y\\n): ").lower()
    if check == 'y':
        for token in tokens:
            checking(token)
    post = input("Введите полную ссылку на пост: ")
    wall, post = get_post(post)
    #print("проверка :", wall, post, msgs) # в случае неисправности уберите хэштег где print и напишите vk.com/klm/andrey или же создайте issue на гитхабе приложив это
    print("Начинаем...")
    mydromet(tokens, wall, post, msgs)
    print("Если нет ошибок то всё прошло успешно! Спасибо за использование!")


if __name__ == '__main__':
    main()
