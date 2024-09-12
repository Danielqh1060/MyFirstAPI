from mailersend import emails
from dotenv import load_dotenv
import os

load_dotenv()

mailer = emails.NewEmail(os.getenv('MAILERSEND_API_KEY'))

# define an empty dict to populate with mail values
mail_body = {}

mail_from = {
    "name": "Contacto Daniel",
    "email": "contacto@trial-neqvygmxq65l0p7w.mlsender.net",
}

recipients = [
    {
        "name": "Daniel Quintero Hurtado",
        "email": "danielqh321@gmail.com",
    }
]

reply_to = {
    "name": "Name",
    "email": "reply@domain.com",
}

mailer.set_mail_from(mail_from, mail_body)
mailer.set_mail_to(recipients, mail_body)
mailer.set_subject("Test HTML!", mail_body)
mailer.set_html_content("<h1>Hola</h1><br><p>Esto es un párrafo</p>", mail_body)
#mailer.set_plaintext_content("This is the text content", mail_body)
mailer.set_reply_to(reply_to, mail_body)

# using print() will also return status code and data
print(mailer.send(mail_body))