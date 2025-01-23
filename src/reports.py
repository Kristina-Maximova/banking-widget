import json


data = {
    "user_currencies": [
        "USD",
        "EUR"
    ],
    "user_stocks": [
        "AAPL",
        "AMZN",
        "GOOGL",
        "MSFT",
        "TSLA"
    ]
}

with open(r"..\data\user_settings.json", "w", encoding="utf-8") as f:
    json.dump(data, f)