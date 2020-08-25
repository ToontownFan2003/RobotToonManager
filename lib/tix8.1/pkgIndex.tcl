# Tcl package index file, version 1.0
# -*-mode: tcl; fill-column: 75; tab-width: 8; coding: iso-latin-1-unix -*-
#
#	$Id: pkgIndex.tcl,v 1.1.2.2 2002/12/15 04:21:54 idiscovery Exp $
#

# The dll can be found in different places depending on how Tix is used
# We look for it in 3 places and stop at the first one we find.
set tail tix8184.dll
# We look in the current directory (usually lib/tix8.1)
set dirs .
# We look in the same directory as the executable 
# (which windows will do for a tix.exe anyway)
lappend dirs [file dirname [info nameofexe]]
# We look in the ../../bin directory (an installed Tcl)
lappend dirs ../../bin
# We look in the ../../DLLs directory (an installed Python)
lappend dirs [file join [file dirname [info nameofexe]] DLLs]
# If not, this pkgIndex.tcl will probably fail.


set pwd [pwd]
foreach elt $dirs {
    if {[file isdir $elt] && \
	    [file isfile [file join $elt $tail]] && \
	    ![catch {cd $elt}]} {
	set tail [file join [pwd] $tail]
	break
    }
}
cd $pwd
package ifneeded Tix 8.1 [list load $tail Tix]
unset dirs pwd elt tail

package ifneeded wm_default 1.0 [list source [file join $dir pref WmDefault.tcl]]
