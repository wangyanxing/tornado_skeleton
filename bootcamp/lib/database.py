from __future__ import absolute_import

import sqlalchemy.orm
import sqlalchemy
from clay_config import config

engines = {}


def get_db_engine(engine_type='write'):
    if engine_type in engines:
        return engines[engine_type]
    else:
        engine = sqlalchemy.engine_from_config(
            {'sqlalchemy.url': config.get('sqlalchemy.master.url')},
            poolclass=sqlalchemy.pool.NullPool,
        )
        engines[engine_type] = engine
        return engine


def get_db_session(engine_type='write'):
    bind = get_db_engine(engine_type)
    return sqlalchemy.orm.scoped_session(
        sqlalchemy.orm.sessionmaker(bind=bind, autoflush=False)
    )
