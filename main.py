import requests
from datetime import datetime
import pytz
import smtplib
import time

# -7.129749, 112.726798

MY_LAT = -7.129749 # Your latitude
MY_LONG = 112.726798 # Your longitude


parameters = {
    "lat": MY_LAT,
    "lng": MY_LONG,
    "formatted": 0,
}

response = requests.get("https://api.sunrise-sunset.org/json", params=parameters)
response.raise_for_status()
data = response.json()
sunrise = int(data["results"]["sunrise"].split("T")[1].split(":")[0])
sunset = int(data["results"]["sunset"].split("T")[1].split(":")[0])

# print(sunset, sunrise)

jakarta_tz = pytz.timezone('Asia/Jakarta')
time_now = datetime.now(jakarta_tz)


hour = time_now.hour
# print(hour)

#If the ISS is close to my current position

def is_iss_near():
    global MY_LAT, MY_LONG
    resp = requests.get(url='http://api.open-notify.org/iss-now.json')
    resp.raise_for_status()
    data_iss = resp.json()
    longitude = float(data_iss['iss_position']['longitude'])
    latitude = float(data_iss['iss_position']['latitude'])
    iss_position = (longitude, latitude)
    # print(iss_position)
    if (MY_LONG + 5) >= longitude >= (MY_LONG - 5) and (MY_LAT + 5) >= latitude >= (MY_LAT - 5):
        return True

    return False

# print(is_iss_near())

# and it is currently dark
def is_dark():
    global hour, sunset, sunrise
    if hour >= sunset or hour <= sunrise:
        return True
    return False

def main():
    my_email = 'bapakfarhan1212@gmail.com'
    password = 'rninseujddsmhixl'
    if is_dark() and is_iss_near():
        with smtplib.SMTP('smtp.gmail.com', port=587) as connection:
            connection.starttls()
            connection.login(user=my_email, password=password)
            connection.sendmail(from_addr=my_email,
                                to_addrs='fani8731507@gmail.com',
                                msg="Subject:Look Up\n\nISS is over you!!!")

while True:
    time.sleep(60)
    main()

