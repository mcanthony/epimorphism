import noumena
import common.default

import copy
from common.log import *
set_log("MIGRATION")

from phenom.datamanager import *

# dict of all migrations
all_migrations = {}

def migrate(vars):

    # test if update necessary
    old_version = vars["VERSION"]
    if(old_version < noumena.VERSION):


        # get necessary migrations
        migrations = all_migrations.keys()
        migrations = [version for version in migrations if version > old_version]
        migrations.sort()

        # run migrations
        for version in migrations:
            all_migrations[version](vars)

        # update VERSION
        vars["VERSION"] = phenom.VERSION

    return vars
