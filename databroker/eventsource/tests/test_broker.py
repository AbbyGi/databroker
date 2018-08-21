from __future__ import (absolute_import, division, print_function,
                        unicode_literals)

from databroker.eventsource.tests.utils import (build_db_from_init,
                                                build_db_from_config)
from databroker import Broker

def test_event_sources_by_name():
    db = build_db_from_init()
    event_sources = db.event_sources_by_name
    assert list(event_sources) == ['mds', 'arch_csx']

def test_from_config():
    db = build_db_from_config()
    event_sources = db.event_sources_by_name
    assert list(event_sources) == ['mds', 'arch_csx']	
