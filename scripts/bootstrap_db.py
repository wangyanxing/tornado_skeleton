#!/usr/bin/env python
from __future__ import absolute_import

import os
import sys
from clay import config


def drop_database(env='development', database_type='write'):
    """Drop the database."""
    os.environ['CLAY_CONFIG'] = './config/%s.yaml' % env

    db = config.get('database')
    db_info = db[database_type][0]
    db_name = db_info['dbname']

    print 'Deleting %s database' % db_name
    os.system('psql template1 -c "DROP DATABASE IF EXISTS %s";' % db_name)


def bootstrap_database(env='development', database_type='write'):
    """Create the database."""
    os.environ['CLAY_CONFIG'] = './config/%s.yaml' % env

    drop_database(env, database_type)

    db = config.get('database')
    db_info = db[database_type][0]
    db_name = db_info['dbname']
    db_user = db_info['user']

    print 'Creating %s database' % db_name

    commands = []
    commands.append('''
        DO
        \$body\$
        BEGIN
            IF NOT EXISTS (
                SELECT *
                FROM pg_catalog.pg_user
                WHERE usename = '{user}') THEN
                CREATE ROLE {user} LOGIN PASSWORD '';
            END IF;
        END
        \$body\$
        '''.format(user=db_user))
    commands.append('CREATE DATABASE {name}'.format(name=db_name))
    commands.append('GRANT ALL PRIVILEGES ON DATABASE {name} to {user}'.format(
        name=db_name,
        user=db_user
    ))

    for command in commands:
        os.system('psql template1 -c "%s";' % command.replace('\n', ' '))

    os.system('psql -U {user} -d {db} -a -f scripts/bootstrap_db.sql'.format(
        user=db_user, db=db_name))


def main():
    if len(sys.argv) > 1:
        if sys.argv[1] == 'drop':
            drop_database()
        else:
            bootstrap_database()

if __name__ == '__main__':
    sys.exit(main())
