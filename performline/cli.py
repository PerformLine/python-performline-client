import os
import sys


def errout(message, exitcode=1):
    sys.stderr.write('%s\n' % message)
    os.exit(exitcode)
