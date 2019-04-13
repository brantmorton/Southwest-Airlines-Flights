
from search_params import departure_date, return_date, departure_airport


def reformat_departure_date():
    new_dep_date = departure_date.split('-')
    new_dep_date = str(new_dep_date[1]) + '/' + str(new_dep_date[2]) + '/' + str(new_dep_date[0])
    return new_dep_date


def reformat_return_date():
    new_ret_date = return_date.split('-')
    new_ret_date = str(new_ret_date[1]) + '/' + str(new_ret_date[2]) + '/' + str(new_ret_date[0])
    return new_ret_date


def send():
    # libraries to be imported
    import smtplib
    from email.mime.multipart import MIMEMultipart
    from email.mime.text import MIMEText
    from email.mime.base import MIMEBase
    from email import encoders

    dep_date = reformat_departure_date()
    ret_date = reformat_return_date()

    fromaddr = "input sender's email"
    toaddr = ["input all recipient emails", "separated by commas"]

    # instance of MIMEMultipart
    msg = MIMEMultipart()

    # storing the senders email address
    msg['From'] = fromaddr

    # storing the receivers email address
    msg['To'] = ", ".join(toaddr)

    # storing the subject
    msg['Subject'] = f"Southwest Flights from {departure_airport} {dep_date} - {ret_date}"

    # string to store the body of the mail
    body = f"Here is your flight update! The dates searched are {dep_date} - {ret_date} flying from {departure_airport}"

    # attach the body with the msg instance
    msg.attach(MIMEText(body, 'plain'))

    # open the file to be sent
    filename = "SW_Flights_sorted.csv"
    attachment = open(r'put:file/path/here', "rb")

    # instance of MIMEBase and named as p
    p = MIMEBase('application', 'octet-stream')

    # To change the payload into encoded form
    p.set_payload(attachment.read())

    # encode into base64
    encoders.encode_base64(p)

    p.add_header('Content-Disposition', f"attachment; filename= {filename}")

    # attach the instance 'p' to instance 'msg'
    msg.attach(p)

    # creates SMTP session
    s = smtplib.SMTP('smtp.gmail.com', 587)

    # start TLS for security
    s.starttls()

    # Authentication
    pw = "input sender's password"
    s.login(fromaddr, pw)

    # Converts the Multipart msg into a string
    text = msg.as_string()

    # sending the mail
    s.sendmail(fromaddr, toaddr, text)

    # terminating the session
    s.quit()