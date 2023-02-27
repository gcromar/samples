# -*- coding: utf-8 -*-
"""
Created on Tue Jan 26 10:39:39 2021

@author: Graham

Purpose:  The purpose of this program is to parse a prot2HG feature file
          in .csv format and create a subset of the data corresponding to
          a gene list and whether a feature is a region that overlaps the
          coverage area of a probeset defined in .BED format.

Note:     Caution should be taken to ensure that the regions defined in
          both the .BED file and feature file are consistent with the same
          level of sequence assembly.  Here, prot2HG features were
          downloaded for hg38 and the .BED file from Agilent was obtained
          in hg19 and uplifted to hg38 using the tool:
          https://genome.ucsc.edu/cgi-bin/hgLiftOver
          prior to running this program.

"""
import re

# covered_regions needs to be a list of class regions -- to be defined


class Region:
    def __init__(self, gene, chromosome, start, end):
        self.gene = gene
        self.chromosome = chromosome
        self.start = start
        self.end = end

    def __repr__(self):
        return self.gene


def is_overlapping_feature(chromosome, start, end, covered_regions):
    overlap = False
    for region in covered_regions:
        if chromosome == region.chromosome:
            if(region.end >= start >= region.start or
               region.start <= end <= region.end or
               start < region.start and end > region.end):
                overlap = True
                break
    return overlap

# =============================================================================
# Main line
# =============================================================================


in_path = 'c:\\users\\graham\\desktop\\prot2hg_1938.csv'
out_path = 'c:\\users\\graham\\desktop\\mini2hg_1938_ok.txt'
bed_path = 'c:\\users\\graham\\desktop\\hglft.bed'

gene_list = ['BGN', 'DCN', 'EFEMP2', 'ELN', 'EMILIN1', 'EMILIN2', 'FBLN1',
             'FBLN2', 'FBLN5', 'FBN1', 'FBN2', 'FBN3', 'FN1', 'GLB1',
             'LTBP1', 'LTBP2', 'LTBP3', 'LTBP4', 'MFAP2', 'MFAP5', 'VCAN']
covered_regions = []
header = True
i = 0

with open(bed_path) as bed_file:
    bed_lines = bed_file.readlines()
    for line in bed_lines:
        chromosome, start, end, gene = line.split('\t')
        covered_region = Region(gene, chromosome, start, end)
        covered_regions.append(covered_region)


with open(in_path, 'r') as infile, open(out_path, 'w') as outfile:
    lines = infile.readlines()
    for line in lines:
        fields = line.split(';')

        # Cleaning
        gene_name = re.sub(r'\W+', r'', fields[1].rstrip())
        strand = re.sub(r'"', r'', fields[4].rstrip())
        site_type = re.sub(r'\W+', r'', fields[5].rstrip())
        domain_name = re.sub(r'\W+', r'', fields[6].rstrip())
        hg38_chr = re.sub(r'\W+', r'', fields[19].rstrip())
        hg38_chr_start = re.sub(r'\W+', r'', fields[20].rstrip())
        hg38_chr_end = re.sub(r'\W+', r'', fields[21].rstrip())

        # Headings
        print(gene_name, site_type)
        if header:
            outfile.write('\t'.join(["Gene", "Strand", "Type", "Name",
                                     "Chr", "Start", "End", "\n"]))
            header = False
        if (gene_name in gene_list and site_type == "Region" and
                hg38_chr_start != "0" and hg38_chr_end != "0" and
                is_overlapping_feature(hg38_chr, hg38_chr_start,
                                       hg38_chr_end, covered_regions)):
            i = i+1
            outfile.write('\t'.join([str(i), gene_name, strand, site_type,
                                     domain_name, hg38_chr, hg38_chr_start,
                                     hg38_chr_end, '\n']))
