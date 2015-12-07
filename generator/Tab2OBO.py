#!/bin/env python

# This script will validate and convert a custom formatted tab-delimited text file
# into an OBO file based on input parameters.

import sys, string
import argparse
import time
import collections

generatingTool = "BioGRID Tab2OBO 0.0.1a"
formatVersion = "1.2"
colCount = 6

# Process Command Line Input
argParser = argparse.ArgumentParser( description = 'Convert tab delimited text into an OBO file' )
argParser.add_argument( '--input', '-i', action='store', nargs=1, help='The input tab-delimited file', required=True )
argParser.add_argument( '--output', '-o', action='store', nargs=1, help='The output obo file', required=True )
argParser.add_argument( '--version', '-v', action='store', nargs=1, help='The data version you wish to assign to the new obo file. Example: 2.3.3', required=True )
argParser.add_argument( '--namespace', '-n', action='store', nargs=1, help='A default namespace for the overall file. Example: biogrid_ontologies', required=True )
argParser.add_argument( '--author', '-a', action='store', nargs=1, help='The author of the file. Example: BioGRID-Team', required=True )
inputArgs = argParser.parse_args( )

runDate = time.strftime( '%d:%m:%Y %H:%M' )

ontologyTerms = collections.OrderedDict( )
hasErrors = False

with open( inputArgs.input[0], 'r' ) as fp :
	isFirst = True
	lineCount = 0
	for line in fp :
	
		lineCount += 1
	
		# Skip Header Line
		if isFirst:
			isFirst = False
			continue
			
		line = line.strip( )
		
		# Skip blank Lines
		if "" == line :
			continue
			
		splitLine = line.split( "\t" )
		if len(splitLine) != colCount :
			print "ERROR ON LINE " + str(lineCount) + ": Needs to be " + str(colCount) + " columns long! Found " + str(len(splitLine)) + " instead. Place 'none' in empty columns!" 
			hasErrors = True
			continue
			
		termID = splitLine[0].strip( )
		termName = splitLine[1].strip( )
		termDef = splitLine[2].strip( )
		termDefSource = splitLine[3].strip( )
		termRelationship = splitLine[4].strip( ).split( "|" )
		termObsolete = splitLine[5].strip( )
		
		if termObsolete.lower( ) == "true" :
			termObsolete = True
		else :
			termObsolete = False
		
		if termID.lower( ) in ontologyTerms :
			print "ERROR ON LINE " + str(lineCount) + ": Duplicate term id used in already!"  
			hasErrors = True
			continue
		
		ontologyTerms[termID.lower( )] = { "ID" : termID, "NAME" : termName, "DEF" : termDef, "DEF_SOURCE" : termDefSource, "RELATIONSHIP" : termRelationship, "OBSOLETE" : termObsolete }
				
if hasErrors :
	print "Output File Not Generated Due to Errors Above"
else :
	
	with open( inputArgs.output[0], 'w' ) as fp :
	
		fp.write( "format-version: " + str(formatVersion) + "\n" )
		fp.write( "data-version: " + str(inputArgs.version[0]) + "\n" )
		fp.write( "date: " + runDate + "\n" )
		fp.write( "saved-by: " + inputArgs.author[0] + "\n" )
		fp.write( "auto-generated-by: " + generatingTool + "\n" )
		fp.write( "default-namespace: " + inputArgs.namespace[0] + "\n" )
	
		for (termID, ontologyTerm) in ontologyTerms.items( ) :
			fp.write( "\n" )
			fp.write( "[Term]\n" )
			fp.write( "id: " + ontologyTerm['ID'] + "\n" )
			fp.write( "name: " + ontologyTerm['NAME'] + "\n" )
			
			# Don't output the DEF term at all if no definition
			# is found to display
			if ontologyTerm["DEF"].lower( ) != "none" :
				fp.write( "def: \"" + ontologyTerm['DEF'].replace( "\"", "" ) + "\"" )
				
				if ontologyTerm["DEF_SOURCE"] != "none" :
					fp.write( " [" + ontologyTerm['DEF_SOURCE'] + "]" )
					
				fp.write( "\n" )
			
			# Print all Relationships if the term it's related to
			# can also be found in the ontology
			for relationship in ontologyTerm['RELATIONSHIP'] :
				if relationship.lower( ) != "root" and relationship.lower( ) != "none" :
					if relationship.lower( ) not in ontologyTerms :
						print "ERROR: " + termID + " has a relationship with " + relationship + " but this term is not in the ontology! This relationship was skipped!"
					else :
						relatedTerm = ontologyTerms[relationship.lower( )]
						fp.write( "is_a: " + relationship + " ! " + relatedTerm['NAME'] + "\n" )
			
			# Only output Obsolete if it's obsolete
			# no is_obsolete implcitly implies it is not obsolete
			if ontologyTerm['OBSOLETE'] :
				fp.write( "is_obsolete: true\n" )

sys.exit(0)