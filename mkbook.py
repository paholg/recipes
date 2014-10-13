#!/usr/bin/python3
import glob
import sys, subprocess, os
begin = r"""
\documentclass[letterpaper,12pt]{article}

\usepackage{fancyhdr}
\usepackage{array}
\usepackage[margin=0.5in]{geometry}

\renewcommand{\l}{\newline}
\def\arraystretch{2}

\begin{document}

\title{Paho's Collection of Recipes}
\date{\today}

\author{Paho Lurie-Gregg}

\newcounter{rowcount}

"""

print(
"""
Run with no arguments to make a full recipe book.
Run with "toc" as an argument to add a table of contents.
Run with a list of .tex files to use just those recipes.
See the included recipes for a formatting example to add more recipes.
""")

if len(sys.argv) == 1 or (len(sys.argv) == 2 and 'toc' in sys.argv):
    files = sorted(glob.glob("*.tex"))

else:
    files = sys.argv[1:]

if len(sys.argv) > 1 and 'toc' in sys.argv:
    begin += "\\tableofcontents\n"

toremove = ['recipe-book.tex', 'toc']
for remove in toremove:
    if remove in files:
        files.remove(remove)

end = "\\end{document}"

middle = ""

for f in files:
    if os.path.isfile(f):
        middle += '\\input{%s}\n' %f
    else:
      print('Error: %s does not exist.' %f)
      exit(17)

f = open('recipe-book.tex', 'w')
f.write(begin + middle + end)
f.flush()

subprocess.call(['pdflatex', 'recipe-book'])
subprocess.call(['pdflatex', 'recipe-book'])
subprocess.call(['pdflatex', 'recipe-book'])
