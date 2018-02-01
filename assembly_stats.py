#!/usr/bin/env python
""" A simple script to calculate some basic assembly stats."""

import sys
import re

if len(sys.argv) != 2:
    print "Usage: ./assembly.stats.py <assembly (fasta) file>\n"
    quit()

assembly = open(sys.argv[1], "r")

assembly_dict = {}
scaffolds = 0

# Reads the assembly into a dictionary
for line in assembly:
    if line.startswith(">"):
        regex = re.match(">(.*?)", line.strip())
        header = regex.group(1)
        assembly_dict[header] = ""
        scaffolds += 1
    else:
        assembly_dict[header] += line.strip()
assembly.close()

assembly_length = 0
scaffold_lengths = []
A = 0
G = 0
C = 0
T = 0
N = 0

# Calculates numbers of A|T|G|C|N as well as total assembly length
for item in assembly_dict:
    scaffold_lengths.append(len(assembly_dict[item]))
    assembly_length += len(assembly_dict[item])

    A += assembly_dict[item].upper().count("A")
    this_a = assembly_dict[item].upper().count("A")

    T += assembly_dict[item].upper().count("T")
    this_t = assembly_dict[item].upper().count("T")

    G += assembly_dict[item].upper().count("G")
    this_g = assembly_dict[item].upper().count("G")

    C += assembly_dict[item].upper().count("C")
    this_c = assembly_dict[item].upper().count("C")

    N += assembly_dict[item].upper().count("N")
    this_n = assembly_dict[item].upper().count("N")

    if (this_a + this_t + this_g + this_c + this_n) != len(assembly_dict[item]):
        print "%s had one or more characters not A|T|G|C|N\n" % item


scaffold_lengths.sort(reverse = True)
length = 0
for item in scaffold_lengths:
    length += item
    if length >= (assembly_length / 2):
        N50 = item
        break

all_bases_N = A + G + C + T + N
all_bases = A + G + C + T
GC_N = (float(G + C) / all_bases_N) * 100
GC = (float(G + C) / all_bases) * 100

# Writes the stats to an output file
stats = open(sys.argv[1] + ".assembly_stats", "w")
stats.write("Number of scaffolds: %s\n" % scaffolds)
stats.write("Total assembly length: %s\n" % assembly_length)
stats.write("N50: %s\n" % N50)
stats.write("Number of As: %s\n" % A)
stats.write("Number of Ts: %s\n" % T)
stats.write("Number of Gs: %s\n" % G)
stats.write("Number of Cs: %s\n" % C)
stats.write("Number of Ns: %s\n" % N)
stats.write("GC content (with Ns): %s\n" % GC_N)
stats.write("GC content (without Ns): %s\n" % GC)
stats.write("assembly_length / all_bases_N (to see if my script screwed up or \
             something): %s\n" % (float(assembly_length / all_bases_N)))

# Prints the stats to the screen
print "Number of scaffolds: %s" % scaffolds
print "Total assembly length: %s" % assembly_length
print "N50: %s" % N50
print "Number of As: %s" % A
print "Number of Ts: %s" % T
print "Number of Gs: %s" % G
print "Number of Cs: %s" % C
print "Number of Ns: %s" % N
print "GC content (with Ns): %s" % GC_N
print "GC content (without Ns): %s" % GC
print "all bases (minus Ns): %s" % all_bases
print "all bases (with Ns): %s" % all_bases_N
print "File with the above statistics: %s" % (sys.argv[1] + ".assembly_stats")
