import requests
from datetime import datetime
from time import *
from smtplib import *
MY_LAT = "Your latitude"  # Your latitude
MY_LONG = "Your longitude"  # Your longitude
MY_EMAIL = "Your mail"
MY_EMAIL_PASSWORD = "Your mail password"
iss_longitude = 0
iss_latitude = 0


def iss_is_overhead():
    global iss_latitude, iss_longitude
    response = requests.get(url="http://api.open-notify.org/iss-now.json")
    response.raise_for_status()
    data = response.json()

    iss_latitude = float(data["iss_position"]["latitude"])
    iss_longitude = float(data["iss_position"]["longitude"])

    # Your position is within +5 or -5 degrees of the ISS position.
    if int(MY_LAT) - 5 <= iss_latitude <= MY_LAT + 5 and int(MY_LONG) - 5 <= iss_longitude <= MY_LONG + 5:
        return True
    return False


iss_is_overhead()


def is_night():
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
    time_now = datetime.now().utcnow().hour
    if time_now < sunrise or time_now > sunset:
        return True
    return False


def print_info():
    print()
    print(datetime.now())
    print(f"\tMy latitude: {MY_LAT}\n\tMy longitude: {MY_LONG}"
          f"\n\tISS latitude: {iss_latitude}\n\tISS longitude: {iss_longitude}")


try:
    while True:
        if iss_is_overhead():
            if is_night():
                message = (f"Look Up \nThe ISS is close to my current position"
                           f"\nIt is in : \n\t{iss_latitude} latitude,\n\t{iss_longitude} longitude\nHurry Up!!"
                           f"\nThis is a link if u want to trace it : http://open-notify.org/Open-Notify-API/ ")
                with SMTP("smtp.gmail.com") as connection:
                    connection.starttls()
                    connection.login(user=MY_EMAIL, password=MY_EMAIL_PASSWORD)
                    connection.sendmail(from_addr=MY_EMAIL,
                                        to_addrs="bedischebaane107@gmail.com",
                                        msg=f"Subject: The ISS is close to my current position\n\n{message}")
                print_info()
                print("Email Sent!")
            else:
                print_info()
                print("let's wait for the sunset")
        else:
            print_info()
            print("let's wait for it. Still so far")
        # If the ISS is close to my current position,
        # and it is currently dark
        # Then email me to tell me to look up.
        # BONUS: run the code every 60 seconds.

        sleep(60)
except KeyboardInterrupt:
    print("Thanks for using our Program")
