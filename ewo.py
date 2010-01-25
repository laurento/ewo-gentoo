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
# EWO 0.1 Copyright 2006 Frittella Laurento <mrfree@infinito.it>

import re, commands
from portage import pkgsplit

#from_date = 'Thu Aug 31 16:17:17 2006'
from_date = 'Thu Nov 23 18:00:17 2006'

world = []
alreadydone = []
toskip = ['media-tv/democracy', 'sys-libs/db-3.2.9-r10']
todo = []
out = ''

def fill_world_ng():
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
		raise Exception('Oops! No world packages list...')


#def fill_world():
#	global world

#	raw_pkglist = commands.getstatusoutput('equery -q l')
#	if raw_pkglist[0] == 0:
#		pkglist = raw_pkglist[1].split()

#		for pkg in pkglist:
			#world.append(pkgsplit(pkg)[0])
#			world.append(pkg.strip())
#	else:
#		raise Exception('Oops! No installed packages list...')

def fill_alreadydone():
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
		raise Exception('Oops! No already-done packages list...')

fill_world_ng()
fill_alreadydone()
		
for pkg in world:
	if alreadydone.count(pkg) == 0 and toskip.count(pkg) == 0:
		todo.append(pkg)

#print 'World packages       : ' + str(len(world))
#print 'Already done packages: ' + str(len(alreadydone))
#print 'TODO packages        : ' + str(len(todo))

for pkg in todo:
	if toskip.count(pkgsplit(pkg)[0]) == 0:
		out += '=' + pkg + ' '

print out
