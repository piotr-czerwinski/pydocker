from sendgrid.helpers.mail import Mail, Email, Content
from flask import current_app

def send_html_email(to, subject, content):
    sender = current_app.config['SENDGRID_DEFAULT_FROM']
    message = Mail(Email(sender), subject, Email(to), Content('text/html', content))
    
    response = current_app.mail.client.mail.send.post(request_body=message.get())     

    return response