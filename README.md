# DNE-tools
Setup and verification scripts for DNE library.

First run the `00-create-environment.sh` script (OSX/Linux users) or `00-create-environment.bat` script (Windows users) with a target directory where you would like the devenet express files located. 

This will setup a directory, create a virtual python environment and download the respository from git.

You will then have a three commands you need to run after this.
For OSX/Linux users:

```
source '/tmp/adam-dne/env/bin/activate'
pip install -r requirements.txt
./verify.py <SPARK-TOKEN>
```

For Windows users:

```
source '\tmp\adam-dne\env\Scripts\activate'
pip install -r requirements.txt
verify.py <SPARK-TOKEN>
```

The first command will activate the virtual environment.  
This has a local copy of the python libraries so that you can install new module without impacting other python applications

The second command will install the required modules for devnet express in the local virtual environment.

You then run the verify.py command to check everything has been setup and post a message into the spark room.
