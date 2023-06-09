# game

Список участников проекта: Анастасия Кленова, Илья Молодцов, Анна Казакова и Алеся Воинская.

Описание игры:
Мы создали игру-платформер с помощью библиотеки pygame и графического редактора Tiled (Tiled Map Editor).
С помощью клавиш w, a, d, а также с помощью стрелок на клавиатуре можно двигаться и прыгать. При этом на пути будут встречаться враги. Прыгнув на них,
главный герой сможет их убить, и враги исчезнут. Однако врагов-грибов так просто не победить. Для победы над ними нужно прыгнуть на левую верхнюю часть шляпки.
Любое соприкосновение с врагами наносит урон главному герою, однако при взаимодействии с грибом здоровье уменьшается только если коснуться верхней левой части шляпки. Это связано с особенностями Tiled, где изображение врага прикрепляется к отдельному "блоку". Шкала здоровья и счётчик монет главного героя находятся в левой верхней части экрана. При падении в пропасть,которая находится между блоками, главный герой погибает. Задача пользователя - добраться до конца и собрать зелёный кристалл, после чего игра завершится.

Структура репозитория:
Наш проект разделился на 2 большие части. 

Первая часть - черновая. 
Она назвается game_draft, есть как обычная папка, так и зип-папка для более быстрого скачивания и ознакомления. Для запуска нужно запустить файл gamepr.py.
В черновом варианте мы создали некое подобие игры и реализовали врагов. Движение игрока там тоже контролируется кнопками w, a, d и стрелками, при этом игрок может стрелять, нажав на клавишу B, а враги ведут себя по-разному: черный враг ходит из стороны в сторону по назначенной траектории, гриб стоит и при этом стреляет в одном направлении, зелёный враг летает из стороны в сторону по заданной траектории, а красный враг ходит в назначенном месте, но, когда игрок приближается к нему на достаточное расстояние, начинает бежать за игроком, преследуя его. В левом верхнем углу у главного героя есть жизни, количество которых при получении урона уменьшается, а в правом нижнем углу лежит ещё одна жизнь, которую игрок может собрать для регенерации. Мы отказались от этой игровой папки, потому что в силу особенностей кода в ней невозможно было реализовать полноценный уровень с блоками и меняющимися врагами. Поэтому мы создали новый файл, в котором используем более сложные методы и более сложную структуру кода. Об этом файле и пойдёт дальше речь.

Вторая часть - окончательная.
Она называется game_final. Так же как и первый код, окончательная папка игры есть и в обычном виде, и в виде zip-папки. Для запуска окончательного варианта игры нужно пройти в code/main.py и запустить этот файл.
В последней части мы писали код, который устроен намного сложнее, чем в первой. В частности, в отличие от первого кода, в окончательном варианте широко использовалось ООП. Также там появились блоки и полноценная карта уровня, сделанная с помощью редактора уровней Tiled (Tiled Map Editor) и внедрённая в код. Мы добавили туда еще много новых элементов, например, мы внедрили новую шкалу здоровья, счетчик монет, гравитацию, промежуточные стадии экрана (меню, объяснение управления, окно выигрыша и окно проигрыша) и т.п. Мы также сочли, что в новом варианте игры убийство врагов прыжками будет более уместно, чем стрельба, поэтому реализовали урон от прыжков. В остальном описание окончательной версии игры соответствует строкам 6-9 выше.

Источники, которыми мы пользовались:

Мы смотрели многочисленные туториалы, в частности:
1. https://www.youtube.com/playlist?list=PLjRuaCofWO0O8qv2or33DGHpQ6kN_CATM (пользовались в основном при создании чернового файла)
Создаётся игра наподобие динозаврика Google. Активно используются классы, что помогает реализовывать многие сложные вещи, при этом реализуется очень много важных и полезных для игр тонкостей (например, смена темы уровня, игровое меню, реализация жизней игрока, ввод текста в игре).

2. https://youtube.com/playlist?list=PLDyJYA6aTY1mLtXrGH55paZHFjpqHdDol (пользовались в основном при создании чернового файла)
Также создается простая игра наподобие динозаврика Google с некоторыми изменениями. Хорошо и понятно объясняются базовые элементы, есть много полезных деталей. Однако классы и функции в коде почти не используются, что является огромным минусом и мешает реализовывать более сложные идеи для игры.

3. https://youtube.com/playlist?list=PL8ui5HK3oSiGXM2Pc2DahNu1xXBf7WQh- (пользовались при создании окончательного файла)
Наш ОСНОВНОЙ источник. Создается платформер, рассматривается работа с Tiled, реализуется много сложных элементов, при этом активно используются классы и функции. Однако, впрочем, наша игра во многом очень сильно отличается от того, что показано в этой серии туторилов.

4. https://youtu.be/AY9MnQ4x3zk
Гайд по основам pygame от ютубера из пункта 1.

5. https://www.youtube.com/watch?v=OAH8K5lVYOU&t=381s 
Туториал по созданию эффекта параллакса при движении главного героя

Также мы мельком просмотрели следующие видео, но не использовали их активно
https://youtu.be/B6DrRN5z_uU
https://youtube.com/playlist?list=PLjcN1EyupaQm20hlUE11y9y8EY2aXLpnv

Привидение и все враги были нарисованы и проанимированы нами вручную, всё остальное было взято из материалов к туториалам. Соответственно, под каждым видео у каждого туторила есть материалы по расказанному, у кого-то это ссылка на гитхаб, у кого-то - ссылка на собственный сайт, а у кого-то - ссылка на папки в гугл-диске.

Ссылка на редактор уровней, которым мы пользовались (для запуска файлов игры он не нужен):
https://www.mapeditor.org/

Приятной игры!
