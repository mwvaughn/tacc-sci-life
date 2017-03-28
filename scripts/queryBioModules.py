#!/usr/bin/env python

import subprocess as sp
import argparse

parser = argparse.ArgumentParser(description='Tabulate all modules with the "biology" keyword.')
parser.add_argument('-S', metavar='LIST', type=str, help='Systems to query [%(default)s]', default='stampede,ls5,wrangler,login-knl1.stampede,hikari')
parser.add_argument('-O', metavar='TYPE', type=str, help='Output format ([csv], tab, pretty)', default='csv')
args = parser.parse_args()

allModules = set([])
sysModules = {}
systems = args.S.split(',')

for system in systems:
	CMD = 'ssh -t %s.tacc.utexas.edu "module key biology 2>&1 | cat" 2>/dev/null | grep ":" | grep -o -P "[^/\s,]+/[^\s/,]+"'%(system)
	sysModules[system] = set(sp.check_output(CMD, shell=True).rstrip('\n').split('\n'))
	allModules |= sysModules[system]

if args.O == 'csv':
	print "Module,"+','.join(systems)
	for module in allModules:
		outStr = module
		for system in systems:
			if module in sysModules[system]:
				outStr += ',X'
			else:
				outStr += ','
		print outStr
elif args.O == 'tab':
	print "Module\t"+'\t'.join(systems)
	for module in allModules:
		outStr = module
		for system in systems:
			if module in sysModules[system]:
				outStr += '\tX'
			else:
				outStr += '\t'
		print outStr
elif args.O == 'pretty':
	maxLen = max(map(len, allModules))
	header = "%"+str(maxLen)+'s'
	header = header%('Module')
	for system in systems:
		sysLen = str(len(system)+1)
		header += ("%"+sysLen+"s")%(system,)
	print header
	for module in allModules:
		outStr = ("%"+str(maxLen)+"s")%(module,)
		for system in systems:
			sysLen = str(len(system)+1)
			if module in sysModules[system]:
				outStr += ('%'+sysLen+'s')%('X',)
			else:
				outStr += ('%'+sysLen+'s')%(' ',)
		print outStr
