# This file defines migrations that are to be run on states as they are loaded from the hard drive.  A global application version # is defined in cmdcenter/__init__.py, and 
# this version # is checked against the version defined in the State object.  If necessary, all migrations defined with a version # less than that of the object are run.


import copy

import cmdcenter
from common.default import *

from common.log import *
set_log("MIGRATION")

# ALL MIGRATIONS
def default(vars):
    pass

# dict of all VERSION: migrations
all_migrations = {1.0: default}

# main migrate method
def migrate(vars):
    # test if update necessary
    old_version = vars["VERSION"]
    if(old_version < cmdcenter.VERSION):

        # get necessary migrations
        migrations = all_migrations.keys()
        migrations = [version for version in migrations if version > old_version]
        migrations.sort()

        # run migrations
        for version in migrations:
            all_migrations[version](vars)

        # update VERSION
        vars["VERSION"] = cmdcenter.VERSION

    return vars


# TODO: increment through all states, migrate & save
def migrate_all_states():
    pass
