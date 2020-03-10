#!/usr/bin/env python
# -*- coding: utf-8 -*-
# created in 2016/06 by Robin Jacob
# edited by Robin Jacob, Thorben Casper and Yun Ouédraogo

import os
import shutil
import argparse

path = os.path.dirname(os.path.abspath(__file__))

def writeSectionTable(commands, comments):
	# depending on whether there are comments, a table with either 2 or 3 columns is created
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


def writeSubTexFiles(styfiles, dirname, texFileBase, addPkg, addPkgOpt):
	print("creating .sty file")
	latexfiles = []
	# check whether list of .sty-files is empty. If it is, remove folder and exit
	if styfiles:
		# iterates over all selected files
		for currentfile in styfiles:
			# loads all lines in current .sty-file into an array
			with open(currentfile, 'r') as f:
				sty_contents = f.read().split('\n')
			# copy current .sty-file to new subdirectory
			currentStyFile = os.path.basename(currentfile)
			shutil.copy2(currentfile, dirname)

			# some settings and parameters
			tabularbegin = False	# ensure that no table is closed without a table opened before
			command = False
			doc_flag = r'%#'
			docOnly_flag = r'%$!'
			comment_flag = r'%-%'
			chapter_flag = r'%%%'
			section_flag = r'%%'

			current_command, current_comment = '', ''
			current_commands, current_comments = [], []

			# opens .tex-subfile
			tex_file = open(dirname+currentStyFile+'.tex', 'w')
			# iterates over all lines in .sty-file
			for line in sty_contents:
				line = line.strip()

				# empty lines and catcode statements are not macros
				if not line or line.find(r'\catcode') is 0:
					continue

				# line starts with documentation flag
				if line[0:2] == doc_flag:
					# don't forget to escape characters that can lead to problems
					tex_file.write(line[2:].strip().replace(r'%','\%').replace('#','\#')+'\n')
				# line contains plain documentation, rest of file will be ignored
				elif line[0:3] == docOnly_flag:
					# if a command was found before, flush out all the commands for the previous section
					if command:
						current_commands.append(current_command)
						current_comments.append(current_comment)
						tex_file.write(writeSectionTable(current_commands, current_comments))
						current_commands, current_comments = [], []
						current_command, current_comment = '', ''
						command = False
					tex_file.write(line[3:].strip())
					tabularbegin = False
					break
				# line gives the title of a new chapter
				elif line[0:3] == chapter_flag:
					# if a command was found before, flush out all the commands for the previous chapter
					if command:
						current_commands.append(current_command)
						current_comments.append(current_comment)
						tex_file.write(writeSectionTable(current_commands, current_comments))
						current_commands, current_comments = [], []
						current_command, current_comment = '', ''
						command = False
					tex_file.write(r'\newpage'+'\n')
					tex_file.write(r'\chapter{'+line[3:].replace(r'%','\%').strip()+'}'+'\n')
				# line gives the title of a new section
				elif line[0:2] == section_flag:
					# if a command was found before, flush out all the commands for the previous section
					if command:
						current_commands.append(current_command)
						current_comments.append(current_comment)
						tex_file.write(writeSectionTable(current_commands, current_comments))
						current_commands, current_comments = [], []
						current_command, current_comment = '', ''
						command = False
					tex_file.write(r'\section{'+line[2:].replace(r'%','\%').strip()+'}'+'\n')
				# if \def is found in a line, the corresponding command is added to command list
				elif line[0:4] == r'\def':
					if command:
						current_commands.append(current_command)
						current_comments.append(current_comment)
						current_command, current_comment = '', ''
					else:
						tabularbegin = True
					command = True
					# extract command from current line
					startfbs = line.find('\\')					#startfirstbackslash
					startsbs = line[startfbs+1:].find('\\')		#startsecondbackslash
					endsbs = line.find('{')
					if line[startsbs+1:endsbs].find('#') == -1:
						current_command = line[startsbs+1:endsbs]
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
				# line starts \newcommand
				elif line[0:11] == '\\newcommand':
					if command:
						current_commands.append(current_command)
						current_comments.append(current_comment)
						current_command, current_comment = '', ''
					else:
						tabularbegin = True
					command = True
					# extract command from current line
					startfb = line.find('{')					#startfirstbrace
					endfb = line.find('}')						#endfirstbrace
					startrb = line.find('[')					#startbracket
					endrb = line.find(']')						#endbracket
					nmbr = line[startrb+1:endrb].strip()
					cmd = line[startfb+1:endfb]
					if line[endfb+1] =='[':
						post = []
						cnt = int(nmbr)
						for counter in range(0,cnt):
							post.append("{"+chr(counter+97)+"}")
						pst = ''.join(post)
						current_command = cmd+pst
					else:
						current_command = cmd
				# line starts with \RequirePackage
				elif line[0:15] == '\\RequirePackage':
					startfb = line.find('{')                    #startfirstbrace
					endfb = line.find('}')                      #endfirstbrace
					startOpt = line.find('[')                   #startfirstbracket
					endOpt = line.find(']')                     #endfirstbracket
					pkg = line[startfb+1:endfb]
					addPkg.append(pkg+'.sty');
					if startOpt != -1:
						addPkgOpt.append(line[startOpt+1:endOpt]);
					else:
						addPkgOpt.append('');

				# if a comment is detected in a line
				if comment_flag in line:
					comment_begin_index = line.find(comment_flag)+len(comment_flag)
					current_comment = line[comment_begin_index:].strip()

			# flush out commands to .tex-file if not have been written out yet
			if tabularbegin:
				current_commands.append(current_command)
				current_comments.append(current_comment)
				tex_file.write(writeSectionTable(current_commands, current_comments))
				current_commands, current_comments = [], []
			latexfiles.append(dirname+currentStyFile+'.tex')
			tex_file.close()
			print(currentStyFile+".tex created")

		# copy additional packages
		for filepath in addPkg:
			currentStyFile = os.path.basename(filepath)
			if filepath[0:4] == 'temf':
				shutil.copy2(filepath, dirname+currentStyFile)
		return addPkg

	else:
		shutil.rmtree(texFileBase)
		print("No data selected, aborting...")


def writeMainTexFile (mfiles, mdirname, mfilename, title, author, subtitle, addPkg, addPkgOpt):
	f = open(mdirname+mfilename+'.tex', 'w')
	f.write("\\documentclass[scrreprt,colorback,accentcolor=tud9b, 11pt]{tudreport}"+"\n")
	f.write("\\usepackage[utf8]{inputenc}"+"\n")
	f.write("\\usepackage[T1]{fontenc}"+"\n")
	f.write("\\usepackage{subfiles}"+"\n")
	f.write("\\usepackage[ngerman]{babel} "+"\n")
	f.write("\\usepackage{framed}"+"\n")
	f.write("\\usepackage{amsmath}"+"\n")
	f.write("\\usepackage{bm}"+"\n")
	f.write("\\usepackage{bbm}"+"\n")
	f.write("\\usepackage{longtable}"+"\n")
	f.write("\\usepackage{listings}"+"\n")
	f.write("\\usepackage{hhline}"+"\n")
	f.write("\\usepackage{hyperref}"+"\n")
  # add additional packages given by --package option to preamble
	for i in range(len(addPkg)):
		pck2 = os.path.splitext(os.path.basename(addPkg[i]))[0]
		if addPkgOpt[i]:
			f.write("\\usepackage["+addPkgOpt[i]+"]{"+pck2+"}"+"\n")
		else:
			f.write("\\usepackage{"+pck2+"}"+"\n")
  # add import of packages to preamble
	for pck in mfiles:
		pck2 = os.path.splitext(os.path.basename(pck))[0]
		f.write("\\usepackage{"+pck2+"}"+"\n")
	# write body of latex document
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
    # include packages as subfiles
	for fe in mfiles:
		fe2 = os.path.basename(fe)
		f.write("\\subfile{"+fe2+".tex}"+"\n")
	f.write("\\end{document}"+"\n")
	f.close()
	print("main .tex File created ("+mfilename+".tex)!")


if __name__ == "__main__":
	# parse input arguments and create help text
	parser = argparse.ArgumentParser(
		description='''This script converts .sty files into pdf files with the translations in between the commands and the symbols.''',
		epilog='''Created in June 2016 by Robin Jacob and edited by Thorben Casper and Yun Ouédraogo''')
	parser.add_argument("sty_files", help=".sty-files for which a .pdf-file shall be created",type=argparse.FileType('r'), nargs='+')
	parser.add_argument("-c","--createPDF", help="use if you want to create the .pdf directly",action="store_true")
	parser.add_argument("-o","--overwrite", help="overwrites any existent files/folders if used (USE WITH CARE!)", action="store_true")
	parser.add_argument("-f","--filename", help="filename to final .pdf (including path without extension)", type=str)
	parser.add_argument("-p","--package", help="use if an additional package shall be loaded when generating the doc. However, this package will not be part of the doc.", type=argparse.FileType('r'), nargs='+')
	parser_args = parser.parse_args()
	createPDF = parser_args.createPDF
	
	# check whether name of output .pdf-file is given. If not, use texFile of .sty file as texFile of .pdf file
	if not parser_args.filename:
		texFile = os.path.basename(parser_args.sty_files[0].name)
		texFileBase = os.path.splitext(texFile)[0]
		texDir = texFileBase
	else:
		texDir = os.path.dirname(parser_args.filename)
		texFileBase = os.path.basename(parser_args.filename)
		texFile = texFileBase + '.sty'
	print(texFile)
	print(texFileBase)
	
	# check if absolute path is used
	if texDir[0]=="/":
		dirname = texDir + os.sep
	else:
		dirname = "." + os.sep + texDir + os.sep
	print(dirname)

	# check whether directory already exists and give a warning if it does. Otherwise, create directory
	if os.path.isdir(dirname):
		if not parser_args.overwrite:
			try: overwrite = raw_input("File/path already existent. Do you want to overwrite (CAUTION: This will delete the whole folder including its contents)? (y/n):  \n> ")
			except NameError: overwrite = input("File/path already existent. Do you want to overwrite (CAUTION: This will delete the whole folder including its contents)? (y/n):	\n> ")
		if parser_args.overwrite or overwrite:
			shutil.rmtree(dirname)
		else:
			quit()		
	os.makedirs(dirname)

	
	# loads additional packages if required for generating the doc using pdflatex
	addPkgFiles = []
	addPkgOptions = []
	if parser_args.package:
		for f in parser_args.package:
			addPkgFiles.append(os.path.abspath(f.name))
			addPkgOptions.append('')

	# creates an array that contains all sty-files given as script input
	styfiles = []
	for f in parser_args.sty_files:
		styfiles.append(os.path.abspath(f.name)) 

	# creates .tex-files from .sty-input
	title = ''
	author = ''
	subtitle = ''
	addPkgFiles = writeSubTexFiles(styfiles, dirname, texFileBase, addPkgFiles, addPkgOptions)
	writeMainTexFile(styfiles, dirname, texFileBase, title, author, subtitle, addPkgFiles, addPkgOptions)

	# compiles using pdflatex if createPDF flag is set
	if createPDF:
		print("creating .pdf file")
		oldpath = path
		os.chdir(dirname)
		err_code = os.system("pdflatex -interaction nonstopmode "+texFileBase+".tex")
		err_code |=os.system("pdflatex -interaction nonstopmode "+texFileBase+".tex")
		if (err_code==0):
			print("\n"+texFileBase+".pdf successfully created! \n")
		else:
			print("\nWARNING: The compilation of "+texFileBase+".tex returned a non zero exit code.\n		   Please check the output.\n")
		os.chdir(oldpath)
