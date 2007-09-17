#!/usr/bin/python

"""Test "Where Am I" on a push button in Firefox.
"""

from macaroon.playback.keypress_mimic import *

sequence = MacroSequence()

########################################################################
# We wait for the focus to be on a blank Firefox window.
#
sequence.append(WaitForWindowActivate("Minefield",None))

########################################################################
# Open the "File" menu and press U for the Page Setup dialog
#
sequence.append(KeyComboAction("<Alt>f"))

sequence.append(WaitForFocus("New Window", pyatspi.ROLE_MENU_ITEM))
sequence.append(TypeAction("u"))

########################################################################
# In the Page Setup dialog, shift+tab to the OK push button, wait three
# seconds, then do a where am I. 
#
sequence.append(WaitForWindowActivate("Page Setup",None))
sequence.append(KeyComboAction("<Shift>ISO_Left_Tab"))

sequence.append(WaitForFocus("Format & Options", acc_role=pyatspi.ROLE_PAGE_TAB))
sequence.append(KeyComboAction("<Shift>ISO_Left_Tab"))

sequence.append(WaitForFocus("OK", acc_role=pyatspi.ROLE_PUSH_BUTTON))
sequence.append(KeyComboAction("KP_Enter", 3000))

########################################################################
# Close the dialog
#
sequence.append(KeyComboAction("Escape"))

# Just a little extra wait to let some events get through.
#
sequence.append(WaitForFocus("Location", acc_role=pyatspi.ROLE_ENTRY))
sequence.append(WaitForFocus(acc_role=pyatspi.ROLE_INVALID, timeout=3000))

sequence.start()
