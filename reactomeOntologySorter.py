# -*- coding: utf-8 -*-
"""
Created on Fri Apr 10 21:32:09 2020

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
                          '\\Reactome_MM_Ontology_Sort_19.txt')
#                          '\\reactomeMMUltimateParsable.txt')
#                         '\\Reactome_MM_Ontology_Sort_13.txt')
#                         '\\ReactomeMMURelations')

outPath = os.path.normpath('c:\\users\\graham\\desktop\\Reactome_Mappings'
                           '\\reactome_MM_Ontology_Sort_20.txt')
# Process main file

exists = os.path.isfile(inPath)

if exists:
    # Open file handle

    IF = open(inPath, 'r')
    OF = open(outPath, 'w')

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

    # Print some diagnostics
    # for key, value in c.items():
    #    print(key, value)
    # for key, value in p.items():
    #    print(key, value)

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
                # print(i, ".  ", child, " used at ", pLowest,
                #       " defined at ", cLowest)
                print(i, ".  Fixing ", child)
                # swap positions in ontology list
                onTemp = on[cLowest]
                on[cLowest] = on[pLowest]
                on[pLowest] = onTemp
#             else:
            # print("Child ", child, " not found in parent list")

    # Output the newly sorted records
    for line in on:
        OF.write(line)

    OF.close()
    print("Done!")

else:
    print('file 1 not found')
