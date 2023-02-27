# -*- coding: utf-8 -*-
"""
Created on Tue Apr 21 14:39:45 2020

@author: Graham

Purpose:  This program assembles data from multiple files into a csv formatted
          output with binary flags indicating the presence of each gene in
          various categories.  The input files each represent the genes that
          belong to the category indicated by the file name.  The output of
          this data assembly will be read into an R program to render an upset
          plot of the data for publication.
"""

import os
import sys
masterProteinList = {}   # protein{categoryList} dictionary

# =============================================================================
# Files
# =============================================================================

filenames = ["1 - Hip C-up T-up (GeneID).txt",
             "2 - Hip C-up T-down (GeneID).txt",
             "3 - Hip C-down T-up (GeneID).txt",
             "4 - Hip C-down T-down (GeneID).txt",
             "5 - Hip T-up (GeneID).txt",
             "6 - Hip T-down (GeneID).txt",
             "7 - Hip C-up (GeneID).txt",
             "8 - Hip C-down (GeneID).txt",
             "13 - Hip All Interactions (GeneID).txt",
             "14 - Hip All Significant (GeneID).txt",
             "15 - Hip All Toxo (GeneID).txt",
             "16 - Hip All Cocaine (GeneID).txt",
             "17 - Hip All Toxo Up (GeneID).txt",
             "18 - Hip All Toxo Down (GeneID).txt",
             "19 - Hip All Cocaine Up (GeneID).txt",
             "20 - Hip All Cocaine Down (GeneID).txt",
             "1 - Str C-up T-up (GeneID).txt",
             "2 - Str C-up T-down (GeneID).txt",
             "3 - Str C-down T-up (GeneID).txt",
             "4 - Str C-down T-down (GeneID).txt",
             "5 - Str T-up (GeneID).txt",
             "6 - Str T-down (GeneID).txt",
             "7 - Str C-up (GeneID).txt",
             "8 - Str C-down (GeneID).txt",
             "15 - Str All Interactions (GeneID).txt",
             "16 - Str All Significant (GeneID).txt",
             "17 - Str All Toxo (GeneID).txt",
             "18 - Str All Cocaine (GeneID).txt",
             "19 - Str All Toxo Up (GeneID).txt",
             "20 - Str All Toxo Down (GeneID).txt",
             "21 - Str All Cocaine Up (GeneID).txt",
             "22 - Str All Cocaine Down (GeneID).txt",
             "23 - All Significant (GeneID).txt"]

labels = ["H.Cocaine.Up.Toxo.Up",
          "H.Cocaine.Up.Toxo.Down",
          "H.Cocaine.Down.Toxo.Up",
          "H.Cocaine.Down.Toxo.Down",
          "H.Toxo.Up",
          "H.Toxo.Down",
          "H.Cocaine.Up",
          "H.Cocaine.Down",
          "H.All.Interactions",
          "H.All",
          "H.All.Toxo",
          "H.All.Cocaine",
          "H.All.Toxo.Up",
          "H.All.Toxo.Down",
          "H.All.Cocaine.Up",
          "H.All.Cocaine.Down",
          "S.Cocaine.Up.Toxo.Up",
          "S.Cocaine.Up.Toxo.Down",
          "S.Cocaine.Down.Toxo.Up",
          "S.Cocaine.Down.Toxo.Down",
          "S.Toxo.Up",
          "S.Toxo.Down",
          "S.Cocaine.Up",
          "S.Cocaine.Down",
          "S.All.Interactions",
          "S.All",
          "S.All.Toxo",
          "S.All.Cocaine",
          "S.All.Toxo.Up",
          "S.All.Toxo.Down",
          "S.All.Cocaine.Up",
          "S.All.Cocaine.Down",
          "All"]

# =============================================================================
# A note on label meanings
# =============================================================================
# "H.Cocaine.Up.Toxo.Up"  # Cocaine up and Toxo up
# "H.Cocaine.Up.Toxo.Down"  # Cocaine up and Toxo down
# "H.Cocaine.Down.Toxo.Up"  # Cocaine down and Toxo up
# "H.Cocaine.Down.Toxo.Down"  # Cocaine down and Toxo down
# "H.Toxo.Up"  # Toxo up (only)
# "H.Toxo.Down"  # Toxo down (only)
# "H.Cocaine.Up"  # Cocaine up (only)
# "H.Cocaine.Down"  # Cocaine down (only)
# "H.All.Interactions"  # All interactions between toxo and cocaine
# "H.All"  # All significant genes
# "H.All.Toxo"  # All toxo effects irrespective of cocaine
# "H.All.Cocaine"  # All cocaine effects irrespective of toxo
# "H.All.Toxo.Up"  # All toxo up irrespective of cocaine
# "H.All.Toxo.Down"  # All toxo down irrespective of cocaine
# "H.All.Cocaine.Up"  # All cocaine up irrespective of toxo
# "H.All.Cocaine.Down"  # All cocaine down irrespective of toxo
# "S.Cocaine.Up.Toxo.Up"  # Cocaine up and Toxo up
# "S.Cocaine.Up.Toxo.Down"  # Cocaine up and Toxo down
# "S.Cocaine.Down.Toxo.Up"  # Cocaine down and Toxo up
# "S.Cocaine.Down.Toxo.Down"  # Cocaine down and Toxo down
# "S.Toxo.Up"  # Toxo up (only)
# "S.Toxo.Down"  # Toxo down (only)
# "S.Cocaine.Up"  # Cocaine up (only)
# "S.Cocaine.Down"  # Cocaine down (only)
# "S.All.Interactions"  # All interactions between toxo and cocaine
# "S.All"  # All significant genes
# "S.All.Toxo"  # All toxo effects irrespective of cocaine
# "S.All.Cocaine"  # All cocaine effects irrespective of toxo
# "S.All.Toxo.Up"  # All toxo up irrespective of cocaine
# "S.All.Toxo.Down"  # All toxo down irrespective of cocaine
# "S.All.Cocaine.Up"  # All cocaine up irrespective of toxo
# "S.All.Cocaine.Down"  # All cocaine down irrespective of toxo


# =============================================================================
# Mainline
# =============================================================================

# Make a lookup table of files and labels
# =============================================================================
# i = 0
# xref = {}
# for file in filenames:
#     xref[file] = labels[i]
#     i += 1
# =============================================================================

# The file labels are the categories for the header
header = ['Genes'] + labels
header = ','.join(header)

# -----------------------------
# Build master list of proteins
# -----------------------------
# The total list of proteins to categorize is H.All + S.All
masterProteinList = {}  # A dictionary so as to remove duplicates
directory = "c:\\users\\graham\\desktop\\Upset_Mappings"
h_all_file = "14 - Hip All Significant (GeneID).txt"
s_all_file = "16 - Str All Significant (GeneID).txt"
h_elements = (directory, h_all_file)
s_elements = (directory, s_all_file)
h_path = '\\'.join(h_elements)
s_path = '\\'.join(s_elements)
h_normPath = os.path.normpath(h_path)
s_normPath = os.path.normpath(s_path)
h_exists = os.path.isfile(h_normPath)
s_exists = os.path.isfile(s_normPath)

if h_exists and s_exists:
    # Open file handles
    h_IF = open(h_normPath, 'r')
    s_IF = open(s_normPath, 'r')

    # Read records and capture all proteins into master list
    for record in h_IF:
        fields = record.split('\t')
        protein = fields[0]
        protein = protein.strip()
        if protein not in masterProteinList:
            masterProteinList[protein] = []

    for record in s_IF:
        fields = record.split('\t')
        protein = fields[0]
        protein = protein.strip()
        if protein not in masterProteinList:
            masterProteinList[protein] = []

    # Close file handles
    h_IF.close()
    s_IF.close()

else:
    sys.exit("Could not build master list of proteins")

# --------------------
# Categorize proteins
# --------------------
for file in filenames:

    #  Assemble file path
    elements = (directory, file)
    separator = '\\'
    path = separator.join(elements)
    filePath = os.path.normpath(path)

    #  Check file path
    exists = os.path.isfile(filePath)

    if exists:
        # Open file handle
        IF = open(filePath, 'r')

        # Clear currentProteinList
        currentProteinList = {}

        # Process records
        for record in IF:

            fields = record.split('\t')

            # Map the fields
            protein = fields[0]

            # Data cleanup
            protein = protein.strip()

            # Print the result
#            print(protein)

            # Accumulate list of proteins
            currentProteinList[protein] = 'dummy'

        # Close file handle
        IF.close()

        # Record enrollment of all proteins in current category
        for protein in masterProteinList:
            if protein in currentProteinList:
                enroll = "1"
            else:
                enroll = "0"

            enrollment = masterProteinList[protein]
            enrollment.append(enroll)
    else:
        print('file not found:  ', path)

# ------------------
# Write some output
# ------------------
out_file = "genesCategorized2.txt"
out_elements = (directory, out_file)
out_path = '\\'.join(out_elements)
out_normPath = os.path.normpath(out_path)
OF = open(out_normPath, 'w')

OF.write(header)
OF.write('\n')

for protein in masterProteinList:
    print('{},'.format(protein), end='')
    OF.write('{},'.format(protein))
    outList = masterProteinList[protein]
    outList_len = len(outList)-1
    for i, enrollment in enumerate(outList):
        if i == outList_len:
            print('{}'.format(enrollment), end='')
            OF.write('{}'.format(enrollment))
        else:
            print('{},'.format(enrollment), end='')
            OF.write('{},'.format(enrollment))
    print()
    OF.write('\n')
