from flask import Flask, request
from datetime import datetime, timedelta
import json

app = Flask(__name__)

def load_users():
    with open("users.json", "r") as f:
        return json.load(f)

def save_users(users):
    with open("users.json", "w") as f:
        json.dump(users, f, indent=2)

@app.route("/gk_callback", methods=["POST"])
def gk_callback():
    data = request.json
    if data["status"] == "paid":
        order_id = data["order_id"]
        amount = int(data["amount"])
        user_id = order_id.split("_")[0]

        tariffs = {
            5: (1, "1 день"),
            99: (30, "1 месяц"),
            499: (180, "6 месяцев"),
            799: (365, "12 месяцев")
        }

        if amount in tariffs:
            days, label = tariffs[amount]
            users = load_users()
            user = users.get(user_id)
            if user:
                expires = datetime.now() + timedelta(days=days)
                user["days"] = days
                user["tariff"] = label
                user["expires"] = expires.strftime("%Y-%m-%d")
                save_users(users)
                return "OK", 200
    return "Ignored", 200

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=10000)
