import webbrowser

def helper(decorated):
    """Displays the docstring for a function when that function is passed the '--help' or '-h' arg

    This is the main source of help documentation for the CLI.
    Should be used to wrap all user-facing functionality."""

    def wrapper(fs, args):
        try:
            if (args[0] == '--help') or (args[0] == '-h'):
                try:
                    if args[1]:
                        print(decorated.__doc__, '\n')
                except IndexError:  #If the only argument is '--help', with no subsequent arg, then that try will fail due to being out of range.
                    print(decorated.__doc__.split('\n')[0], '\n')
            else:
                decorated(fs, *args)
        except IndexError:
            decorated(fs)  #Won't break if passed *args, since unpacking an empty list leaves nothing. However, it'd be pointless.
    return wrapper

def confirmation(decorated):
    """Provides a confirmation dialogue for the user when performing dangerous actions"""
    def wrapper(fs, args=None):  #Default set so this won't break for functions with no arguments
        choice = input("Are you sure you want to do this? [y/n]  ").lower()
        if (choice == 'y') or (choice == 'yes'):
            if args:
                decorated(fs, args)  #Having passed through 'helper', the arguments are not a list 
            else:
                decorated(fs)
        else:
            print("Action canceled.")
    wrapper.__doc__ = decorated.__doc__  #Ensures --help will return the help for the decorated function
    return wrapper

def help_summary():
    """Displays a brief summary of the cfs_manager help"""
    print("""
    All commands are preceded by dashes.
    Long-form commands start with two dashes, while shortenings start with one.

    A list of all commands can be reached with '--commands', and an about page with '--about'.
    The help for a specific command can be reached with '[command] --help'.
    To see a more detailed version of this or another help page, follow '--help' with '--verbose'.
    To quit this interface, use '--quit' or '-q'.
    """)

def help_file():
    """Displays the full, detailed help file for cfs_manager"""
    print("""
    All commands are preceded by dashes.
    Long-form commands are preceded by two dashes (eg. '--upload')
    Some of these commands have shortenings that do the same thing.
    These shortened commands only have one dash (eg. '-u')
    To see a list of all the valid commands, use '--commands'

    Commands can often be followed by 'arguments'.
    An argument is additional information that modifies how the command behaves.
    For example, if you're downloading files, you may want to say where to download to.
    You can do this by saying "--download-file [your preferred destination]".

    Some commands have defaults (eg. '--download-file' defaults to the Downloads folder).
    If a command has a default, it'll work without arguments by doing its default action.
    Other commands don't accept arguments (eg. '--list-files' just lists every file).
    If you use "[command] --help", you'll get a description of what it does and its arguments.

    A detailed version of a help page is given when the help command is followed by '--verbose'.
    (Following the '--help' with any argument does this, but '--verbose' and '-v' are typical.)
    To learn about CFS_Manager, use '--about'. To quit this interface, use '--quit' or '-q'.
    """)

@helper
def help_switch(fs, args=None):
    """Displays the help file for the cfs_manager command line"""
    if args:  #This is true if /any/ argument is passed after --help/-h; not just -v
        help_file()
    else:
        help_summary()

@helper
def about(*ignored):
    """Displays a summary of the CFS_Manager's description"""
    print("""
    This is the command line interface for the Cloud File-System Manager (CFS_Manager).
    This utility aims to make it easy for a user to manage a virtual file system.
    It is entirely written in Python 3 and is released under the Apache License 2.0
    To see the full text of the license (in your browser), use --license
    The source code can be found at https://github.com/alisonstreete/cfs-manager

    CFS_Manager was written (and is maintained) by Alison Streete.
    Do you have any questions, or have you encountered a bug?
    Please email her at alison.streete@gmail.com
    """)

@helper
def license(*ignored):
    """Opens the default browser to display the Apache License on Apache's website."""
    webbrowser.open('https://www.apache.org/licenses/LICENSE-2.0', new=2, autoraise=True)

@helper
def github(*ignored):
    """Opens the default browser to display CFS_Manager's Github repo."""
    webbrowser.open('https://github.com/alisonstreete/cfs-manager', new=2, autoraise=True)

@helper
def documentation(*ignored):
    """Opens the default browser to display the index page of CFS_Manager's documentation."""
    webbrowser.open('https://cfs-manager.readthedocs.io/en/latest/', new=2, autoraise=True)

@helper
def quit_doc(fs):
    """Quits the CFS_Manager command line interface"""

    #This function does not actually quit the CLI. It's main() that reacts to the quit commands.
    #This function only exists so that the user can see the quit commands when they list commands.