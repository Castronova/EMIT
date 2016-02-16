

import os, sys
from subprocess import Popen, PIPE

def run_tests(nose_args):

    # get the path to the virtualenv nosetests, otherwise imports will be messed up
    exc = os.path.abspath(sys.executable)
    n = os.path.join(
            os.path.dirname(exc), 'nosetests'
    )

    cmd = [n, '--nologcapture'] + args
    process = Popen(cmd, stdout=PIPE)
    for c in iter(lambda: process.stdout.read(1), ''):
        sys.stdout.write(c)


if __name__ == "__main__":

    args = sys.argv[1:]
    run_tests(args)
