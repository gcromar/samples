# -*- coding: utf-8 -*-
"""
Created on Mon Mar 23 15:22:38 2020

@author: Graham
"""

import os

# =============================================================================
# Main line
# =============================================================================

# Check file path
inPath = os.path.normpath('c:\\users\\graham\\desktop\\Reactome_Mappings'
                          '\\Ensembl2Reactome_All_Levels.txt')
outPath = os.path.normpath('c:\\users\\graham\\desktop\\Reactome_Mappings'
                           '\\reactome_full_annotation.txt')

exists = os.path.isfile(inPath)

if exists:
    # Open file handles

    IF = open(inPath, 'rU')
    OF = open(outPath, 'w')

    # Write the header
    OF.write("(species=Mus musculus)(type=pathway)(curator=REACTOME)\n")
    print("(species=Mus musculus)(type=pathway)(curator=REACTOME)")

    # Read each record and parse

    for record in IF:

        fields = record.split('\t')

        if (str(fields[0]).startswith('ENSMUS') is True):

            # Map the fields

            protein = fields[0]
            annotation = fields[1]

            # Data cleanup

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
