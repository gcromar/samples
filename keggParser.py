# -*- coding: utf-8 -*-
"""
Created on Mon Mar 18 14:43:06 2020

@author: Graham
"""

import os

# =============================================================================
# Main line
# =============================================================================

# Check file path
inPath = os.path.normpath('c:\\users\\graham\\desktop\\KEGG_Mappings'
                          '\\kegg_cleanup.txt')
outPath = os.path.normpath('c:\\users\\graham\\desktop\\KEGG_Mappings'
                           '\\kegg_full_annotation.txt')

exists = os.path.isfile(inPath)

if exists:
    # Open file handles

    IF = open(inPath, 'rU')
    OF = open(outPath, 'w')

    # Write the header
    OF.write("(species=Mus musculus)(type=pathway)(curator=KEGG)\n")
    print("(species=Mus musculus)(type=pathway)(curator=Me)")

    # Read each record and parse

    for record in IF:

        fields = record.split('\t')

        if (fields[0] == "A" or fields[0] == "B"):
            continue

        if (fields[0] == "C"):

            # Capture the annotation number
            annotation = fields[1]

            # Zero fill to six characters
            annotation = annotation.zfill(6)

        if (fields[0] == "D"):

            protein = fields[2]

            # Clean protein identifier
            protein = protein.rstrip(";")

            # Print the result
            # print(protein, " = ", annotation)
            elements = (protein, annotation)
            separator = ' = '
            output = separator.join(elements)
            OF.write(output)
            OF.write('\n')
            print(output)

    IF.close()
    OF.close()

else:
    print('file not found')
