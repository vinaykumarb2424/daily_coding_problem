import re
import email
import imaplib
from MONGO import *


class ReadGmails(object):
    IMAP_SERVER = "imap.gmail.com"
    IMAP_PORT = 993

    def __init__(self, username, password):
        self.mail = None
        self.username = username
        self.password = password

    def login(self):
        try:
            mail = imaplib.IMAP4_SSL(ReadGmails.IMAP_SERVER)
            status, response = mail.login(self.username, self.password)
            if status == "OK":
                return mail
            #print("status   : {}".format(status))
            #print("Response : {}".format(response[0].decode()))
        except Exception as ex:
            return False

    def clean_body(self, body):
        try:
            filtered_text = re.sub(r'[^\w\s]', '', body)
            start_index = filtered_text.find('today.')+1
            end_index = filtered_text.find('Upgrade')
            filtered_text = filtered_text[start_index:end_index].strip().replace("\r", '').split('\n')
            return filtered_text
        except:
            return False

    def create_json_object(self,subject, filtered_text):
        problem_no = subject[subject.find('#') + 1:subject.find('[')].strip()
        level = subject[subject.find('[') + 1:subject.find(']')]
        # print(subject)
        # print(filtered_text)
        company = filtered_text[2].split()[-1]
        # print(company)
        problem_stmt = " ".join(filtered_text[1: len(filtered_text)+1])
        # print(problem_stmt)
        json_object = dict()
        json_object["_id"] = int(problem_no)
        json_object["problem_no"] = int(problem_no)
        json_object["level"] = level
        json_object["company"] = company
        json_object["problem_stmt"] = problem_stmt
        return json_object

    def add_data(self, data):
        try:
            client = MONGO().get_mongo_client()
            # Access your database and collection
            db = client["daily_coding_problem"]
            collection = db["problems"]
            query = {"problem_no":data["problem_no"]}
            collection.update_one(query, {"$set": data}, upsert=True)
            #result = collection.insert_one(data)
            print(f"result added{data['problem_no']}")
            client.close()
        except Exception as ex:
            print(ex)


    def get_mail(self):
        try:
            self.mail = self.login()
            if self.mail:
                self.mail.select(mailbox="Inbox")
                try:
                    count =1
                    while count<803:
                        status, mails = self.mail.search(
                            None, f'FROM "Daily Coding Problem" Subject "Daily Coding Problem: Problem #{count}"')
                        mail_list = mails[0].decode("utf-8").split()
                        print(mail_list,len(mail_list))
                        for mail_id in mail_list:
                            status, mail_data = self.mail.fetch(mail_id, '(RFC822)')  # Fetch mail data
                            if status == "OK":
                                message = email.message_from_bytes(mail_data[0][1])  # Construct Message from mail data
                                # print("From       : {0}".format(message.get("From")))
                                # print("To         : {0}".format(message.get("To")))
                                # print("Date       : {0}".format(message.get("Date")))
                                subject =(message.get("Subject"))
                                # print("Body       :")
                                for part in message.walk():  # iterate over all the parts and subpart
                                    # print(part)
                                    if part.get_content_type() == "text/plain":
                                        body = part.get_payload()
                                        filtered_text =self.clean_body(body)
                                        if filtered_text:
                                            data = self.create_json_object(subject.strip(), filtered_text)
                                            self.add_data(data)
                                    elif part.get_content_type() == "text/html":
                                        body = part.get_payload()
                                        # print(body)
                        count +=1
                except Exception as ex:
                        print(ex)
            else:
                print('login failed')
        except Exception as ex:
            raise Exception(f"failed to get email message:{ex}")

    def logout(self):
        try:
            self.mail.logout()
            print('mail logged out')
        except:
            raise Exception("Failed to logged out")


cv = ReadGmails("vinaykumarb2424@gmail.com", "fkhxoadssqgwixau")
cv.get_mail()
cv.logout()

# fkhxoadssqgwixau google app password
#Lunareclipse@sun regula rpassword