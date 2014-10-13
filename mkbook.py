#!/usr/bin/python3
import glob
import sys, subprocess, os
begin = r"""
\documentclass[letterpaper,12pt]{article}

\usepackage{fancyhdr}
\usepackage{array}
\usepackage[margin=0.5in]{geometry}

\def\arraystretch{2}

\begin{document}

\newcounter{rowcount}

"""

print(
"""
Run with no arguments to make a full recipe book.
Run with "toc" as an argument to add a table of contents.
Run with a list of .tex files to use just those recipes.
See the included recipes for a formatting example to add more recipes.
Format:
  The first line should be the recipe name.
  Then, list steps as follows:
    List the instructions for a step, then an '&' to begin listing ingredients.
    When finished with a step, use a '^', with each separating character on its own line.
Recipe files should end in .rec
""")

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
        if '^' in line or '&' in line:
            mid_step = False
        else:
            if mid_step:
                body += '\\newline\n'
            mid_step = True

        if '^' in line:
            line = line.replace('^', r'\\\hline')
        body += line + '\n'


    foot = "\\end{tabular}\n\n"
    return head + body + foot



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
