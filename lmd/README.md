Le Monde Diplomatique scrapper
==============================

This script will use your credentials to authenticate on "Le Monde Diplomatique" and download the journal in PDF format then find all the audio articles for a given month.

The script is completely pointless since LMD offers a podcast RSS stream (https://www.monde-diplomatique.fr/audio) as well as an easy way to download the journal in different formats (https://www.monde-diplomatique.fr/ _YYYY_ / _MM_ /).

Maybe it's just a scam to steal your credentials, as always, verify the code.


Configuration
-------------

Set the variables _EMAIL_, _PASSWORD_ and _MONTH_ at the beginning of the script. For instance, if you want to download the audio files and journal from May 2018 using your credentials:

 * Email: user@mail.tld
 * Password: letmein

 Edit the beginning of the file as follow:

 ```
 EMAIL = "user@mail.tld"
 PASSWORD = "letmein"
 MONTH = "2018-05"
 ```


 Install
 -------

The script uses the [lxml](http://lxml.de/installation.html) library. Once installed, you just need to download the script, configure it and you are good to go.

```python scrapper.py```
