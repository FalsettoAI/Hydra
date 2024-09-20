import json
import csv

data = json.load(open('data_full.json'))

data = data['val'] + data['oos_val']

filtered_list = [item for item in data if item[1] not in ['restaurant_reservation', 'cancel_reservation', 'accept_reservations', 'meal_suggestion', 'restaurant_suggestion', 'pay_bill', 'cancel', 'repeat', 'how_busy', 'order_status', 'confirm_reservation', 'restaurant_reviews', 'order', 'thank_you', 'yes', 'are_you_a_bot', 'no', 'ingredient_substitution', 'ingredients_list', 'directions', 'what_is_your_name', 'what_can_i_ask_you', 'greeting', 'goodbye']]

print(filtered_list[0])
# Write data to CSV file
with open('out-of-scope.txt', mode='w') as file:
    for item in filtered_list:
        file.write(item[0] + '\n')