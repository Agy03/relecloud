import requests

def send_email_via_azure(recipient_email, recipient_name, subject, body):
    url = "https://<your-resource-name>.communication.azure.com/emails:send?api-version=2021-10-01-preview"

    headers = {
        "Content-Type": "application/json",
        "Authorization": "Bearer <your_access_token>" 
    }

    data = {
        "senderAddress": "DoNotReply@367dfc30-e245-4dbe-98aa-0acde800b2a4.azurecomm.net",  
        "content": {
            "subject": subject,
            "plainText": body
        },
        "recipients": {
            "to": [
                {
                    "address": recipient_email,
                    "displayName": recipient_name
                }
            ]
        }
    }

    response = requests.post(url, json=data, headers=headers)

    if response.status_code == 202:
        print("Correo enviado con éxito.")
    else:
        print(f"Error al enviar el correo: {response.status_code}")
        print(response.json())
