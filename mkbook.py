#!/usr/bin/env python3
import glob
import sys, subprocess, os
import argparse

files = sorted(glob.glob("recipes/*"))
names = [f.split("/")[-1] for f in files]

parser = argparse.ArgumentParser(description="Create a nicely formatted recipe book.")
parser.add_argument("--toc", action='store_true', help="Include table of contents")
parser.add_argument("--recipes", metavar='recipes', type=str, help="List of recipe file names", choices=names)

args = parser.parse_args()

begin = r"""
\documentclass[letterpaper,12pt]{article}

\usepackage{fancyhdr}
\usepackage{array}
\usepackage[margin=0.5in]{geometry}

\def\arraystretch{2}

\begin{document}

\newcounter{rowcount}

"""

# takes recipe files and turns them into latex
def translate(filename):
    f = open(filename, 'r')
    recipe = [l.strip() for l in f.readlines() if l.strip()]
    name = recipe[0]
    head = '\\section{%s}\n'  %name + \
    '\\setcounter{rowcount}{0}\n' + \
    r'\begin{tabular}{@{\stepcounter{rowcount}\therowcount)\hspace*{\tabcolsep}}p{.64\textwidth}p{.3\textwidth}}' + '\n'

    body = ""
    mid_step = False
    for line in recipe[1:]:
        if '&' in line:
            mid_step = False
        else:
            if mid_step:
                body += '\\newline\n'
            mid_step = True

        if '&&&' in line:
            line = line.replace('&&&', r'\\\hline')
        body += line + '\n'


    foot = "\\end{tabular}\n\n"
    return head + body + foot



recipes = names if args.recipes is None else args.recipes

files = ["recipes/"+r for r in recipes]

if args.toc:
    begin += "\\tableofcontents\n"

# toremove = ['recipe-book.tex', 'toc']
# for remove in toremove:
#     if remove in files:
#         files.remove(remove)

end = "\\end{document}"

middle = ""

for f in files:
    if os.path.isfile(f):
        middle += translate(f)
    else:
      print('Error: %s does not exist.' %f)
      exit(17)

f = open('recipe-book.tex', 'w')
f.write(begin + middle + end)
f.flush()

subprocess.call(['pdflatex', 'recipe-book'])
subprocess.call(['pdflatex', 'recipe-book'])
subprocess.call(['pdflatex', 'recipe-book'])

for f in glob.glob("recipe-book.*"):
    if not "recipe-book.pdf" in f:
        os.remove(f)
