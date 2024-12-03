# Django Catalog

Implementing a product catalog in django

## About

This is a project for a chain of furniture stores. All fields and models were made according to the technical specifications of the customer. The model diagram looks like this:

![structure image](./src/apps/main/static/main/img/model_structure.jpg)


## Running this project

To get this project up and running you should start by having Python installed on your computer. It's advised you create a virtual environment to store your projects dependencies separately. You can install virtualenv with

```
pip install virtualenv
```

Clone or download this repository and open it in your editor of choice. In a terminal (mac/linux) or windows terminal, run the following command in the base directory of this project

```
virtualenv venv
```

That will create a new folder `venv` in your project directory. Next activate it with this command on mac/linux:

```
source venv/bin/active
```

Then install the project dependencies with

```
poetry install
```


Now you can run the project with this command

```
docker-compose -f docker-compose-local.yaml up -d
```

## Features:

<ol>
    <li>Automatic generation of folders for categories and products</li>
    <li>Auto-delete on photos and folders</li>
    <li>Slug auto-generation for RU-ru</li>
    <li>ORM and SEO optimization</li>
    <li>Api for telegram bot</li>
    <li>Auto Generated thumbnails</li>
    <li>Pagination</li>
    <li>Cache</li>
</ol>

Project works in several enviroments:
* local
* development
* testing
* production

## Полезные команды

* Тестирование:

    ```bash
    pytest -v -x -n 4 src
    ```

* Форматер:

    ```bash
    black src
    ```

* Pylint:
    ```bash
    pylint --load-plugins pylint_django --django-settings-module=django_catalog.settings --fail-under=9 **/*.py
    ```

* Pre-commit
    ```bash
    pre-commit run # Вручную запускает пре комиты
    pre-commit install # Устанавлиет пре-комиты
    pre-commit autoupdate # Обновляет пакеты для пре-комитов
    ```
