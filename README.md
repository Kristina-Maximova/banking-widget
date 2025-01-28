# Banking widget

## *Краткое описание проекта*

Проект содержит функции, отдающие по запросу обработанную 
информацию о транзакциях, курсах валют, стоимости акций.

## *Установка и использование*

+ клонируйте репозиторий: [GitHub](https://github.com/Kristina-Maximova/banking-widget)
+ установите зависимости: 
  - python = "^3.13"
  - requests = "^2.32.3"
  - pandas = "^2.2.3"
  - openpyxl = "^3.1.5"

## *Примеры использования*

Пример Json - ответа по заданной дате: 
```commandline
{
    "greeting": "Доброе утро",
    "cards": [
        {
            "last_digits": "7197",
            "total_spent": 36766.89,
            "cashback": 367.67
        },
        {
            "last_digits": "4556",
            "total_spent": 1550.0,
            "cashback": 15.5
        }
    ],
    "top_transactions": [
        {
            "date": "23.07.2021",
            "amount": 96099.94,
            "category": "Переводы",
            "description": "Перевод Кредитная карта. ТП 10.2 RUR"
        },
        {
            "date": NaN,
            "amount": 90000.0,
            "category": "Переводы",
            "description": "Перевод с карты"
        },
        {
            "date": NaN,
            "amount": 90000.0,
            "category": "Переводы",
            "description": "Перевод с карты"
        },
        {
            "date": "09.07.2021",
            "amount": 13042.75,
            "category": "ЖКХ",
            "description": "ЖКУ Квартира"
        },
        {
            "date": "09.07.2021",
            "amount": 11148.96,
            "category": "ЖКХ",
            "description": "ЖКУ Квартира"
        }
    ],
    "stock_prices": [
        {
            "stock": "AAPL",
            "price": 239.44
        },
        {
            "stock": "AMZN",
            "price": 239.56
        },
        {
            "stock": "GOOGL",
            "price": 194.41
        },
        {
            "stock": "MSFT",
            "price": 443.18
        },
        {
            "stock": "TSLA",
            "price": 390.29
        }
    ]
}

```

пример json-ответа по инвест_накоплениям:
```commandline
{
    "investment": 1901.52
}

```

## *Тестирование*

+ Проводится на базе фреймворка  **` pytest `**
+ Целевое покрытие кода тестами: не менее 80%.
