#!/usr/bin/env python3

import iterm2
import os, subprocess, getpass

# function to return user information
def get_user_info():
    _uid = os.getuid()
    _uname = getpass.getuser()
    return _uid, _uname

# function to prepare selected text
def prepare_recipes(cookbook):
    _special_chars = '✔\t\n\r'
    
    # prepare the kitchen
    _b = cookbook
    
    # replace the special characters
    for _char in _special_chars:
        _b = _b.replace(_char, ' ')
    
    # split into a list on those spaces,
    # sort them alphabetically
    _p = sorted(_b.split())
    print(_p)
    
    # return result
    return _p

# main function
async def main(connection):
    # get connection to selection
    app = await iterm2.async_get_app(connection)

    # get the window
    window = app.current_terminal_window
    if window is None:
        print("No current window")
    else:
        # get the session
        session = window.current_tab.current_session

        # check session
        if session is None:
            print("No current session")
        else:
            # get the selection and the text
            selection = await session.async_get_selection()
            recipes = await session.async_get_selection_text(selection)
            
            # get the dishes from the recipes
            items = prepare_recipes(recipes)
            
            # test if there are recipes
            if len(items) > 0:
                
                # get userid and name
                uid, uname = get_user_info()

                # now invoke a subprocess to tell brew to open it up
                cmd = ['launchctl',\
                      'asuser',\
                      '{}'.format(uid),\
                      'sudo',\
                      '-u',\
                      uname,\
                      '/usr/local/bin/brew',\
                      'home']

                # add the items to the command list
                cmd.extend(items)
                
                # execute the subprocess
                cp = subprocess.run(cmd)
            else:
                # nothing selected
                print("Could not get receipe name")

iterm2.run_until_complete(main)
