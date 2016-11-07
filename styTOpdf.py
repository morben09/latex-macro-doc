#!/usr/bin/env python
# -*- coding: utf-8 -*-
# created in 06/2016 by Robin Jacob
# edited by Robin Jacob, Thorben Casper and Yun Ouedraogo
# using parts of the latex template from the "VAdF"-lab at the TU Darmstadt during SoSe 2016

import os
import shutil
import argparse

path = os.path.dirname(os.path.abspath(__file__))
print(path)

def format_section(commands, comments):
	if ''.join(comments):
		table_opening = r'\begin{longtable}{||l|r|l||}'+'\n'+r'\hline'+'\n'+r'\textbf{symbol} & \textbf{shortcut} & \textbf{comment} \\'+'\n'+r'\hhline{|=|=|=|}'+'\n'
		table_closing = r'\hline'+'\n'+r'\end{longtable}'+'\n'
		command_format = r'${0}$ & \begin{{lstlisting}}'+'\n'+r'{0}'+r' \end{{lstlisting}} & {1}'+'\n'+r'\\' + '\n'
		contents = ''.join([command_format.format(command, comment) for command, comment in zip(commands, comments)])
	else:
		table_opening = r'\begin{longtable}{||l|r||}'+'\n'+r'\hline'+'\n'+r'\textbf{symbol} & \textbf{shortcut}\\'+'\n'+r'\hhline{|=|=|}'+'\n'
		table_closing = r'\hline'+'\n'+r'\end{longtable}'+'\n'
		command_format = r'${0}$ & \begin{{lstlisting}}'+'\n'+r'{0}'+r' \end{{lstlisting}}\\' + '\n'
		contents = ''.join([command_format.format(command) for command in commands])

	return ''.join([table_opening, contents, table_closing])


def write(list, df, mf, title, author, subtitle):
	latexfiles = []
	if list:
		#iterates over all selected files
		for myfilepath in list:

			with open(myfilepath, 'r') as fl:
				sty_contents = fl.read().split('\n')
			myfile = os.path.basename(myfilepath)
			shutil.copy2(myfilepath, df+myfile)
			tex_file = open(df+myfile+'.tex', 'w')
			tabularbegin = False									#ensure that at the end no table is closed without a table opened before (avoiding latex error)
			command = False
			comment_flag = r'%-%'
			chapter_flag = r'%%%'
			section_flag = r'%%'

			current_command, current_comment = '', ''
			current_commands, current_comments = [], []

			# iterates over all lines in file f1
			for line in sty_contents:

				# Empty lines and catcode statements are not macros
				if not line or line.find(r'\catcode') is 0:
					continue

				if chapter_flag in line:
					if command:
						current_commands.append(current_command)
						current_comments.append(current_comment)
						tex_file.write(format_section(current_commands, current_comments))
						current_commands, current_comments = [], []
						current_command, current_comment = '', ''
						command = False
					tex_file.write(r'\newpage'+'\n')
					tex_file.write(r'\chapter{'+line.replace('%','').strip()+'}'+'\n')
				elif section_flag in line:
					if command:
						current_commands.append(current_command)
						current_comments.append(current_comment)
						tex_file.write(format_section(current_commands, current_comments))
						current_commands, current_comments = [], []
						current_command, current_comment = '', ''
						command = False
					tex_file.write(r'\section{'+line.replace('%','').strip()+'}'+'\n')
				elif r'\def' in line:
					if command:
						current_commands.append(current_command)
						current_comments.append(current_comment)
						current_command, current_comment = '', ''
					else:
						tabularbegin = True
					command = True
					startfbs = line.find('\\')					#startfirstbackslash
					startsbs = line[startfbs+1:].find('\\')		#startsecondbackslash
					endsbs = line.find('{')
					if line[startsbs+1:endsbs].find('#') == -1:
						current_command = line[startsbs+1:endsbs]
						#tex_file.write(cmd+r' & \begin{lstlisting}'+'\n'+cmd+r' \end{lstlisting} & ')
					else:
						hash_index =  line.find('#')
						cmd = line[startsbs+1:hash_index]
						nmbr = line[hash_index+1:endsbs].strip()
						cnt = int(nmbr)
						post = []
						for counter in range(0,cnt):
							post.append('{'+chr(counter+97)+'}')
						pst = ''.join(post)
						current_command = cmd+pst
						#tex_file.write(cmd+pst+r' & \begin{lstlisting}'+'\n'+cmd+pst+r' \end{lstlisting} & ')
				elif line[0] == '\\':
					if command:
						current_commands.append(current_command)
						current_comments.append(current_comment)
						current_command, current_comment = '', ''
					else:
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
						current_command = cmd+pst
						#tex_file.write('$'+cmd+pst+r'$ & \begin{lstlisting}'+'\n'+cmd+pst+r' \end{lstlisting} & ')
					else:
						current_command = cmd
						#tex_file.write('$'+cmd+r'$ & \begin{lstlisting}'+'\n'+cmd+r' \end{lstlisting} & ')

				if comment_flag in line:
					comment_begin_index = line.find(comment_flag)+len(comment_flag)
					current_comment = line[comment_begin_index:].strip()

			if tabularbegin:
				current_commands.append(current_command)
				current_comments.append(current_comment)
				tex_file.write(format_section(current_commands, current_comments))
				current_commands, current_comments = [], []
			latexfiles.append(df+myfile+'.tex')
			tex_file.close()
			print(myfile+".tex created")

		writefilename(list, df, mf, title, author, subtitle)
	else:
		shutil.rmtree(mf)
		print("No data selected, aborting...")



def writefilename (mfiles, mdirname, mfilename, title, author, subtitle):
	f = open(mdirname+mfilename+'.tex', 'w')
	f.write("\\documentclass[scrreprt,colorback,accentcolor=tud9b, 11pt]{tudreport}"+"\n")
	f.write("\\usepackage[utf8]{inputenc}"+"\n")
	f.write("\\usepackage[T1]{fontenc}"+"\n")
	f.write("\\usepackage{subfiles}"+"\n")
	f.write("\\usepackage[ngerman]{babel} "+"\n")
	f.write("\\usepackage{framed}"+"\n")
	f.write("\\usepackage{amsmath}"+"\n")
	f.write("\\usepackage{longtable}"+"\n")
	f.write("\\usepackage{listings}"+"\n")
	f.write("\\usepackage{hhline}"+"\n")
	for pck in mfiles:
		pck2 = os.path.splitext(os.path.basename(pck))[0]
		f.write("\\usepackage{"+pck2+"}"+"\n")
	f.write("\\begin{document}"+"\n")
	if title and (not title.isspace()):
		f.write("\\title{"+title+"}"+"\n")
	else:
		f.write("\\title{Macro documentation}"+"\n")
	if author and (not author.isspace()):
		f.write("\\subtitle{Shortcuts created by: "+author+"\\\\"+subtitle+"}"+"\n")
		f.write("\\author{"+author+"}"+"\n")
	else:
		if subtitle and (not subtitle.isspace()):
			f.write("\\subtitle{"+subtitle+"}"+"\n")
	f.write("\\maketitle"+"\n")
	f.write("\\tableofcontents"+"\n")
	f.write("\\newpage"+"\n")
	for fe in mfiles:
		fe2 = os.path.basename(fe)
		f.write("\\subfile{"+fe2+".tex}"+"\n")
	f.write("\\end{document}"+"\n")
	print("Main .tex File created ("+mfilename+".tex)!")


def executeThis():
	parser = argparse.ArgumentParser()
	parser.add_argument("sty_files", help=".sty-files for which a .pdf-file shall be created",type=argparse.FileType('r'), nargs='+')
	parser.add_argument("-c","--createPDF", help="use if you want to create the .pdf directly",action="store_true")
	parser.add_argument("-o","--overwrite", help="overwrites any existent files/folders if used (USE WITH CARE!)", action="store_true")
	parser.add_argument("-f","--filename", help="file and pathname of PDF", type=str)
	parser_args = parser.parse_args()
	createPDF = parser_args.createPDF
	
	if not parser_args.filename:
		basename = os.path.basename(parser_args.sty_files[0].name)
		filename = os.path.splitext(basename)[0] # splits filename into base and extension and chooses base
	else:
		filename = parser_args.filename
	print filename
	if os.path.isdir(path+os.sep+filename):
		print(path+os.sep+filename)
		if not parser_args.overwrite:
			try: overwrite = raw_input("File/path already existent. Do you want to overwrite (CAUTION: This will delete the whole folder including its contents)? (y/n):  \n> ")
			except NameError: overwrite = input("File/path already existent. Do you want to overwrite (CAUTION: This will delete the whole folder including its contents)? (y/n):	\n> ")
		if parser_args.overwrite or overwrite:
			shutil.rmtree(filename)
		else:
			return
	dirname = path+os.sep+filename+os.sep
	os.makedirs(dirname)
	open(dirname+filename+'.tex', 'w')

	title = ''
	author = ''
	subtitle = ''

	# this loop can surely be done better
	styfiles = []
	for f in parser_args.sty_files:
		styfiles.append(os.path.abspath(f.name)) 

	print("creates .sty file")
	write(styfiles, dirname, filename, title, author, subtitle)
	if createPDF:
		print("starts to create .pdf file")
		oldpath = path
		os.chdir(dirname)
		err_code = os.system("pdflatex -interaction nonstopmode "+filename+".tex")
		err_code |=os.system("pdflatex -interaction nonstopmode "+filename+".tex")
		if (err_code==0):
			print("\n"+filename+".pdf successfully created! \n")
		else:
			print("\nWARNING: The compilation of "+filename+".tex returned a non zero exit code.\n		   Please check the output.\n")
		os.chdir(oldpath)
	return


print("==================================================================================================================")
print("||Created in June 2016 by Robin Jacob                                                                           ||")
print("||                                                                                                              ||")
print("||This script converts .sty files into pdf files with the translations in between the commands and the symbols. ||")
print("==================================================================================================================")
executeThis()
