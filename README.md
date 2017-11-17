## Introduction

Kraken is tool for assigning taxonomy to DNA sequences and while a powerful tool, its output can be overly verbose for applications where all the information you need is the overall taxonomic composition for a sample.
This tool was used to determine the composition of Illumina draft assemblies for a manuscript where we wanted to exclude contaminated samples from further analyses. 

## Release 1.0
sumKrakenResults will summarize the percent composition of a genome assembly using the output of kraken-translate. 

## Useage

1) Classify an assembly using Kraken
kraken --db minikraken_20141208/ ERR1759247.fasta > ERR1759247.kraken;

2) Run Kraken translate on kraken file
kraken-translate --db minikraken_20141208/ ERR1759247.kraken;

3) Summarize the results of the kraken-translate output as a percentage of the total number of bases in the sample

Default useage: The full taxonomy of the kraken output will be used and contigs smaller than 1000bp will be removed
python sumKrakenResults.py --krakenfile ./example/ERR1759247.txt --fastafile ./example/ERR1759247.fasta 


Filtering the output: The complete taxonomy can complicate interpreting results when you are only interested in the composition at the family, genus, species ranks. So sumKrakenResults allows you to select up to which numerical taxonomic rank you want to consider to reduce some of the complexity in the results. In this example, I want to know the genus composition of
the kraken output so I specify that the output should include upto the 8th rank in the list. 

python sumKrakenResults.py --krakenfile /Users/jrobertson/PycharmProjects/sra-manuscript/example/ERR1759247.txt --fastafile /Users/jrobertson/PycharmProjects/sra-manuscript/example/ERR1759247.fasta --tax_division 8

|File|TaxaSlice|Total Genome Size|Filtered Genome Size|Taxon|PercentAbundance
|----------------|----|-------|-------|-----------------------------------------------------------------------------------------------------------------------|
|ERR1759247.fasta|0:8|4685246|4659423|root;cellular organisms;Bacteria;Proteobacteria;Gammaproteobacteria;Enterobacteriales;Enterobacteriaceae;Salmonella|100.0|

**Note: NCBI taxonomy can have multiple taxonomic divisions so a slice of up to the 8th item for your taxon may not capture the genus because there are more/fewer taxonomic ranks. 

## Dependancies

Kraken https://ccb.jhu.edu/software/kraken/


## Contact

James Robertson - james.robertson@phac-aspc.gc.ca

## License

Licensed under the Apache License, Version 2.0 (the "License"); you may not use this work except in compliance with the License. You may obtain a copy of the License at:

http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software distributed under the License is distributed on an "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the License for the specific language governing permissions and limitations under the License.