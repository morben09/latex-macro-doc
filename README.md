LaTeX Macro Documentation Tool
===
Created in 06/2016 by Robin Jacob and edited by Thorben Casper and Yun Ouédraogo

## Installation
- Make sure you have Python and LaTeX installed, if not do so!
- Put the styTOpdf.py in the folder where the file which should be translated is in.

## Usage

### Formatting of .sty-file to generate a well formated .pdf-file
- While reading, all lines with one %-symbol (%) at first are being ignored.
- While reading, all lines with two %-symbols (%%) are being interpreted as a title.
- While reading, all lines with more than two %-symbols are being interpreted as a new chapter.
- Comments after the tag %-% are inserted in the 'comment' column of the last command.
- Plain documentation can be used by starting a line with %$!. The rest of that line will be directly printed to the PDF. The rest of the .sty-file after this line will be ignored. This is useful if sty2pdf does not support some parts of the .sty-file. In this case, these parts can be placed at the end of the .sty-file and the plain documentation may describe it.
- The minimal_example.sty document this comment system.

### Examples of supported LaTeX-commands
- \def\cmd
- \def\cmd#n
- \newcommand{}{}
- \newcommand{}[]{}
- \renewcommand{}{}
- \DeclareMathOperator{}{}

### Note
- Commands with input parameters only works with up to nine parameters. (else compiling error in LaTeX)
- In .sty files, use \ensuremath{} instead of $$ to prevent compiling issues.
- If you renew a command with input parameters, make sure to declare the input parameters for the new command as well.
- Make sure you have read and write permissions in your working directory.
- The script will create a folder named as your desired filename in your working directory where all the needed files will be put in. Therefore, it is possible to simply store all of your .sty files in one directory and create pdfs as you need them.
