from django.core.mail import send_mail

def send_custom_email(subject, message, recipient_list):
    from_email='notemarketplace4@gmail.com'
    send_mail(subject, message, from_email, recipient_list, fail_silently=False)

def send_welcome_mail(email, password, project):
    clientURL = 'https://real-esate-crm.netlify.app/'
    subject = f'Welcome mail: {project}'
    message = f'email: {email} \n password: {password} \n\n Link: {clientURL}'
    recipient_list = [email]
    send_custom_email(subject, message, recipient_list)

def send_invitation_mail(email, project):
    clientURL = 'https://real-esate-crm.netlify.app/'
    subject = f'Invitation mail: {project}'
    message = f'You are invited to project: {project} \n\n Link: {clientURL}'
    recipient_list = [email]
    send_custom_email(subject, message, recipient_list)