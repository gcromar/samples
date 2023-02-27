# -*- coding: utf-8 -*-
"""
Created on Mon Mar 25 21:47:06 2019

@author: Graham
"""

from xml.etree import ElementTree
from nltk.corpus import stopwords
from textblob import Word
import os
import psycopg2
import re
import string

# Define translations for data cleaning
translation = str.maketrans("", "", string.punctuation)

# Define stop words
# stop = stopwords.words('english')

# Customize stop word list
stop = set(stopwords.words('english'))
new_stopwords = ['ubuntu', 'like', 'x', 'http', 'com', 'would', 'work',
                 'use', 'using', 'window', 'get', 'file', 'way', 'want',
                 'one', 'problem', 'line']
stop = stop.union(new_stopwords)

# =============================================================================
# Main line
# =============================================================================

# Check file path
path = os.path.normpath('c:\\users\\graham\\StackExchange\\AskUbuntu'
                        '\\Posts.xml')
exists = os.path.isfile(path)

if exists:
    # Parse xml file element by element

    try:
        connection = psycopg2.connect(user="postgres",
                                      password="insight",
                                      host="127.0.0.1",
                                      port="5432",
                                      database="stack")
        cursor = connection.cursor()

        i = 0
        xml_iter = ElementTree.iterparse(path, events=('start', 'end'))
        for event, elem in xml_iter:

            if event == 'start':
                i += 1
                if elem.tag == "row":
                    attrib = elem.attrib

                    # field mapping

                    Id = attrib["Id"]
                    PostTypeId = attrib['PostTypeId']  # 1:Question 2:Answer

                    # Either ParentID or AcceptedAnswer
                    # will be present depending on PostTypeId
                    # Other fields have also been found to be occassionally
                    # Blank and hence missing from the attribute list

                    if 'ParentID' in attrib:
                        ParentId = attrib['ParentID']
                    else:
                        ParentId = None

                    if 'AcceptedAnswerId' in attrib:
                        AcceptedAnswerId = attrib['AcceptedAnswerId']
                    else:
                        AcceptedAnswerID = None

                    if 'CreationDate' in attrib:
                        CreationDate = attrib['CreationDate']
                    else:
                        CreationDate = None

                    if 'Score' in attrib:
                        Score = attrib['Score']
                    else:
                        Score = None

                    if 'ViewCount' in attrib:
                        ViewCount = attrib['ViewCount']
                    else:
                        ViewCount = None

                    if 'Body' in attrib:
                        Body = attrib['Body']
                    else:
                        Body = None

                    if 'OwnerUserId' in attrib:
                        OwnerUserId = attrib['OwnerUserId']
                    else:
                        OwnerUserId = None

                    if 'LastEditorUserId' in attrib:
                        LastEditorUserId = attrib['LastEditorUserId']
                    else:
                        LastEditorUserId = None

                    if 'LastEditorDiplayName' in attrib:
                        LastEditorDisplayName = attrib['LastEditorDisplayName']
                    else:
                        LastEditorDisplayName = None

                    if 'LastEditDate' in attrib:
                        LastEditDate = attrib['LastEditDate']
                    else:
                        LastEditDate = None

                    if 'LastActivityDate' in attrib:
                        LastActivityDate = attrib['LastActivityDate']
                    else:
                        LastActivityDate = None

                    if 'CommunityOwnedDate' in attrib:
                        CommunityOwnedDate = attrib['CommunityOwnedDate']
                    else:
                        CommunityOwnedDate = None

                    if 'ClosedDate' in attrib:
                        ClosedDate = attrib['ClosedDate']
                    else:
                        ClosedDate = None

                    if 'Title' in attrib:
                        Title = attrib['Title']
                    else:
                        Title = None

                    if 'Tags' in attrib:
                        Tags = attrib['Tags']
                    else:
                        Tags = None

                    if 'AnswerCount' in attrib:
                        AnswerCount = attrib['AnswerCount']
                    else:
                        AnswerCount = None

                    if 'CommentCount' in attrib:
                        CommentCount = attrib['CommentCount']
                    else:
                        CommentCount = None

                    if 'FavoriteCount' in attrib:
                        FavoriteCount = attrib['FavoriteCount']
                    else:
                        FavoriteCount = None

                    # clean the data
                    body_clean = ""
                    if Body is not None:

                        # remove embedded html tags
                        body_clean = re.sub(r'<\w+>|<\/\w+>|<a href=\S*">',
                                            r'', Body.rstrip())

                        # remove excess non-word characters
                        body_clean = re.sub(r'\W+', r' ', body_clean.rstrip())

                        # remove digits
                        body_clean = re.sub(r'\d+', r' ', body_clean.rstrip())

                        # tranlate to lower case and remove punctuation
                        body_clean = body_clean.lower().translate(
                                translation).rstrip().lstrip()

                        # remove stop words
                        words = body_clean.split()
                        body_clean = " ".join(
                                word for word in words if word not in stop)

                        # lemmatization (finds root words)
                        body_lemmed = ""
                        words = body_clean.split(" ")
                        for word in words:
                            lemmed = Word(word).lemmatize()
                            body_lemmed += " " + lemmed
                            body_lemmed = body_lemmed.lstrip()

                        Body = body_lemmed

                    title_clean = ""
                    if Title is not None:

                        # remove embedded html tags
                        title_clean = re.sub(r'<\w+>|<\/\w+>|<a href=\S*">',
                                             r'', Title.rstrip())

                        # remove excess non-word characters
                        title_clean = re.sub(r'\W+', r' ',
                                             title_clean.rstrip())

                        # remove digits
                        title_clean = re.sub(r'\d+', r' ',
                                             title_clean.rstrip())

                        # tranlate to lower case and remove punctuation
                        title_clean = title_clean.lower().translate(
                                translation).rstrip().lstrip()

                        # remove stop words
                        words = title_clean.split()
                        title_clean = " ".join(
                                word for word in words if word not in stop)

                        Title = title_clean

                    tags_clean = ""
                    if Tags is not None:

                        # remove embedded html tags
                        tags_clean = re.sub(r'<\w+>|<\/\w+>|<a href=\S*">',
                                            r'', Tags.rstrip())

                        # remove excess non-word characters
                        tags_clean = re.sub(r'\W+', r' ', tags_clean.rstrip())

                        # remove digits
                        tags_clean = re.sub(r'\d+', r' ', tags_clean.rstrip())

                        # tranlate to lower case and remove punctuation
                        tags_clean = tags_clean.lower().translate(
                                translation).rstrip().lstrip()
                        # remove stop words
                        words = tags_clean.split()
                        tags_clean = " ".join(
                                word for word in words if word not in stop)

                        Tags = tags_clean

                    # prepare insert query

                    postgres_insert_query = """ INSERT INTO posts (
                    id,
                    post_type,
                    parent_id,
                    accepted_answer_id,
                    creation_date,
                    score,
                    view_count,
                    body,
                    owner_user_id,
                    last_editor_user_id,
                    last_editor_display_name,
                    last_edit_date,
                    last_activity_date,
                    community_owned_date,
                    closed_date,
                    title,
                    tags,
                    answer_count,
                    comment_count,
                    favorite_count)
                    VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,
                            %s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"""

                    record_to_insert = (Id,
                                        PostTypeId,
                                        ParentId,
                                        AcceptedAnswerId,
                                        CreationDate,
                                        Score,
                                        ViewCount,
                                        Body,
                                        OwnerUserId,
                                        LastEditorUserId,
                                        LastEditorDisplayName,
                                        LastEditDate,
                                        LastActivityDate,
                                        CommunityOwnedDate,
                                        ClosedDate,
                                        Title,
                                        Tags,
                                        AnswerCount,
                                        CommentCount,
                                        FavoriteCount)

                    # insert the record

                    cursor.execute(postgres_insert_query, record_to_insert)
                    connection.commit()
                    count = cursor.rowcount
                    print(count, "Record inserted successfully "
                                 "into mobile table")

                    if i > 10000:
                        break
    except (Exception, psycopg2.Error) as error:
        print("PostgreSQL error:  ", error)

    finally:
        # closing database connection.
        if(connection):
            cursor.close()
            connection.close()
            print("PostgreSQL connection is closed")
#            text = elem.text
#            text.strip()
#            if text != '':
#                print(text, end='')
#            elif event == 'end':
#                print('</%s>' % elem.tag)


else:
    print('file not found')
