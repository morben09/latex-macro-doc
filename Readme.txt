% Created in 06/2016 by Robin Jacob

IMPORTANT FOR A GOOD FORMATTING IN THE TEX-FILE/PDF:
% For input-files (.sty):
% 	While reading, all lines with one %-symbol (%) at first are being ignored.
% 	While reading, all lines with two %-symbols (%%) are being interpreted as a title.
% 	While reading, all lines with more than two %-symbols are being interpreted as a new chapter.
% 	Comments after the tag %-% are inserted in the 'comment' column of the last command.
% 	The minimal_example.sty document this comment system.

% Commands with input parameters only works with up to nine parameters. (else compiling error in LaTeX)

% working commands in sty:
%	-\def\cmd
%	-\def\cmd#n
%	-\newcommand{}{}
%	-\newcommand{}[]{}
%	-\renewcommand{}{}
%	-\DeclareMathOperator{}{}

CARE:
- In .sty files, use \ensuremath{} instead of $$ to prevent compiling issues
- If you renew a command with input parameters, make sure to declare the input parameters for the new command as well


HOW TO USE:
- Make sure you have Python and LaTeX installed, if not do so!
- Put the styTOpdf.py in the folder where the file which should be translated is in.
- Start the script by simply clicking at it or start it via your commandline.
- Follow the steps in the commandline.
- Done!

Notice:
- Make sure you have read and write permissions in your working directory.
- The script will create a folder named as your desired filename in your working directory where all the needed files will be put in.
	-> Therefore it is possible to simply store all of your .sty files in one directory and create pdfs as you need them.
- Tab completion is available for quickly choosing the .sty files to include.
