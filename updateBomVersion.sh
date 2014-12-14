#!/bin/bash

# updateBomVersion.sh

# This script is used to update versions for buildoop recipes
# The version update is a mandatory step before tagging a branch
# to freeze a buildoopRecipes version

# Usage:
# run it in the packages directory (where is placed after cloning the repository)
# ./updateBomVersion.sh <newVersion>

if [ $# -ne 1 ]
then
	echo -e "\nERROR: Specify new version number\n"
	echo -e "usage: updateBomVersion.sh <newVersion>\n"
	exit
fi

# Get new and old bom file names
bomNewVersion=$1.bom
bomOldVersion=`find -name '*.bom' | cut -f 2 -d '/'`

# Get current version from Bom file
newVersion=$1
oldVersion=${bomOldVersion%.*}
#oldVersion=openbus0.0.1

specOldVersion=`echo $oldVersion | sed s/-/_/g`
specNewVersion=`echo $newVersion | sed s/-/_/g`

# Debug purpose
#echo " oldVersion: $oldVersion -->  newVersion: $newVersion"
#echo " bomOldVersion: $bomOldVersion --> bomNewVersion: $bomNewVersion"
#echo " specOldVersion: $specOldVersion --> specNewVersion: $specNewVersion "

# Update bom name file to new version 
echo Renaming $bomOldVersion to $bomNewVersion
mv $bomOldVersion $bomNewVersion

# Update al rpm .spec files from recipes
packageFiles=`find . -name '*.spec'`

# Red color for prinit errors
red='\033[0;31m'
NC='\033[0m' # No Color

for file in $packageFiles
do
	specPackageName=`echo $file | cut -f 2 -d '/'| sed s/-/_/g`_release
	
	echo Updating $specPackageName version $specOldVersion to version $specNewVersion
	nameFind=`grep -r $specPackageName $file | wc -l`
	if [ $nameFind -ge 1 ]
	then
		sed -i "s/$specPackageName $specOldVersion/$specPackageName $specNewVersion/" "$file"
	else
		echo -e "${red}\nFile $file and release name in spec file ($specPackageName) doesn't match ${NC}"
	fi
done
