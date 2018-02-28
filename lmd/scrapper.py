import os
import urllib2
import urllib
from cookielib import CookieJar
from lxml import html

EMAIL = ""
PASSWORD = ""
MONTH = "" # Format (String) YYYY-MM

url_get_args = "https://www.monde-diplomatique.fr/load_mon_compte"
url_auth = "https://lecteurs.mondediplo.net/?page=connexion_sso"
url_pdf = "https://www.monde-diplomatique.fr/telechargements/"
url_audio = "https://www.monde-diplomatique.fr/audio?mois="

cj = CookieJar()
opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(cj))


# Get the form args for authentication
print "Generating a valid 'formulaire_action_args'..."
response = opener.open(url_get_args)
content = response.read()
tree = html.fromstring(content)
form_inputs = tree.xpath('//input[@name="formulaire_action_args"]')
form_args = ''

for form_input in form_inputs:
    for attr, value in form_input.items():
        if attr == "value":
            form_args = value

if not form_args:
    print "formulaire_action_args not found!"
    exit()


# Authentication
print "Trying authentication..."
response = opener.open(url_auth)
formdata = { "page" : "connexion_sso",
             "formulaire_action": "identification_sso",
             "formulaire_action_args" : form_args,
             "retour": "https://www.monde-diplomatique.fr/",
             "site_distant": "https://www.monde-diplomatique.fr/",
             "email": EMAIL,
             "mot_de_passe": PASSWORD,
             "valider": "Valider" }
data_encoded = urllib.urlencode(formdata)
response = opener.open(url_auth, data_encoded)

if not "session_mon_compte" in response.read():
    print "Authentication failed!"
    exit()

print "Authentication successful"


# Get the PDF version
print "Generating the downloading link..."
y = MONTH.split("-")[0]
m = MONTH.split("-")[1]
response = opener.open(url_pdf + y + "/" + m)
content = response.read()

link = ""
tree = html.fromstring(content)
pdf_links = tree.xpath('//div[@class="format PDF"]/a')
for pdf_link in pdf_links:
    for attr, value in pdf_link.items():
        if attr == "href":
            filename = "Le-Monde-Diplomatique-" + MONTH + ".pdf"
            link = value

if not link:
    print "No PDF found!"
    exit()

# Create the folder
if not os.path.exists(MONTH):
    print "Creating folder:", MONTH
    os.makedirs(MONTH)

if os.path.exists(MONTH + "/" + filename):
    print "PDF already downloaded:", filename
else:
    print "Downloading:", filename
    response = opener.open("https://www.monde-diplomatique.fr" + link)
    with open(MONTH + "/" + filename, "wb") as f:
        f.write(response.read())


# Get the audio list
print "Collecting audio links..."
response = opener.open(url_audio)
content = response.read()

tree = html.fromstring(content)
audio_links = tree.xpath('//a[@class="telecharger_son"]')

links = []

for audio_link in audio_links:
    for attr, value in audio_link.items():
        if attr == "href":
            filename = os.path.basename(value).split("?")[0]
            links.append((filename, value))

if not links:
    print "No article found!"
    exit()

print len(links), "article(s) found:"
for filename, link in links:
    print " - ", filename


# Download the audio files
for filename, link in links:
    if os.path.exists(MONTH + "/" + filename):
        print "Audio already downloaded:", filename
    else:
        print "Downloading:", filename
        response = opener.open(link)
        with open(MONTH + "/" + filename, "wb") as f:
            f.write(response.read())
