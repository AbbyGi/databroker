from __future__ import print_function
import signal
import logging
import sys


from ..controls.positioner import Positioner
from ..controls.signal import Signal, SignalGroup


class SessionManager(object):
    _instance = None

    def __init__(self, logger=None, ipy=None):
        #TODO: FIXME... seriously...
        if SessionManager._instance is not None:
            return SessionManager._instance

        SessionManager._instance = self
        self._ipy = ipy
        self._logger = logger
        self._registry = {'positioners': {}, 'signals': {},
                        'beamline_config': {}}

        if ipy is not None:
            self._ipy = ipy
            session_mgr = self
            self._ipy.push('session_mgr')

        orig_hdlr = signal.getsignal(signal.SIGINT)

        def sigint_hdlr(sig, frame):
            self._logger.info('Calling SessionManager SIGINT handler...')
            self.stop_all()
            orig_hdlr(sig, frame)
            raise KeyboardInterrupt
        signal.signal(signal.SIGINT, sigint_hdlr)
        self._ipy.push('sigint_hdlr')

    def _update_registry(self, obj, category):
        if obj not in self._registry[category] and obj.name is not None:
            self._registry[category][obj.name] = obj

    # TODO: figure out what the policy needs to be here...
    def register(self, obj):
        '''Maintain a dict of positioners and detectors.

           If these objects are loaded via "ipython -i conf_script.py",
           then they're available in the ipy namespace too.
        '''
        if issubclass(obj.__class__, Positioner):
            self._update_registry(obj, 'positioners')
        elif issubclass(obj.__class__, (Signal, SignalGroup)):
            self._update_registry(obj, 'signals')
        else:
            raise TypeError('%s cannot be registered with the session.' % obj)
        return self._logger

    #TODO: should swallow and gracefully notify the user of changes
    def notify_connection(self, msg):
        self._logger.info('connection notification: %s' % msg)

    def stop_all(self):
        for pos in self._registry['positioners'].itervalues():
            if pos.moving is True:
                pos.stop()
                self._logger.info('Stopped %s' % pos)

    def get_positioners(self):
        return self._registry['positioners']

    #TODO: should we let this raise a KeyError exception? Probably...
    def get_positioner(self, pos):
        return self._registry['positioners'][pos]
