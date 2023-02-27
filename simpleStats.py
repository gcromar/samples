# -*- coding: utf-8 -*-
"""
Created on Tue Apr 23 22:29:59 2019

Note: Parses an XML file containing StackExchange Posts and does some
      simple NLP processing.

@author: Graham
"""

from xml.etree import ElementTree
from nltk.corpus import stopwords
from textblob import TextBlob
from textblob import Word
from nltk.stem import PorterStemmer
import os
import re
import string


# functions
def is_number(s):
    try:
        float(s)
        return True
    except ValueError:
        return False


# Check file path
path = os.path.normpath('c:\\users\\graham\\StackExchange\\AskUbuntu'
                        '\\Posts.xml')
exists = os.path.isfile(path)

# Define translations for data cleaning
translation = str.maketrans("", "", string.punctuation)

# Define stop words
stop = stopwords.words('english')

# Instantiate word stemmer
st = PorterStemmer()


if exists:
    # Parse xml file element by element

    xml_iter = ElementTree.iterparse(path, events=('start', 'end'))
    for event, elem in xml_iter:

        if event == 'start':
            if elem.tag == "row":
                attrib = elem.attrib

            # field mapping

                Id = attrib["Id"]
                PostTypeId = attrib['PostTypeId']  # 1:Question 2:Answer

                if 'Body' in attrib:
                    Body = attrib['Body']
                else:
                    Body = None

                if 'Title' in attrib:
                    Title = attrib['Title']
                else:
                    Title = None

                if 'Tags' in attrib:
                    Tags = attrib['Tags']
                else:
                    Tags = None

            # basic feature extraction

                body_wordCount = 0
                title_wordCount = 0
                tags_wordCount = 0

                # word count
                if Body is not None:
                    body_wordCount = len(Body.split(" "))
                if Title is not None:
                    title_wordCount = len(Title.split(" "))
                if Tags is not None:
                    tags_wordCount = len(Tags.split(" "))

#                print(title_clean.split(" "))
#                print(body_clean.split(" "))
#                print(tags_clean.split(" "))
#
#                print(title_clean, title_wordCount)
#                print(body_clean, body_wordCount)
#                print(tags_clean, tags_wordCount)

                body_charCount = 0
                title_charCount = 0
                tags_charCount = 0

                # character count (including spaces)

                if Body is not None:
                    body_charCount = len(Body)
                if Title is not None:
                    title_charCount = len(Title)
                if Tags is not None:
                    tags_charCount = len(Tags)

                body_wordLen = 0
                title_wordLen = 0
                tags_wordLen = 0

                # average word length
                if Body is not None:
                    words = Body.split(" ")
                    body_wordlen = (sum(len(word) for word in words))/(len(
                            words))
                if Title is not None:
                    words = Title.split(" ")
                    title_wordLen = (sum(len(word) for word in words))/(len(
                            words))
                if Tags is not None:
                    words = Tags.split(" ")
                    tags_wordLen = (sum(len(word) for word in words))/(len(
                            words))

                body_stops = 0
                title_stops = 0
                tags_stops = 0

                # count stop words
                if Body is not None:
                    words = Body.split(" ")
                    body_stops = len([word for word in words if word in stop])
#                    body_stopWords = [word for word in words if word in stop]
                if Title is not None:
                    words = Title.split(" ")
                    title_stops = len([word for word in words if word in stop])
                if Tags is not None:
                    words = Tags.split(" ")
                    tags_stops = len([word for word in words if word in stop])

                body_tweets = 0
                title_tweets = 0
                tags_tweets = 0

                # count hashtags
                if Body is not None:
                    words = Body.split(" ")
                    body_tweets = len([word for word in words if
                                      word.startswith('#')])
                if Title is not None:
                    words = Title.split(" ")
                    title_tweets = len([word for word in words if
                                       word.startswith('#')])
                if Tags is not None:
                    words = Tags.split(" ")
                    tags_tweets = len([word for word in words if
                                      word.startswith('#')])

                body_nums = 0
                title_nums = 0
                tags_nums = 0

                # count numerics (use str.isdigit for integers only)
                if Body is not None:
                    words = Body.split(" ")
                    body_nums = len([word for word in words if
                                    is_number(word)])
                if Title is not None:
                    words = Title.split(" ")
                    title_nums = len([word for word in words if
                                     is_number(word)])
                if Tags is not None:
                    words = Tags.split(" ")
                    tags_nums = len([word for word in words if
                                    is_number(word)])

                body_upper = 0
                title_upper = 0
                tags_upper = 0

                # count UPPER case words
                if Body is not None:
                    words = Body.split(" ")
                    body_upper = len([word for word in words if
                                      word.isupper()])
                if Title is not None:
                    words = Title.split(" ")
                    title_upper = len([word for word in words if
                                       word.isupper()])
                if Tags is not None:
                    words = Tags.split(" ")
                    tags_upper = len([word for word in words if
                                      word.isupper()])

            # data cleaning
                body_clean = ""
                if Body is not None:

                    # remove embedded html tags
                    body_clean = re.sub(r'<\w+>|<\/\w+>|<a href=\S*">', r'',
                                        Body.rstrip())

                    # remove excess non-word characters
                    body_clean = re.sub(r'\W+', r' ', body_clean.rstrip())

                    # tranlate to lower case and remove punctuation
                    body_clean = body_clean.lower().translate(
                            translation).rstrip().lstrip()
                    # remove stop words
                    words = body_clean.split()
                    body_clean = " ".join(
                            word for word in words if word not in stop)

                title_clean = ""
                if Title is not None:

                    # remove embedded html tags
                    title_clean = re.sub(r'<\w+>|<\/\w+>|<a href=\S*">', r'',
                                         Title.rstrip())

                    # remove excess non-word characters
                    title_clean = re.sub(r'\W+', r' ', title_clean.rstrip())

                    # tranlate to lower case and remove punctuation
                    title_clean = title_clean.lower().translate(
                            translation).rstrip().lstrip()
                    # remove stop words
                    words = title_clean.split()
                    title_clean = " ".join(
                            word for word in words if word not in stop)

                tags_clean = ""
                if Tags is not None:

                    # remove embedded html tags
                    tags_clean = re.sub(r'<\w+>|<\/\w+>|<a href=\S*">', r'',
                                        Tags.rstrip())

                    # remove excess non-word characters
                    tags_clean = re.sub(r'\W+', r' ', tags_clean.rstrip())

                    # tranlate to lower case and remove punctuation
                    tags_clean = tags_clean.lower().translate(
                            translation).rstrip().lstrip()
                    # remove stop words
                    words = tags_clean.split()
                    tags_clean = " ".join(
                            word for word in words if word not in stop)

# =============================================================================
# Note on common and rare word removal
#   At this stage one would normally remove e.g. the top 10 most common
#   words and most rare words in the data set.  The reasoning is that
#   extremely common words will have a high random association whereas
#   with rare words, the association between them and other words
#   is dominated by noise.
#
#   Here, calculation of word frequencies for the whole data set are
#   needed.  This is easy to incorporate using a dataframe approach but
#   as this example uses line by line parsing of extremely large XML files
#   such as step would require a separate process.  Since I'm uncertain
#   how much data I will use for my sample application I am opting to
#   skip this step for the time being.
# =============================================================================

            # Spelling correction (not used beyond this example)
                body_corrected = str(TextBlob(body_clean).correct())
                title_corrected = str(TextBlob(title_clean).correct())
                tags_corrected = str(TextBlob(tags_clean).correct())

            # Tokenization
                body_words = str(TextBlob(body_clean).words)
                title_words = str(TextBlob(title_clean).words)
                tags_words = str(TextBlob(tags_clean).words)

            # Stemming (removal of word suffices)
                # Works but is pretty terrible!
                body_stemmed = ""
                words = body_clean.split(" ")
                for word in words:
                    stemmed = st.stem(word)
#                    print(word, stemmed)
                    body_stemmed += " " + stemmed
                body_stemmed = body_stemmed.lstrip()

            # Lemmatization (finds root words - prefered to stemming)
                body_lemmed = ""
                words = body_clean.split(" ")
                for word in words:
                    lemmed = Word(word).lemmatize()
                    print(word, lemmed)
                    body_lemmed += " " + lemmed
                body_lemmed = body_lemmed.lstrip()

else:
    print('file not found')
