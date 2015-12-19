#!/bin/sh -e
version=$1
namespace="biogrid_ontologies"
author="biogrid_team"

tabFiles="./tab-files/"
generator="./generator/Tab2OBO.py"
python="/usr/bin/python"

$python $generator -i $tabFiles/BioGRIDParticipantTags.txt -o BioGRIDParticipantTags.obo -v $version -n $namespace -a $author
$python $generator -i $tabFiles/BioGRIDChemicalActions.txt -o BioGRIDChemicalActions.obo -v $version -n $namespace -a $author
$python $generator -i $tabFiles/BioGRIDExperimentalSystems.txt -o BioGRIDExperimentalSystems.obo -v $version -n $namespace -a $author
$python $generator -i $tabFiles/BioGRIDPhenotypeTypes.txt -o BioGRIDPhenotypeTypes.obo -v $version -n $namespace -a $author
$python $generator -i $tabFiles/BioGRIDPostTranslationalModifications.txt -o BioGRIDPostTranslationalModifications.obo -v $version -n $namespace -a $author
$python $generator -i $tabFiles/BioGRIDSources.txt -o BioGRIDSources.obo -v $version -n $namespace -a $author
$python $generator -i $tabFiles/BioGRIDThroughput.txt -o BioGRIDThroughput.obo -v $version -n $namespace -a $author
$python $generator -i $tabFiles/BioGRIDPostTranslationalModificationIdentities.txt -o BioGRIDPostTranslationalModificationIdentities.obo -v $version -n $namespace -a $author