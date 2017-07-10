#!/bin/bash

# No argument provided - show file Usage
if [ -z "$1" ] ; then
    echo 'Usage:'$0' <Your-Directory>'
    echo "e.g. $0 ~/work/adam-dne"
    exit 1
fi

DIR=$1

# make sure directory does not already exist
if [ -f "$DIR" ]
then
    echo "File $DIR exists, cannot create directory $DIR, please remove file or choose a different name"
    exit 1
fi

# create directory if it does not already exist
if [ ! -d "$DIR" ]
then
    echo "Creating directory $DIR"
    mkdir -p "$DIR"
    echo "DIR='$DIR'" > var.py

    echo "Cloning DevNet Express Sample repository"
    git clone  https://github.com/CiscoDevNet/devnet-express-code-samples.git "$DIR/devnet-express-code-samples"

    echo "Creating virtual environment in $DIR"
    virtualenv -p python3 "$DIR/env"

    echo
    echo "****"
    echo "To activate virtual environment, install libraries and verify your environment."
    echo "Please run the following commands"
    echo "****"
    echo "source '$DIR/env/bin/activate'"
    echo "pip install -r requirements.txt"
    echo "./verify.py <SPARK-TOKEN>"

else
    echo "Directory $DIR already exists, please remove or choose a different name"
    exit 2
fi

