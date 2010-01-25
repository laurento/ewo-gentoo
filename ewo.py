#! /usr/bin/env python
#
#    This program is free software; you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation; either version 2 of the License, or
#    (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.
#
#    You should have received a copy of the GNU General Public License
#    along with this program; if not, write to the Free Software
#    Foundation, Inc., 59 Temple Place, Suite 330, Boston, MA  02111-1307  USA
#
# Emerge (-e) World Optimizer (EWO)
# EWO 0.2 Copyright 2007 Frittella Laurento <mrfree@infinito.it>

import re, commands, os, sys
from portage import pkgsplit
from portage_dep import isvalidatom, dep_getcpv
from time import gmtime, strftime
from subprocess import call, Popen, PIPE

conf_dir = os.path.expanduser('~/.ewo/')
conf_fromdate = conf_dir + '.ewo_from_date'
conf_toskip = conf_dir + 'package.skip'

ewo_version = "0.2"
from_date = ''
world = []
alreadydone = []
toskip = []
todo = []
out = ''

class EwoError(Exception): pass

def read_config_files():
	global toskip, from_date
	#
	# Read ebuilds to skip in the re-compilation
	#
	fd = open(conf_toskip, 'r')
	toskip_lines = fd.readlines()
	fd.close()
	for atom in toskip_lines:
		# Whitespace cleanup
		atom = re.sub('\s+', '', atom)
		if not re.match('^#.*|^$', atom) and isvalidatom(atom):
			toskip.append(dep_getcpv(atom))
	#
	# Read from_date value from the config file
	#
	if os.path.isfile(conf_fromdate):
		fd = open(conf_fromdate, 'r')
		from_date = fd.readline()
		fd.close()
	else:
		raise EwoError("The starting point has not been set!\nPlease specify it using -s option first")

def fill_world_ng():
	print "Checking ALL installed packages..."
	
	global world
	raw_emerge_pattern = re.compile('\[.+\]\s+([^\s]+).*')

	raw_pkglist = commands.getstatusoutput('emerge -ep --quiet --nospinner world')
	if raw_pkglist[0] == 0:
		pkglist = raw_pkglist[1].split('\n')	

		for pkg in pkglist:
			match = raw_emerge_pattern.match(pkg)
			if match:
				world.append(match.group(1))
	else:
		raise EwoError('Oops! No world packages list...')

def fill_alreadydone():
	print "Checking Already-Done (re-compiled) packages..."
	
	global alreadydone, from_date
	raw_genlop_pattern = re.compile('.+>>>\s+([^\s]+).*')

	raw_alreadydone_pkglist = commands.getstatusoutput('genlop -ln --date ' + from_date)
	if raw_alreadydone_pkglist[0] == 0:
		alreadydone_pkglist = raw_alreadydone_pkglist[1].split('\n')

		for pkg in alreadydone_pkglist:
			match = raw_genlop_pattern.match(pkg)
			if match:
				alreadydone.append(match.group(1))
	else:
		raise EwoError('Oops! No already-done packages list...')

#
# Whoami
#
print "EWO - Emerge (-e) World Optimizer (v%s)\n" % ewo_version

#
# Setting up the configuration files and dir too
#
if not os.path.isdir(conf_dir):
	os.makedirs(conf_dir, 0755)
if not os.path.isfile(conf_toskip):
	toskip_file_template = '''# EWO will ignore, in the 'to compile' list, the following packages
# -- ONE atom per line --

# media-tv/democracy
# =sys-libs/db-3.2.9-r10

'''
	fd = open(conf_toskip, 'w')
	fd.writelines(toskip_file_template)
	fd.close()


from optparse import OptionParser

parser = OptionParser(usage="%prog [options]",version=("%prog - " + ewo_version))
parser.add_option("-s", "--setstart", action="store", dest="touch_fromdate",
                  help="set the starting point (possible values are 'NOW' or a genlop-style date like 'Mon Jun 05 11:09:37 2007')")
parser.add_option("-P", "--purgestart", action="store_true", dest="purge_fromdate",
                  help="remove the previously set starting point")
parser.add_option("-v", "--showstart", action="store_true", dest="show_fromdate",
                  help="show the already set starting point")
parser.add_option("-f", "--fetchonly", action="store_true", dest="fetch_only",
                  help="use the --fetchonly option in the emerge command")
parser.add_option("-m", "--mode", action="store", dest="mode", choices=['exec','pretend','emerge-pretend'],
                  help="using mode 'exec' an 'emerge -1 [...]' will start automatically; " +
                       "using 'pretend' ewo simply shows the todo packages list on the stdout " +
                       "and using 'emerge-pretend' (Default) the output of 'emerge -1vp [...] | less' will be shown")
parser.set_defaults(mode="emerge-pretend")

(options, args) = parser.parse_args()

if options.touch_fromdate:
	if options.touch_fromdate == "NOW":
		choosen_date = strftime("%a %b %d %H:%M:%S %Y")
	elif re.match('(Mon|Tue|Wed|Thu|Fri|Sat|Sun) (Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec) \d{2} \d{2}:\d{2}:\d{2} \d{4}', options.touch_fromdate):
		choosen_date = options.touch_fromdate
	else:
		raise EwoError("'%s' isn't a valid genlop-style date!" % options.touch_fromdate)
	
	fd = open(conf_fromdate, 'w')
	fd.write(choosen_date)
	fd.close()
	print "Ok, I'm considering the Global-Thermonuclear 'emerge -e world' started on: \n%s" % choosen_date
	sys.exit(0)
elif options.purge_fromdate:
	os.remove(conf_fromdate)
	print "Starting point date info removed."
	sys.exit(0)
elif options.show_fromdate:
	if os.path.isfile(conf_fromdate):
		fd = open(conf_fromdate, 'r')
		print "I'm considering the Global-Thermonuclear 'emerge -e world' started on: \n%s" % fd.readline()
		fd.close()
		sys.exit(0)
	else:
		print "The starting point has not been set!"
		sys.exit(0)

try:
	read_config_files()
	print "Using '%s' as starting date\n" % from_date
	
	fill_world_ng()
	fill_alreadydone()
	
	for pkg in world:
		if alreadydone.count(pkg) == 0 and toskip.count(pkg) == 0:
			todo.append(pkg)
	
	print "\n'-e world' packages   : %d" % len(world)
	print "Already done packages : %d" % len(alreadydone)
	print "TODO packages         : %d" % len(todo)
	if len(toskip) > 0:
		print "Skipped packages      : %d" % len(toskip)
		for pck in toskip:
			print '   %s' % pck
	
	for pkg in todo:
		if toskip.count(pkgsplit(pkg)[0]) == 0:
			out += '=' + pkg + ' '
	
	if options.mode == "exec":
		print "\nStarting the Global-Thermonuclear 'emerge -1 [...]'...\n"
		cmd = ["emerge", "-1"]
		if options.fetch_only:
			cmd.append("--fetchonly")
		cmd.extend(out.split(" "))
		retcode = call(cmd)
		if retcode > 0:
			print "\n\nOne or more errors occurred, please make your checks\nand restart EWO to -resume- the 'emerge -e world'"
		elif options.fetch_only:
			print "\n\nAll fetched. Hey, what are you waiting for? Start to compile! :D"
		else:
			print "\n\nMumble Mumble... no error occurred, enjoy your fresh compiled gentoo system ;)"
	elif options.mode == "emerge-pretend":
		cmd = ["emerge", "--color=y", "-1vp", "--nospinner"]
		cmd.extend(out.split(" "))
		p1 = Popen(cmd, stdout=PIPE)
		p2 = Popen(["less", "-R"], stdin=p1.stdout)
		p2.wait()
		#p1.wait() # This blocks EWO if the user quit "less" before reach the end of the emerge output
		
		if p1.returncode > 0:
			print "\n\nOne or more errors occurred, please make your checks and restart EWO"
		else:
			print "\n\nIf all seems ok, start EWO with '--mode=exec' to automatically start a convenient emerge"
	else:
		print "\nHere is the todo package list:\n(start EWO with '--mode=exec' to automatically start a convenient emerge)\n"
		print out
	
except EwoError, e:
	print e
except:
	print "\nUnexpected error:", sys.exc_info()[0]
	raise
