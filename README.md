# OneSecMailAsyncWapper
OneSecMailAsyncWapper - Async wapper over https://www.1secmail.com API temporary mail service
See also: https://github.com/MrNom4ik/OneSecMailWapper (sync version on the `requests` library)
# Install
```bash
python setup.py install
```
# Examples
```py
from OneSecMailWapper import get_domians, get_mailbox, Mailbox, Mail, Attachment
```
## Mailbox
### Get domians
```python
domians: List[str] = await get_domians()
```
### Get specific mailbox
```python
mailbox: Mailbox = await get_mailbox("0ad1ekwui8", "qiott.com")
```
or
```python
mailbox: Mailbox = await get_mailbox("0ad1ekwui8@qiott.com")
```
### Get random mailbox
```python
mailbox: Mailbox = await get_mailbox()
```

## Mails
Initially, the API returns short mails, in order to receive the mails in full, you need to make an additional request to the API.

[Mail](https://github.com/MrNom4ik/OneSecMailWapper/blob/main/OneSecMailAsyncWapper/mailbox.py#L86) fields:
```python
id: int
from_adress: str
subject: str
date: datetime
attachments: List[Attachment]
body: str
textBody: str
htmlBody: str
```
### Get mails
You can get all mails with [Mailbox.get_mails()](https://github.com/MrNom4ik/OneSecMailWapper/blob/main/OneSecMailAsyncWapper/mailbox.py#L43):
```python
mails: List[Mail] = await mailbox.get_mails()
```
### Wait mail
If you need to receive an mail that is due soon, you can use [Mailbox.wait_mail()](https://github.com/MrNom4ik/OneSecMailWapper/blob/main/OneSecMailAsyncWapper/mailbox.py#L57):
```python
async def check(mail: Mail) -> bool:
    return mail.from_adress == "example@example.com"

mail: Mail = await mailbox.wait_mail(check)
print(mail.body)
```
This method will create a while loop and will check for new mails every 5 seconds(default). Each new mail will be checked through `check` and if the check is successful, the letter will be returned.

## Attachments
[Attachment](https://github.com/MrNom4ik/OneSecMailWapper/blob/main/OneSecMailAsyncWapper/mailbox.py#L16) fields:
```python
filename: str
content_type: str
size: int
```

You can get the content of an attachment with [Attachment.get_content()](https://github.com/MrNom4ik/OneSecMailWapper/blob/main/OneSecMailAsyncWapper/mailbox.py#L23):
```python
for attachment in mail.attachments:
    print(attachment.get_content(), file=open(attachment.filename, 'wb'))
```
