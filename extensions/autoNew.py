import re


# Example plugin for EditorFunctions type plugins
# The functionality was originally implemented by endura29 <endura29@gmail.com>
#
# The plugin allows to install new menu items and toolbar items and register a
# a function with each that is called. The function must accept one argument which
# is the instance of PersonalWikiFrame providing access to the editor and the data store.
#
# To register a menu item implement the function describeMenuItem to return a
# sequence of tuples at least containing the callback function, the item string
# and an item tooltip (see below for details).
#
# To register a toolbar item implement the function describeToolbarItem to return
# a tuple at least containing the callback function, item label, tooltip and icon.
#
# both register functions must accept one argument which is again the
# PersonalWikiFrame instance

# descriptor for EditorFunctions plugin type
WIKIDPAD_PLUGIN = (("MenuFunctions",1),)

def describeMenuItems(wiki):
    """
    wiki -- Calling PersonalWikiFrame
    Returns a sequence of tuples to describe the menu items, where each must
    contain (in this order):
        - callback function
        - menu item string
        - menu item description (string to show in status bar)
    It can contain the following additional items (in this order), each of
    them can be replaced by None:
        - icon descriptor (see below, if no icon found, it won't show one)
        - menu item id.

    The  callback function  must take 2 parameters:
        wiki - Calling PersonalWikiFrame
        evt - wxCommandEvent

    An  icon descriptor  can be one of the following:
        - a wxBitmap object
        - the filename of a bitmap (if file not found, no icon is used)
        - a tuple of filenames, first existing file is used
    """
    global nextNumber
    
    return ((autoNew, "Create new page\tShift-Ctrl-N", "Create new page"),)


_testRE = re.compile(ur"^New[0-9]{6}$")


def autoNew(wiki, evt):
    wiki.saveCurrentWikiPage()
    candidates = wiki.wikiData.getWikiWordsStartingWith(u"New",
            includeAliases=False)
            
    candidates = filter(lambda w: _testRE.match(w), candidates)
    numbers = map(lambda w: int(w[3:]), candidates)

    if len(numbers) == 0:
        nextNumber = 1
    else:
        nextNumber = max(numbers) + 1
    wiki.openWikiPage(u"New%06i" % nextNumber)
    wiki.editor.SetFocus()
