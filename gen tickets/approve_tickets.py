import os
import sqlite3
import requests
import hashlib
import pyqrcode
from sendmail import SendMessage

connection = sqlite3.connect('db.sqlite3')
cur = connection.cursor()


API_KEY = "Your API Key"
FOLDER_URL = "https://www.googleapis.com/drive/v2/files?q='[FOLDER_ID]'+in+parents&key="
FILE_URL = "https://www.googleapis.com/drive/v3/files/[FILE_ID]?alt=media&key="

vol = "https://docs.google.com/spreadsheets/d/1chCtVLKz_D2qpE3uVaOiJujdeLqvO0H0tsjFuMJIp-I/export?format=csv"
gen = "https://docs.google.com/spreadsheets/d/1a0kEcjbyJfz8ZSm0g5ts50cvJ1mF6AJdo6PLVbqR2UI/export?format=csv"
gen_img_1 = "https://drive.google.com/drive/folders/1DtDTwMk06b_E2t_y5vRLGFYvWugD3JtaVgk3Cxz4TGruBAMCYvBu3RmphaEK7qTnNSnNbdvO?usp=sharing"
gen_img_2 = "https://drive.google.com/drive/folders/1qdt0Jxar_DRV3fVd7ojd67Amvj-C5N58GqImLXLBw7DLTIN7XdxMUE-3GIhOgXK32CKoYyR6?usp=sharing"

codes = {
    'Srushti': '4666',
    'Zaid': '4984',
    'Parth': '8147',
    'Bhavnish': '8024',
    'Pranav': '4484',
    'Shreyas': '4665',
    'Isha': '4697',
    'Vishal': '5552',
    'Ashkrit': '3681',
    'Aarnav': '1034',
    'Omkar': '4979',
    'Sanyukta': '9648',
    'Makarand': '2409',
    'Rishi': '0862',
    'Vratesh': '9648'
}


MAIL_CONTENT = """
Hello [NAME], welcome to the TEDx Community! Your booking is confirmed for TEDxDYPIT.<br>
<br>
Below attached is your QR Ticket<br>
<br>
Please produce this QR code at the registration desk for verification.<br>
<br>
Venue: DPU Auditorium, Dr. D.Y. Patil Medical College, Sant Tukaram Nagar, Pimpri Colony, Pimpri-Chinchwad, Maharashtra. <br>
<br>
Google Maps Link:<br>
<br>
https://maps.app.goo.gl/nZ7nGhM9dCucy4qU6<br>
<br>
Date: 15th October 2022<br>
<br>
Registrations will begin at 11:00 am and will be closed by 11:30 am.<br>
<br>
Rules & Regulations:<br>
<br>
• Without the QR code, entry shall not be granted at the venue.<br>
<br>
• Please carry an ID along with you.<br>
<br>
• Videography is strictly prohibited during the event.<br>
<br>
• Your compliance with the TEDx set of rules is expected.<br>
<br>
• The TEDxDYPIT team reserves the right to terminate the registration of any of the attendees at any time during or prior the event.<br>
<br>
• Eatables and beverages are strictly not permitted inside the auditorium (A separate interval will be provided for the same).<br>
<br>
• Please report to the venue at the given time. See you there!<br>
<br>
- On-spot registration also available, starting from 10.30am at venue<br>
<br>
Regards,<br>
<br>
Team TEDxDYPIT
"""


def DownLoadFile(url,  file_name):
    if os.path.exists(file_name):
        os.remove(file_name)

    r = requests.get(url, allow_redirects=True, stream=True)
    if r.status_code != 200:
        return
    with open(f"./downloads/{file_name}", 'wb') as fd:
        for chunk in r.iter_content(chunk_size=1024*10):
            if chunk:
                fd.write(chunk)
    return f"./downloads/{file_name}"


def update_database(spreadsheet, form_name):
    f = DownLoadFile(spreadsheet, file_name=f'{form_name}.csv')
    f = f"./downloads/{form_name}.csv"
    with open(f, 'r') as f:
        data = f.read()
    data = data.split('\n')[1:]
    for i in data:
        i = i.replace(", Pimpri", " Pimpri")
        i = [j.strip() for j in i.split(",")]
        try:
            if form_name == "vol":
                # if codes.get(i[5]) == i[6]:  # confirm if codes match
                if True:
                    query = f"INSERT INTO TedXDypit(Name, Number, Email, Type, Payment_Methord) values('{i[2]}', '{i[3]}', '{i[1]}', '{form_name}', '{i[4]}')"
                    cur.execute(query)
                else:
                    print(f'{i[2]}, {i[3]}, {i[1]}', "codes dont match", i[5], ":", i[6])
            elif form_name == "gen":
                query = f"INSERT INTO TedXDypit(Name, Number, Email, Type, Payment_Methord, Screenshot) values('{i[2]}', '{i[3]}', '{i[1]}', '{form_name}', 'UPI', '{i[5].split('=')[-1]}')"
                cur.execute(query)
        except Exception as e:
            # print(str(e), f'{i[2]}, {i[3]}, {i[1]}')
            pass
    connection.commit()


def download_folder_screenshots(furl):
    folder_id = furl.split("/")[-1].split("?")[0]
    url = FOLDER_URL
    url = url.replace("[FOLDER_ID]", folder_id)
    r = requests.get(f"{url}{API_KEY}")
    main = r.json()
    j = r.json()
    while j.get("nextLink"):
        r = requests.get(f"{j['nextLink']}&key={API_KEY}")
        j = r.json()
        main['items'] += j['items']
    
    items = main["items"]
    print(len(items))
    for i in items:
        id = i['id']
        name = i['title']
        name = name.replace("&", "_").replace("%", '_')
        if not os.path.exists(id+".png"):
            try:
                os.rename("downloads/"+name, "downloads/"+id+".png")
            except:
                print(id, name)


def approve_ss_tickets():
    # RUN THIS ONLY AFTER GETTING FAILURE.TXT FROM RUNNING OCR
    with open('failure.txt', 'r') as f:
        data = f.read()
    data = data.split("\n")
    for i in data:
        query = f"UPDATE TedXDypit SET Approved='N' WHERE Screenshot='{i}'"
        cur.execute(query)
    query = "UPDATE TedXDypit SET Approved='Y' WHERE Approved IS NULL"
    connection.commit()


def generate_qr():
    query = "SELECT * FROM TedXDypit where Approved='Y'"
    cur.execute(query)
    data = cur.fetchall()
    res = []
    for i in data:
        id = i[0]
        hash = hashlib.md5(bytes(id))
        qr = pyqrcode.create(f"TedXDypit-ID-{id}-{hash.hexdigest()[:4]}")
        qr.png(f'qrs/{id}.png', scale = 8)
        temp = list(i)
        temp[-2] = f"TedXDypit-ID-{id}-{hash.hexdigest()[:4]}"
        temp[-1] = f'qrs/{id}.png'
        if temp[2] == None:
            temp[2] = 0
        res.append(tuple(temp))

    return res


def send_tickets():
    query = "SELECT * FROM TedXDypit WHERE Approved ='Y'"
    cur.execute(query)
    data = cur.fetchall()
    query = "SELECT * FROM emails"
    cur.execute(query)
    mails = cur.fetchall()
    mails = [i[1] for i in mails]
    # print(mails)
    for i in data:
        id = i[0]
        name = i[1]
        email = i[3]
        if email not in mails:
            try:
                send_mail(name, email, id, content= MAIL_CONTENT)
                query = f"INSERT INTO emails(Email) values('{email}')"
                cur.execute(query)
            except Exception as e:
                print(e)
                print("error with send mail: ", id, name, email)

    connection.commit()

        
def send_mail(name, email, id, content):
    SendMessage(
        sender = "tedxdypitcommunications@gmail.com",
        to = email,
        msgHtml = content.replace("[NAME]", name),
        msgPlain = "TedXDypit Ticket",
        subject = "TedXDypit Ticket",
        attachmentFile = f"qrs/{id}.png"
    )
    print("Sent: ", name, ", ", email)


if __name__ == "__main__":
    pass
    # update_database(vol, "vol")
    # update_database(gen, "gen")
    # download_folder_screenshots(gen_img_1)
    # download_folder_screenshots(gen_img_2)
    # approve_ss_tickets()
    # generate_qr()
    # send_tickets()