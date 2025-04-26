import os
import requests
from flask import Flask, render_template, request

app = Flask(__name__)

NUTRITIONIX_API_URL = "https://trackapi.nutritionix.com/v2/natural/nutrients"
NUTRITIONIX_APP_ID = os.environ.get("759b141f")
NUTRITIONIX_API_KEY = os.environ.get("24e7d0b489aed08057df865213cac037-")

headers = {
    "x-app-id": NUTRITIONIX_APP_ID,
    "x-app-key": NUTRITIONIX_API_KEY,
    "Content-Type": "application/json"
}

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/result', methods=['POST'])
def result():
    food_item = request.form['food']
    weight = request.form['weight']
    
    try:
        response = requests.post(NUTRITIONIX_API_URL, headers=headers, json={"query": food_item})
        data = response.json()
        
        if 'foods' in data:
            food_info = data['foods'][0]
            calories_per_gram = food_info['nf_calories'] / 100
            total_calories = calories_per_gram * float(weight)
            return render_template('result.html', food=food_item, weight=weight, calories=round(total_calories, 2))
        else:
            return render_template('result.html', food=food_item, weight=weight, calories="Error, Try again!")
    except Exception as e:
        print(e)
        return render_template('result.html', food=food_item, weight=weight, calories="Error, Try again!")

@app.route('/goal', methods=['POST'])
def goal():
    choice = request.form['choice']
    if choice == 'gain':
        suggestion = "To gain weight, eat more healthy fats like avocados, nuts, peanut butter, and whole milk."
    else:
        suggestion = "To lose weight, switch to low-calorie foods like cucumbers, spinach, grilled chicken, and yogurt."
    return render_template('goal.html', suggestion=suggestion)

@app.route('/thankyou')
def thankyou():
    return render_template('thankyou.html')

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=int(os.environ.get("PORT", 5000)))
