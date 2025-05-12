from openai import OpenAI
from fastapi import FastAPI
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart


client = OpenAI(
    api_key="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",
    base_url = "https://api.groq.com/openai/v1",
)

app = FastAPI()

def gen_mail(name,res):
    prompt = f"""
    You are an LIC policy sales expert. The potential customer named {name} gave this response:
    '{res}'. Based on that, write a personalized follow-up email to re-engage them.
    """
    response = client.chat.completions.create(
        model="llama3-8b-8192",
         messages=[
        {"role": "user", "content":prompt}]
        )
     
    return response.choices[0].message.content



def send_email(name,res,to_email):
    subject ="Test Automation"
    body = gen_mail(name=name,res=res)
    from_email = "prabhakalyan0473@gmail.com"
    password = "xvzt htwa xcsj aekl"  

    message = MIMEMultipart()
    message['From'] = from_email
    message['To'] = to_email
    message['Subject'] = subject

    message.attach(MIMEText(body, 'plain'))

    try:
        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.starttls() 
        server.login(from_email, password)

        server.sendmail(from_email, to_email, message.as_string())
        print(f"Email sent to {to_email} successfully!")
    except Exception as e:
        # print(f"Error: {e}")
        pass
    finally:
        server.quit() 

@app.post("/")
def final(names,mails,ress):
    names = names.split(",")
    mails = mails.split(",")
    ress =  ress.split(",")
    for name,mail,res in zip(names,mails,ress):
        # print(mail,name,res)
        send_email(name=name,res=res,to_email=mail)



