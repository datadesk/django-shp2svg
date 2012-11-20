from __future__ import with_statement
from fabric.api import *
import os



def rmpyc():
    """
    Erases pyc files from current directory.

    Example usage:

        $ fab rmpyc

    """
    print("Removing .pyc files")
    with hide('everything'):
        local("find . -name '*.pyc' -print0|xargs -0 rm", capture=False)


def rs(port=8000):
    """
    Fire up the Django test server, after cleaning out any .pyc files.

    Example usage:
    
        $ fab rs
        $ fab rs:port=9000
    
    """
    with settings(warn_only=True):
        rmpyc()
    local("python manage.py runserver 0.0.0.0:%s" % port, capture=False)


def sh():
    """
    Fire up the Django shell, after cleaning out any .pyc files.

    Example usage:
    
        $ fab sh
    
    """
    rmpyc()
    local("python manage.py shell", capture=False)


def load():
    """
    Prints the current load values.
    
    Example usage:
    
        $ fab stage load
        $ fab prod load
        
    """
    def _set_color(load):
        """
        Sets the terminal color for an load average value depending on how 
        high it is.
        
        Accepts a string formatted floating point.

        Returns a formatted string you can print.
        """
        value = float(load)
        template = "\033[1m\x1b[%sm%s\x1b[0m\033[0m"
        if value < 1:
            # Return green
            return template % (32, value)
        elif value < 3:
            # Return yellow
            return template % (33, value)
        else:
            # Return red
            return template % (31, value)
    
    with hide('everything'):
        # Fetch the data
        uptime = run("uptime")
        # Whittle it down to only the load averages
        load = uptime.split(":")[-1]
        # Split up the load averages and apply a color code to each depending
        # on how high it is.
        one, five, fifteen = [_set_color(i.strip()) for i in load.split(',')]
        # Get the name of the host that is currently being tested
        host = env['host']
        # Combine the two things and print out the results
        output = u'%s: %s' % (host, ", ".join([one, five, fifteen]))
        print(output)

