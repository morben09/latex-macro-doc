#!/usr/bin/env python
# -*- coding: utf-8 -*-
# created in 06/2016 by Robin Jacob
# using parts of the latex template from the "VAdF"-internship at the TU Darmstadt during SoSe 2016

import os
import shutil

path = os.path.dirname(os.path.abspath(__file__))

def read():
	path = os.path.dirname(os.path.abspath(__file__))
	d = "predef";
	list = [];
	while d != "end":
		d = input("Insert a source-filename (including ending such as .sty) or type 'end' to end the input:  \n> ")
		if d != 'end':
			if (not os.path.isfile(path+'\\'+ d)) and (d != 'end'):
				print('ERROR: ' + '\''+d+'\'' + ' NOT existant, try again!')
			else:
				list.append(d)
				print(d + ' hinzugefügt!')
	return list
			
def write(list, mf, title, author, subtitle):
	latexfiles = []
	if list:
		#iterates over all selected files
		for file in list:
			fl = open(path+'\\'+file, 'r')
			shutil.copy2(path+'\\'+file, path+'\\'+mf+'\\'+file)
			latex = open(path+'\\'+mf+'\\'+file+'.tex', 'w')
			tabularbegin = False									#ensure that at the end no table is closed without a table opened before (avoiding latex error)
			command = False
			#iterates over all lines in file f1
			for line in fl:
				#print(line)
				append = []
				if line:
					if line.find("\catcode") is not 0:
						if "%%%" in line:
							if command:
								latex.write("\\hline"+ "\n")
								latex.write("\\end{tabular}"+ "\n")
								command = False
							latex.write("\\newpage \n")
							latex.write("\\chapter{"+line.replace('%','').strip()+"}"+"\n")
						elif "%%" in line:
							if command:
								latex.write("\\hline"+ "\n")
								latex.write("\\end{tabular}"+ "\n")
								command = False
							latex.write("\\section{"+line.replace('%','').strip()+"}"+"\n")
						elif "\def" in line:
							if not command:
								latex.write("\\begin{tabular}{||l|r||}"+ "\n")
								latex.write("\hline"+ "\n")
								latex.write("\\textbf{symbol} & \\textbf{shortcut} \\\\\hhline{|=|=|}"+ "\n")
								tabularbegin = True
							command = True
							startfbs = line.find('\\')					#startfirstbackslash
							startsbs = line[startfbs+1:].find('\\')		#startsecondbackslash
							endsbs = line.find('{')
							if line[startsbs+1:endsbs].find('#') == -1:
								cmd = line[startsbs+1:endsbs]
								latex.write(cmd+" & \\begin{lstlisting}"+"\n"+cmd+" \\end{lstlisting}\\\\"+ "\n")
							else:
								hashtag =  line.find('#')
								cmd = line[startsbs+1:hashtag]
								nmbr = line[hashtag+1:endsbs].strip()
								cnt = int(nmbr)
								post = []
								for counter in range(0,cnt):
									post.append("{"+chr(counter+97)+"}")
								pst = ''.join(post)
								latex.write(cmd+pst+" & \\begin{lstlisting}"+"\n"+cmd+pst+" \\end{lstlisting}\\\\"+ "\n")
						elif line[0] == '\\':
							if not command:
								latex.write("\\begin{tabular}{||l|r||}"+ "\n")
								latex.write("\hline"+ "\n")
								latex.write("\\textbf{symbol} & \\textbf{shortcut} \\\\\hhline{|=|=|}"+ "\n")
								tabularbegin = True
							command = True
							startfb = line.find('{')					#startfirstbracket
							endfb = line.find('}')						#endfirstbracket
							startrb = line.find('[')					#startrectangularbracket
							endrb = line.find(']')						#endrectangularbracket
							nmbr = line[startrb+1:endrb].strip()
							cmd = line[startfb+1:endfb]
							if line[endfb+1] =='[':
								post = []
								cnt = int(nmbr)
								for counter in range(0,cnt):
									post.append("{"+chr(counter+97)+"}")
								pst = ''.join(post)
								latex.write("$"+cmd+pst+"$ & \\begin{lstlisting}"+"\n"+cmd+pst+" \\end{lstlisting}\\\\"+ "\n")
							else:
								startsb = endfb + line[endfb:].find('{')	#startsecondbracket
								endsb = line.rfind('}')						#endsecondbracket
								latex.write("$"+cmd+"$ & \\begin{lstlisting}"+"\n"+cmd+" \\end{lstlisting}\\\\"+ "\n")
			if tabularbegin:
				latex.write("\\hline"+ "\n")
				latex.write("\\end{tabular}"+ "\\newpage")
			latexfiles.append(path+'\\'+mf+'\\'+file+'.tex')
			latex.close()		
			fl.close()
			print(file+".tex created")
			
		writemainfile(list, mf, title, author, subtitle)
	else:
		shutil.rmtree(mf)
		print("No data selected, aborting...")
		
	
	
def writemainfile (mfiles, mfilename, title, author, subtitle):
	f = open(path+'\\'+mfilename+'\\'+mfilename+'.tex', 'w')
	f.write("\\documentclass[scrreprt,colorback,accentcolor=tud9b, 11pt]{tudreport}"+"\n")
	f.write("\\usepackage[utf8]{inputenc}"+"\n")
	f.write("\\usepackage[T1]{fontenc}"+"\n")
	f.write("\\usepackage{subfiles}"+"\n")
	f.write("\\usepackage[ngerman]{babel} "+"\n")
	f.write("\\usepackage{framed}"+"\n")
	f.write("\\usepackage{amsmath}"+"\n")
	f.write("\\usepackage{listings}"+"\n")
	f.write("\\usepackage{hhline}"+"\n")
	for pck in mfiles:
		pck2 = pck[0:pck.rfind('.')]
		f.write("\\usepackage{"+pck2+"}"+"\n")
	f.write("\\begin{document}"+"\n")
	f.write("\\title{"+title+"}"+"\n")
	f.write("\\subtitle{Shortcuts created by: "+author+"\\\\"+subtitle+"}"+"\n")
	f.write("\\author{"+author+"}"+"\n")
	f.write("\\maketitle"+"\n")
	f.write("\\tableofcontents"+"\n")
	f.write("\\newpage"+"\n")
	for fe in mfiles:
		f.write("\\subfile{"+fe+".tex}"+"\n")
	f.write("\\end{document}"+"\n")
	print("Main .tex File created ("+mfilename+".tex)!")
	
	
def executeThis():
	mainfile = input("Please input the desired name of the final LaTeX file:  \n> ")
	existant = True
	while existant:
		if os.path.isdir(path+'\\'+mainfile):
			mainfile = input("File/path already existent. Please input another name of the final LaTeX file:  \n> ")
		else:
			existant = False
			if not os.path.exists(path+mainfile):
				os.makedirs(path+'\\'+mainfile)
				open(path+'\\'+mainfile+'\\'+mainfile+'.tex', 'w')
			
	title = input("Please input the desired title of your final LaTeX file (optional):  \n> ")
	author = input("Please input the name/names of the author(s), divided by commas (optional):  \n> ")
	subtitle = input("Please input a subtitle for your final LaTeX file(optional):  \n> ")
	lst = read()
	print("All files added!")
	write(lst, mainfile, title, author, subtitle)
	if lst:
		return mainfile
	else:
		return []

go = True
print("==================================================================================================================")
print("||Created in June 2016 by Robin Jacob                                                                           ||")
print("||                                                                                                              ||")
print("||This script converts .sty files into pdf files with the translations in between the commands and the symbols. ||")
print("==================================================================================================================")
while go:
		out = executeThis()
		create = input("Do you want to create a PDF file? Type 'y'/'Y' for yes or anything else for no! \n> ")
		if create == 'y' or create == 'Y':
			if out:
				os.chdir(out)
				os.system("pdflatex "+out+".tex")
				os.system("pdflatex "+out+".tex")
				print("\n"+out+".pdf created! \n")
				os.chdir(path)
			else:
				print("No PDF created, no files were selected!")
		cont = input("Do you want to create another file? Type 'y'/'Y' for yes or anything else for no! \n> ")
		print("\n\n")
		if not ((cont == "y") or (cont == "Y")):
			go = False
			input("End the program with any key...")
			