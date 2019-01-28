from sendgrid.helpers.mail import Mail, Email, Content
from web import app, mail

def send_html_email(to, subject, content):
    sender = app.config['SENDGRID_DEFAULT_FROM']
    message = Mail(Email(sender), subject, Email(to), Content('text/html', content))
    
    response = mail.client.mail.send.post(request_body=message.get())     

    return response