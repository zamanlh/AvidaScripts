"""
A class used to manipulate Avida genomes. 

"""

import gzip
import sys
import copy
import random
import os
import csv
from numpy import loadtxt, mean

__author__ = """Luis Zaman (luis.zaman@gmail.com)"""

class GenomeManipulator:
    """
    A class built to manipulate Avida genomes in various ways including 
    generating different types of mutations, converting genomes (list of 
    instructions) to sequences (string of letters representing instructions),
    and sequences to genomes.
    
    """
    inst_hash = {} #hash from instruction string to sequence char
    rev_inst_hash = {} #hash from sequence char to instruction string
    char_lookup = [] #list of characters used as shorthand
    
    def __init__(self, inst_set_path):
        """Initialize a GenomeManipulator object with a particular inst_set.
        
        Parameters
        ----------
        inst_set_path : path to instruction set file
            This instruction set file contains the definition and 
            configuration of instructions that may be used by
            Avida organisms in their genome.
        
        """
        try:
            inst_file = open(inst_set_path)
        except IOError, e:
            print "Cannot open instruction set file"
            raise
            
        inst_contents = inst_file.read()
        inst_file.close()
        inst_data =  [i.strip().split(' ')[1].strip() 
            for i in inst_contents.split('\n') if len(i) > 1 and 
            i[0] != "#" and (not i.startswith("INSTSET"))]

        for i in xrange(len(inst_data)):
        	if i < 26:
        		self.char_lookup.append(chr(ord('a') + i))
        	else:
        		self.char_lookup.append(chr(ord('A') + (i-26)))

        for i in xrange(len(inst_data)):
        	self.inst_hash[self.char_lookup[i]] = inst_data[i]
        	self.rev_inst_hash[inst_data[i]] = self.char_lookup[i]

    def genome_to_sequence(self, genome):
        """Convert a list of instructions into a sequence of chars
        
        Parameters
        ----------
        genome :  list of instructions
            The genome is a list of instructions from the instruction set 
            used in the creation of this class, and is case sensitive.
            
        """
        return [self.rev_inst_hash[g] for g in genome]
  
    def sequence_to_genome(self, sequence):
        """Convert a sequence of chars into a list of instructions
        
        Parameters
        ----------
        sequence :  string of char representations of each instruction
            Avida often reports back these genomic sequences which are based
            on assigning instructions in the instruction set a single char
            representation as shorthand.
            
        """

        return [self.inst_hash[s] for s in sequence]
        
    def generate_all_insertion_mutants(self, sequence):
        """Return a list of sequences with all possible insertion mutants
            
        Parameters
        ----------
        sequence :  string of char representations of each instruction
            Avida often reports back these genomic sequences which are based
            on assigning instructions in the instruction set a single char
            representation as shorthand.
            
        """
        ancestor_sequence = list(sequence)
        all_insertion_mutants = []
  
        #make all insertions, (+1 for insertion off the last instruction)
        for i in range(len(sequence) + 1):
            for new_char in self.char_lookup:
                new_seq = list(ancestor_sequence)
                new_seq.insert(i, new_char)
                all_insertion_mutants.append(''.join(new_seq))
                
        return all_insertion_mutants
        
    def generate_all_deletion_mutants(self, sequence):
        """Return a list of sequences with all possible deletion mutants
            
        Parameters
        ----------
        sequence :  string of char representations of each instruction
            Avida often reports back these genomic sequences which are based
            on assigning instructions in the instruction set a single char
            representation as shorthand.
            
        """
        ancestor_sequence = list(sequence)
        all_deletion_mutants = []
  
        #deletions
        for i in range(len(sequence)):
            new_seq = list(ancestor_sequence)
            new_seq.pop(i)
            all_deletion_mutants.append(''.join(new_seq))
            
        return all_deletion_mutants
    
    def generate_all_point_mutants(self, sequence):
        """Return a list of sequences with all possible deletion mutants
            
        Parameters
        ----------
        sequence :  string of char representations of each instruction
            Avida often reports back these genomic sequences which are based
            on assigning instructions in the instruction set a single char
            representation as shorthand.
            
        """
        ancestor_sequence = list(sequence)
        all_point_mutants = []
  
        #and point mutations
        for i in range(len(sequence)):
            for new_char in self.char_lookup:
                new_seq = list(ancestor_sequence)
          
                #avoid calling ancestral state a "mutant"
                if new_seq[i] != new_char:
                    new_seq[i] = new_char
                    all_point_mutants.append(''.join(new_seq))
                    
        return all_point_mutants
  
    def generate_all_mutants(self, sequence):
        """Return a list of sequences with all possible mutants
            
        Parameters
        ----------
        sequence :  string of char representations of each instruction
            Avida often reports back these genomic sequences which are based
            on assigning instructions in the instruction set a single char
            representation as shorthand.
            
        """

        return(self.generate_all_deletion_mutants(sequence)
            + self.generate_all_insertion_mutants(sequence) 
            + self.generate_all_point_mutants(sequence))
