# -*- coding: utf-8 -*-
"""
Created on Sat Apr 11 10:24:07 2020

@author: Graham
-------------------------------------------------------------------------------
Note:  The purpose of the post assembler is to take a sorted file of
       records in [child=p1 p2 p3...] format and output these records
       as child description [isa: p1 p2 p3...] format.  The required
       header line will also be created.  However, manual editing will
       be required to add the top level pathways immediately after the
       header:

R-MMU-00001 = Reactome_Pathway
R-MMU-9612973 = Autophagy [isa: R-MMU-00001]
R-MMU-1640170 = Cell Cycle [isa: R-MMU-00001]
R-MMU-1500931 = Cell-Cell communication [isa: R-MMU-00001]
R-MMU-8953897 = Cellular responses to external stimuli [isa: R-MMU-00001]
R-MMU-4839726 = Chromatin organization [isa: R-MMU-00001]
R-MMU-1266738 = Developmental Biology [isa: R-MMU-00001]
R-MMU-8963743 = Digestion and absorption [isa: R-MMU-00001]
R-MMU-1643685 = Disease [isa: R-MMU-00001]
R-MMU-73894 = DNA Repair [isa: R-MMU-00001]
R-MMU-69306 = DNA Replication [isa: R-MMU-00001]
R-MMU-1474244 = Extracellular matrix organization [isa: R-MMU-00001]
R-MMU-74160 = Gene expression (Transcription) [isa: R-MMU-00001]
R-MMU-109582 = Hemostasis [isa: R-MMU-00001]
R-MMU-168256 = Immune System [isa: R-MMU-00001]
R-MMU-1430728 = Metabolism [isa: R-MMU-00001]
R-MMU-392499 = Metabolism of proteins [isa: R-MMU-00001]
R-MMU-8953854 = Metabolism of RNA [isa: R-MMU-00001]
R-MMU-397014 = Muscle contraction [isa: R-MMU-00001]
R-MMU-112316 = Neuronal System [isa: R-MMU-00001]
R-MMU-1852241 = Organelle biogenesis and maintenance [isa: R-MMU-00001]
R-MMU-5357801 = Programmed Cell Death [isa: R-MMU-00001]
R-MMU-9609507 = Protein localization [isa: R-MMU-00001]
R-MMU-1474165 = Reproduction [isa: R-MMU-00001]
R-MMU-162582 = Signal Transduction [isa: R-MMU-00001]
R-MMU-382551 = Transport of small molecules [isa: R-MMU-00001]
R-MMU-5653656 = Vesicle-mediated transport [isa: R-MMU-00001]

       As a final manual step, a global search/replace will need to be
       done to remove the "R-MMU-" prefixes from all identifiers because
       BiNGO will only accept numeric identifiers.
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
                          '\\reactome_MM_Ontology_Sort_20.txt')
#                          '\\ReactomePathwaysRelation.txt')
lookupPath = os.path.normpath('c:\\users\\graham\\desktop\\Reactome_Mappings'
                              '\\ReactomePathways.txt')
outPath = os.path.normpath('c:\\users\\graham\\desktop\\Reactome_Mappings'
                           '\\reactomeMMUltimate20.txt')
#                           '\\reactomeMMUltimate.txt')
#                           '\\reactome.txt')

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

    # print(d)

else:
    print('secondary file not found')
    exit

# ------------------
# Process main file
# ------------------
exists = os.path.isfile(inPath)

if exists:

    # Open file handles
    IF = open(inPath, 'r')
    OF = open(outPath, 'w')

    # Write the header
    OF.write("(curator=REACTOME)(type=pathway)\n")
    print("(curator=KEGG)(type=pathway)")

    # Read each record and parse
    for record in IF:

        # Map the fields
        fields = record.split('=')
        childTerm = fields[0]
        parentTerms = fields[1].rstrip("\n")

        # Retrieve description of child term
        description = d.get(childTerm)
        # print(description)

        # Print the result
        elements = (childTerm, " = ", description, " [isa: ", parentTerms, "]")
        separator = ''
        output = separator.join(elements)
        print(output)
        OF.write(output)
        OF.write("\n")

    IF.close()
    OF.close()

else:
    print('file not found')
