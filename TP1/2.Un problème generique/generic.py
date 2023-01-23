#!/usr/bin/env python3
import sys
import os
import getopt

def read_file(file):
	with open(file, "r") as f:
		line = f.readline()
		m, n = [eval(i) for i in line.split(" ")]
		line = f.readline()
		ressources = line.split("\n")[0].split(" ")
		conditions = []
		vars = []
		for _ in range(n):
			line = f.readline()
			var = line.split("\n")[0].split(" ")[:1]
			condition = line.split("\n")[0].split(" ")[1:]
			conditions.append(condition)
			vars.append(var)
		flat_var = [item for var in vars for item in var]
	return ressources, conditions,flat_var

def integralite(vars):
	strings = "int"
	delimitor = ""
	for n in vars:
		strings += f" {delimitor}{n}"
		delimitor = ","
	strings += ";\n"
	return strings

def write_file(file, output):
	ressources, conditions, vars = read_file(file)
	with open(output, "w") as fw:
		string = "max: "
		delimitor = ""
		for index in range(len(conditions)):
			string += f"{delimitor}{conditions[index][-1]} {vars[index]}"
			delimitor = " + "
		string += ";\n"
		fw.write(string)

		for index, ressource in enumerate(ressources):
			string = ""
			delimitor = ""
			for index2, condition in enumerate(conditions):
				string += f"{delimitor}{condition[index]} {vars[index2]}"
				delimitor = " + "

			string += f" <= {ressource};\n"
			fw.write(string)

def write_file_integralite(file, output):
	write_file(file, output)
	ressources, conditions, vars = read_file(file)
	with open(output,"a") as fw:
		fw.write(integralite(vars))

def main(args):
	optlist, args = getopt.getopt(args[1:], "i", ["int"])
	integral_opt = False
	help_opt = False
	for opt in optlist:
		if "--int" in opt or "-i" in opt:
			integral_opt = True
		#elif("--help" in optlist or "-h" in optlist):
			
	if integral_opt:
		write_file_integralite(args[0], args[1])
		os.system("lp_solve " + args[1])
	else:
		write_file(args[0], args[1])
		os.system("lp_solve " + args[1])

main(sys.argv)