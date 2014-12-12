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

for file in $packageFiles
do
	specPackageName=`echo $file | cut -f 2 -d '/'`_release
	echo Updating $specPackageName version $specOldVersion to version $specNewVersion
	sed -i "s/$specPackageName $specOldVersion/$specPackageName $specNewVersion/" "$file"
done
