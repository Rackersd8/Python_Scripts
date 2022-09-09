import pyfiglet
import time

pyfiglet.print_figlet("Download Speed Calculator")

calc_num = 8

while True:
    try:
        connection_speed = float(
            input("Enter results from online speed test: "))  # Try to convert the input into a number
        break  # Break out of the infinite loop if the conversion is successful
    except ValueError:  # Do this instead if the try block causes a ValueError
        print("Sorry, that is not an integer. Please try again.")
download_speed = float(connection_speed) / float(calc_num)
if connection_speed < 0:
    print("You entered a negative integer which cannot be converted. ")
    exit()
elif connection_speed < 10:
    print("You entered", connection_speed,
          ", please enter any integer above 10. As anything below it will result in less than 1 MB/s sum. ")
    exit()
print("\nYour download speed is", download_speed, "MB/s\n\nThis converter will close automatically in 30 seconds....")

time.sleep(30)

exit()