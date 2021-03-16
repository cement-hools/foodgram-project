## Foodgram
<!---
https://github.com/cement-hools/foodgram-project/workflows/foodgram/badge.svg
--->
![yamdb%20workflow Actions Status](https://github.com/cement-hools/foodgram-project/workflows/foodgram%20workflow/badge.svg)

Это онлайн-сервис, где пользователи смогут публиковать рецепты, 
подписываться на публикации других пользователей, 
добавлять понравившиеся рецепты в список «Избранное», 
а перед походом в магазин скачивать сводный список продуктов, 
необходимых для приготовления одного или нескольких выбранных блюд.

### Сервис расположен по адресу: http://cement-yatube.tk

## Установка
#### Для установки потребуется
- Docker ([установка](https://docs.docker.com/engine/install/))

#### Процесс установки и запуска

- склонируйте проект с реппозитория GitHub
    ```
    git clone https://github.com/cement-hools/foodgram-project
    ```
- перейдите в директорию foodgram-project
    ```
    cd foodgram-project
    ```
- запустите docker-compose
    ```
    docker-compose up
    ```
 - выполните миграции
    ```
    docker-compose exec web python manage.py migrate
    ```   
 - заполнить базу данных
    ```
    docker-compose exec web python manage.py loaddata fixture.json
   ```   
 - создать суперпользователя
    ```
    docker-compose exec web python manage.py createsuperuser
    ```  
    Введите username, email, password<br><br>
- после установки перейдите в браузре на http://localhost