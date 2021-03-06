# Orca
#
# Copyright (C) 2014 Igalia, S.L.
#
# Author: Joanmarie Diggs <jdiggs@igalia.com>
#
# This library is free software; you can redistribute it and/or
# modify it under the terms of the GNU Lesser General Public
# License as published by the Free Software Foundation; either
# version 2.1 of the License, or (at your option) any later version.
#
# This library is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
# Lesser General Public License for more details.
#
# You should have received a copy of the GNU Lesser General Public
# License along with this library; if not, write to the
# Free Software Foundation, Inc., Franklin Street, Fifth Floor,
# Boston MA  02110-1301 USA.

__id__        = "$Id$"
__version__   = "$Revision$"
__date__      = "$Date$"
__copyright__ = "Copyright (c) 2014 Igalia, S.L."
__license__   = "LGPL"

import pyatspi

import orca.debug as debug
import orca.script_utilities as script_utilities


class Utilities(script_utilities.Utilities):

    def __init__(self, script):
        script_utilities.Utilities.__init__(self, script)

    def selectedChildren(self, obj):
        try:
            selection = obj.querySelection()
        except:
            # This is a workaround for bgo#738705.
            if obj.getRole() != pyatspi.ROLE_PANEL:
                return []

            isSelected = lambda x: x and x.getState().contains(pyatspi.STATE_SELECTED)
            children = pyatspi.findAllDescendants(obj, isSelected)
        else:
            children = []
            for x in range(selection.nSelectedChildren):
                children.append(selection.getSelectedChild(x))

        return children

    def insertedText(self, event):
        if event.any_data:
            return event.any_data

        if event.detail1 == -1:
            msg = "GNOME SHELL: Broken text insertion event"
            debug.println(debug.LEVEL_INFO, msg, True)

            text = self.queryNonEmptyText(event.source)
            if text:
                string = text.getText(0, -1)
                if string:
                    msg = "HACK: Returning last char in '%s'" % string
                    debug.println(debug.LEVEL_INFO, msg, True)
                    return string[-1]

            msg = "GNOME SHELL: Unable to correct broken text insertion event"
            debug.println(debug.LEVEL_INFO, msg, True)

        return ""


    def selectedText(self, obj):
        string, start, end = super().selectedText(obj)
        if -1 not in [start, end]:
            return string, start, end

        msg = "GNOME SHELL: Bogus selection range (%i, %i) for %s" % (start, end, obj)
        debug.println(debug.LEVEL_INFO, msg, True)

        text = self.queryNonEmptyText(obj)
        if text.getNSelections() > 0:
            string = text.getText(0, -1)
            start, end = 0, len(string)
            msg = "HACK: Returning '%s' (%i, %i) for %s" % (string, start, end, obj)
            debug.println(debug.LEVEL_INFO, msg, True)

        return string, start, end
