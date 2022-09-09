import pyfiglet
import time


pyfiglet.print_figlet("Download Speed Calculator")

connection_speed = float(input(" Enter results from online speed test: "))

calc_num = 8

download_speed = float(connection_speed) / float(calc_num)

if connection_speed < 0:
    print("You entered a negative integer which cannot be converted. ")
    exit()
elif connection_speed < 10:
    print("You entered", connection_speed, ", please enter any integer above 10. As anything below it will result in less than 1 MB/s sum. ")
    exit()
print("Your download speed is", download_speed, "MB/s\nThis converter will close automatically in 30 seconds....")

time.sleep(30)

exit()
