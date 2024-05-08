from fatsecret import Fatsecret
from datetime import *
from dateutil.relativedelta import *
import pandas as pd
import time

fs = Fatsecret('consumer_key', 'consumer_secret')

auth_url = fs.get_authorize_url()

print("Browse to the following URL in your browser to authorize access:\n{}"\
    .format(auth_url))

pin = input("Enter the PIN provided by FatSecret: ")
session_token = fs.authenticate(pin)

#Iterate through months
start_date = datetime(2021, 1, 1)
end_date = datetime.now()
delta = relativedelta(months=1)
meal = []
while start_date <= end_date:
    print(start_date.strftime("%Y-%m-%d"))
    try:
        month_info=fs.food_entries_get_month(start_date)
        print(f"{start_date}\n{month_info} - end month")
        print(type(month_info))

        if month_info:
            if type(month_info) == dict:
                month_info = [month_info]
            for item in month_info:
                day = datetime(1970,1,1,0,0) + timedelta(int(item['date_int']))
                try:
                    meal.append(fs.food_entries_get(date=day))
                    print(day.strftime("%Y-%m-%d"))
                    print(meal)
                    time.sleep(10)
                except Exception as e:
                    print(f"Requests limit. Last day is: {day}")
                    print(type(e))
                    print(e.args)
                    print(e)

                    break

        start_date += delta
    except Exception as e:
        print(f"Requests limit. Last date is: {start_date}")
        print(type(e))
        print(e.args)
        print(e)
        break

df = pd.DataFrame(meal)

csv_file = 'output.csv'
df.to_csv(csv_file, index=False)