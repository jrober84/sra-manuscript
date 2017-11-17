#!/usr/bin/env python
from __future__ import print_function
from Bio import SeqIO
import logging
from argparse import (ArgumentParser, FileType)
import sys, os

def parse_args():
    "Parse the input arguments, use '-h' for help"
    parser = ArgumentParser(description='Summarize the kraken translate output taxon composition of an assembly')
    parser.add_argument('--krakenfile', type=str, required=True, help='Input kraken translate taxon file to process')
    parser.add_argument('--fastafile', type=str, required=True, help='Input fasta file to process')
    parser.add_argument('--size_cutoff', type=str, required=False, help='minuimum contig length', default=1000)
    parser.add_argument('--tax_division', type=str, required=False, help='Taxon Numerical rank to truncate at', default=-1)
    return parser.parse_args()

def read_fasta_dict(fasta_file):
    seqs = dict()
    with open(fasta_file, "r") as handle:
        for record in SeqIO.parse(handle, "fasta"):
            seqs[str(record.id)] = str(record.seq)
    handle.close()
    return seqs

def read_kraken_dict(kraken_file):
    taxa = dict()
    with open(kraken_file, "r") as fh:
        content = fh.readlines()
        content = [x.strip() for x in content]
        for line in content:
            row = line.split("\t")
            if len(row) >= 2:
                taxa[row[0]] = row[1]
    return taxa

def summarize_taxa(contig_taxa_dict,contig_sizes,tax_division):
    taxa_info = dict()
    total_bases = 0

    for contig_id in contig_taxa_dict:
        if not contig_id in contig_sizes:
            continue

        taxon = contig_taxa_dict[contig_id]

        if tax_division != -1:
            taxon = ";".join(taxon.split(';')[0:tax_division])


        length = contig_sizes[contig_id]
        total_bases+= length

        if not taxon in taxa_info:
            taxa_info[taxon] = 0

        taxa_info[taxon]+= length

    for taxon in taxa_info:
        taxa_info[taxon] = float(taxa_info[taxon]) / total_bases * 100


    return taxa_info




def main():

    args = parse_args()
    if not args.krakenfile:
        logging.info('Error, no krakenfile taxon file specified, please specify one')
        sys.exit()

    if not args.fastafile:
        logging.info('Error, no fasta file specified, please specify one')
        sys.exit()
    args.size_cutoff = int(args.size_cutoff)
    if not isinstance(args.size_cutoff,int):
        logging.info('Error, size limit is not an integer')
        sys.exit()

    args.tax_division = int(args.tax_division)
    if not isinstance(args.tax_division,int):
        print (args.tax_division)
        logging.info('Error, taxon rank is not an integer')
        sys.exit()

    tax_division = args.tax_division
    size_cutoff = args.size_cutoff

    kraken_file = args.krakenfile
    if not os.path.exists(kraken_file):
        logging.info('Error, kraken file not found, check path and try again')
        sys.exit()

    fasta_file = args.fastafile
    if not os.path.exists(fasta_file):
        logging.info('Error, fasta file not found, check path and try again')
        sys.exit()

    #Get the sizes of each contig
    fasta_dict = read_fasta_dict(fasta_file)
    contig_lengths = dict()
    filtered_genome_length = 0
    total_genome_length = 0
    for seqid in fasta_dict:
        seq_len = len(fasta_dict[seqid])
        total_genome_length += seq_len
        if seq_len < size_cutoff:
            continue
        filtered_genome_length+= seq_len
        contig_lengths[seqid] = len(fasta_dict[seqid])

    del(fasta_dict)

    #Get Taxa associations from kraken file
    contig_taxa_dict = read_kraken_dict(kraken_file)
    taxa_representation = summarize_taxa(contig_taxa_dict,contig_lengths,tax_division)

    #Print sample composition as a representation of the total number of bases present
    print("File\tTaxaSlice\tTotal Genome Size\tFiltered Genome SizeTaxon\tPercentAbundance")
    if tax_division == -1:
        div = 'Full'
    else:
        div = "{}:{}".format(0,tax_division)

    for taxa in taxa_representation:
        print("{}\t{}\t{}\t{}\t{}\t{}".format(os.path.basename(fasta_file),div,total_genome_length,filtered_genome_length,taxa,taxa_representation[taxa]))




main()



