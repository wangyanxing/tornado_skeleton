from __future__ import absolute_import

import socket

import sqlalchemy.orm
import sqlalchemy
from clay_config import config, os

sessions = {}

DB_URL = 'postgresql+psycopg2://{}@:{}/{}'


def get_db_engine(engine_type='write'):
    db_config = config.get('database.{}'.format(engine_type))[0]
    db_url = DB_URL.format(
        db_config.get('user'),
        db_config.get('port'),
        db_config.get('dbname'),
    )
    connect_args = {'application_name': '%s@%s.%d' % (
        'bootcamp', socket.gethostname().split('.')[0], os.getpid())}

    engine = sqlalchemy.create_engine(
        db_url,
        poolclass=sqlalchemy.pool.QueuePool,
        pool_recycle=60,
        connect_args=connect_args
    )
    return engine


def get_db_session(session_type='write', engine=None):
    if session_type not in sessions:
        bind = engine or get_db_engine(session_type)
        sessions[session_type] = sqlalchemy.orm.scoped_session(
            sqlalchemy.orm.sessionmaker(bind=bind, autoflush=False,
                                        query_cls=sqlalchemy.orm.query.Query)
        )
    return sessions[session_type]
