import smtplib

try:
    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.starttls()
    server.login('takkharidwebsite@gmail.com', 'T@KkharidIsTheBest')
    message = "Test email from Django"
    server.sendmail('takkharidwebsite@gmail.com', 'takkharidwebsite@gmail.com', message)
    server.quit()
    print("Email sent successfully")
except Exception as e:
    print(f"Failed to send email: {e}")
