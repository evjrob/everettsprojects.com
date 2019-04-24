#!/bin/bash

# example use:
# [~/.../_drafts/]$ ../convert.sh jupyter_notebook_filename.ipynb 
# 

BUILD_DIR="$PWD/" 
POST_DIR="/home/everett/Development/everettsprojects.com/_posts/"
IMG_DIR="/home/everett/Development/everettsprojects.com/img/"

# use nbconvert on the file
jupyter nbconvert --to markdown $1 --config ../jekyll.py

# copies the file to a newly named file
ipynb_fname="$1"
md_fname="${ipynb_fname/ipynb/md}"
dt=`date +%Y-%m-%d`
fname="$dt-$md_fname"
mv $BUILD_DIR$md_fname $BUILD_DIR$fname
echo "file name changed from $1 to $fname"

# adds the date to the file
dt2=`date +"%b %d, %Y"`
sed -i "3i date: $dt2" $BUILD_DIR$fname
echo "added date $dt2 to line 3"

# Gets the title of the post
echo "What's the title of this post going to be?"
read ttl
sed -i "4i title: \"$ttl\"" $BUILD_DIR$fname
echo "added title $ttl in line 4"

# Copy images over
imgs_exist=false

if [ -d "$BUILD_DIR/img" ]; then
  img_dir_name="$dt-${ipynb_fname/.ipynb/}"
  cp -r "$BUILD_DIR/img" "$IMG_DIR/$img_dir_name"
  imgs_exist=true
fi

if [ -d "$BUILD_DIR/${ipynb_fname/.ipynb/}_files/" ]; then
  cp -r "$BUILD_DIR/${ipynb_fname/.ipynb/}_files/" "$IMG_DIR/$img_dir_name/${ipynb_fname/.ipynb/}_files/"
  imgs_exist=true
fi

# Fix image paths on md file
sed -i "s/img\//\/img\/sed_temp_path\//g" $BUILD_DIR$fname
sed -i "s/sed_temp_path/$img_dir_name/g" $BUILD_DIR$fname
echo "Corrected image paths"

# if the current version is newer than the version in _posts
if [[ $1 -nt $POST_DIR$fname ]]; then
  mv $BUILD_DIR$fname $POST_DIR$fname
  echo "moved $fname from $BUILD_DIR to $POST_DIR"
  echo -e "\e[32m Process Completed Successfully \e[0m"
else
  echo -e "\e[31m $1 older than the version in $POST_DIR, not overwriting $POST_DIR$fname \e[0m"
fi
