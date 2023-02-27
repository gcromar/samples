# -*- coding: utf-8 -*-
"""
Created on Thu Apr  9 14:32:26 2020

@author: Graham
-------------------------------------------------------------------------------
Note:  Input to this program is a file containing [parent child] pairs
       and the output is a consolidated file of [child isa: p1,p2,p3...]
       along with an unformatted [child=p1 p2 p3...] records suitable
       for iterative sorting by reactomeOntologyReporter.py and
       reactomeOntologySorter.py  The formatted write to the outPath
       was subsequently disabled as this file is of limited use when unsorted.
       Ultimately this logic should be removed but, the output has been
       left to the console for what use it has in debugging.
       In summary: This program should be used to assemble the various
       parent records into a single child = p1, p2, p3 line prior to the
       iterative sort by the reporter and sorter, and nothing more!
       Post processing by reactomeOntologyPostAssembler.py and some manual
       edits will be required to prepare the ontology for input to BiNGO.
-------------------------------------------------------------------------------
"""

import os
lookup = dict()
on = []  # list to hold records in file
d = {}   # dictionary for term description lookups
p = {}   # dictionary for parent terms
c = {}   # dictionary for child terms

# =============================================================================
# Main line
# =============================================================================



# Check file paths
inPath = os.path.normpath('c:\\users\\graham\\desktop\\Reactome_Mappings'
                          '\\reactome_MM_Ontology_Sort_13.txt')
#                          '\\ReactomePathwaysRelation.txt')
lookupPath = os.path.normpath('c:\\users\\graham\\desktop\\Reactome_Mappings'
                              '\\ReactomePathways.txt')
outPath = os.path.normpath('c:\\users\\graham\\desktop\\Reactome_Mappings'
                           '\\reactomeMMUltimate20.txt')
#                           '\\reactomeMMUltimate.txt')
#                           '\\reactome.txt')
outPath2 = os.path.normpath('c:\\users\\graham\\desktop\\Reactome_Mappings'
                            '\\reactomeMMUltimateParsable20.txt')
#                            '\\reactomeMMUltimateParsable.txt')

# -----------------------------------
# Load look-up table for descriptions
# -----------------------------------
exists = os.path.isfile(lookupPath)

if exists:

    SF = open(lookupPath, 'r')

    for record in SF:
        fields = record.split('\t')
        term = str(fields[0])
        description = fields[1].rstrip("\n")
        # print(term, description)
        d[term] = description

    SF.close()

    print(d)

else:
    print('secondary file not found')
    exit

# ------------------
# Process main file
# ------------------
exists = os.path.isfile(inPath)

if exists:
    # -----------------
    # Open file handles
    # -----------------
    IF = open(inPath, 'r')
    OF = open(outPath, 'w')
    OF2 = open(outPath2, 'w')

    # --------------------------
    # Read each record and parse
    # --------------------------
    i = 0  # relates index in on[] with record where parent and child are found

    for record in IF:

        # Capture records
        on.append(record)

        # Map the fields
        fields = record.split('\t')
        parentTerm = fields[0]
        childTerm = fields[1]

        # Data cleanup
        parentTerm = parentTerm.rstrip("\n")
        childTerm = childTerm.rstrip("\n")

        # Load parent dictionary
        iList = []
        if parentTerm in p:
            iList = p[parentTerm]
            iList.append(i)
            iList.sort()
            p[parentTerm] = iList
        else:
            iList.append(i)
            p[parentTerm] = iList

        # Load child dictionary
        iList = []
        if childTerm in c:
            iList = c[childTerm]
            iList.append(i)
            iList.sort()
            c[childTerm] = iList
        else:
            iList.append(i)
            c[childTerm] = iList

        i = i + 1

    IF.close()

    # -----------------
    # Write the header
    # -----------------
    # The following was removed to accomodate the sort
    # Both the header lines and the top level parents without
    # their own parents will be added manually at the end

    # OF.write("(curator=REACTOME)(type=pathway)\n")
    # print("(curator=KEGG)(type=pathway)")

    # -----------------------------------------------------------
    # Process records in the array, building up parent lists
    # -----------------------------------------------------------
    seen = {}
    for record in on:
        fields = record.split('\t')

        # Map the fields
        parentTerm = fields[0]
        childTerm = fields[1]

        # Data cleanup
        # parentTerm = parentTerm.rstrip("\n")
        childTerm = childTerm.rstrip("\n")
        # print(parentTerm)

        # Retrieve description of child term
        description = d.get(childTerm)
        # print(description)

        # Look for additional parents
        clist = c[childTerm]  # list of locations of all same children
        separator = ' '
        pString = ""
        for childLocation in clist:
            childRecord = on[childLocation]
            line = childRecord.split('\t')
            parentToInclude = line[0].rstrip("\n")  # the parent of that child
            elements = (pString, parentToInclude)
            pString = separator.join(elements)
            # on.pop(childLocation)  # remove from further consideration

        # Print the result
        elements = (childTerm, " = ", description, " [isa:", pString, "]")
        separator = ''
        output = separator.join(elements)

        pString = pString.lstrip(' ')
        elements = (childTerm, "=", pString)
        separator = ''
        output2 = separator.join(elements)

        # Avoid duplicate writes
        if output not in seen:
#            OF.write(output)
#            OF.write('\n')
            OF2.write(output2)
            OF2.write('\n')
            print(output)
            seen[output] = 'dummy'
    OF.close()
    OF2.close()
else:
    print('file not found')
