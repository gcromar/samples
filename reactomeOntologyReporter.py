# -*- coding: utf-8 -*-
"""
Created on Fri Apr 10 16:05:43 2020

@author: Graham
"""

import os
on = []  # list to hold records in file
p = {}   # dictionary for parent terms
c = {}   # dictionary for child terms

# =============================================================================
# Main line
# =============================================================================

# Check file paths
inPath = os.path.normpath('c:\\users\\graham\\desktop\\Reactome_Mappings'
                          '\\Reactome_MM_Ontology_Sort_20.txt')
#                          '\\reactomeMMUltimateParsable.txt')
#                         '\\Reactome_MM_Ontology_Sort_13.txt')
#                         '\\ReactomeMMURelations')

# Process main file

exists = os.path.isfile(inPath)

if exists:
    # Open file handle

    IF = open(inPath, 'r')

    # Read each record and parse

    i = 0

    for record in IF:

        on.append(record)

        # Map the fields
        fields = record.split('=')
        parentField = fields[1].rstrip('\n')
        parentList = parentField.split(' ')
        childTerm = fields[0]

        # print(childTerm, " = ", parentList)

        # Load child dictionary
        iList = []
        if childTerm in c:
            iList = c[childTerm]
            iList.append(i)
            iList.sort()
            c[childTerm] = iList
        else:
            iList.append(i)
            c[childTerm] = iList  # list of where that child record exists

        for parentTerm in parentList:

            # Load parent dictionary
            iList = []
            if parentTerm in p:
                iList = p[parentTerm]
                iList.append(i)
                iList.sort()
                p[parentTerm] = iList  # where parent is listed
            else:
                iList.append(i)
                p[parentTerm] = iList

        i = i + 1

    IF.close()

#        Print some diagnostics
#        for key, value in c.items():
#           print(key, value)
#        for key, value in p.items():
#           print(key, value)

    # Report children used before definition as parent
    i = 0
    for child, value in c.items():
        cLowest = value[0]
        if child in p:
            pList = p[child]
            pLowest = pList[0]
            if pLowest < cLowest:
                # report a problem
                i = i + 1
                print(i, ".  ", child, " used at ", pLowest,
                      " defined at ", cLowest)
#             else:
                # print("Child ", child, " not found in parent list")

else:
    print('file 1 not found')
