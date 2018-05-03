# Algorithm Code
# Code that will be used to find, analyze, and present news and or relevant articles around our site.

To run article_NERT_parser.py on your own machine, you need to install newspaper(only needed while running  article_NERT_parser), nltk, and as well as Stanford NLP on your own machine.

To instal newspaper:      ```sudo pip instal newspaper```

To instal nltk:           ```sudo pip instal nltk```

go into terminal:         ```python
                          >>> import nltk
                          >>> nltk.download()```
    Set the download directory to:
          Windows  C:\nltk_data
          Mac      /usr/local/share/nltk_data
          Unix     /usr/share/nltk_data
                            

To instal stanford nlp:   http://nlp.stanford.edu/software/stanford-ner-2016-10-31.zip rename the file from stanford-ner-2016-10-31 to stanford-ner then move the file into either your /usr/share or /usr/local/share

Running article_NERT_parser with keywords wrapped in "" and  separated inside with commas by calling: python ```article_NERT_parser [ article_url ] [ pub_time ] [ source ] [ allkeywords ] [ DiffName ] [ "PERSON" ])```
Example:
``` python article_NERT_parser 'https://www.ksl.com/?sid=43675196' "2017-03-29 17:30:38" "2017-03-30 10:43:45" allkeywords DiffName "PERSON" ```



If problem with importing lxml.etree and get the reason, Reason: Incompatible library version: etree.so requires version 12.0.0 or later, but libxml2.2.dylib provides version 10.0.0, fix with the following:

```
brew install libxml2
brew install libxslt
brew link libxml2 --force
brew link libxslt --force
```
