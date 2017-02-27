Hello!
In order to run this script, please do not mess with the Resumes-Good
folder as that is used for test data. You are allowed to add as many resumes
in the Resumes-Raw folder and the script will convert them into .txt files to
be put into the Resumes-Txt folder.
This script only accepts .docx and .pdf resumes.
It uses a variety of libraries including:
  PDFMiner
  Kmeans
  docs2txt
  glob
  fuzzywuzzy
  enchant
  numpy
To run this script in the command terminal, you would write:
python parse.py <document>
The document has to be in the same directory as the script. The script has to
be in the same directory as the three folders and buzz.txt.
Thank you!
Traian
