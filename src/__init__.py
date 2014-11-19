
import os

# class Settings(dict):
#     '''
#     Settings dict
#     ..note:: every instance shares the same values
#     '''

#     # inspired from Borg design pattern (or Monostate in C++)
#     # http://fr.wikipedia.org/wiki/Singleton_(patron_de_conception)#Python
#     # we don't use QSettings because we want to use it in non gui app

#     # default values
#     __shared_state = {
#             'preview/width': 200,
#             'puli/server': 'puliserver',
#             'puli/port': 8004,
#             'puli/pool': 'mik',
#             }

#     def __setitem__(self, key, value):
#         return self.__shared_state.__setitem__(key, value)

#     def __getitem__(self, key):
#         return self.__shared_state.__getitem__(key)

#     def __contains__(self, item):
#         return self.__shared_state.__contains__(item)
   
#     def iteritems(self):
#         return self.__shared_state.iteritems()

#     def __iter__(self):
#         return self.__shared_state.__iter__()

#     def __repr__(self):
#         return self.__shared_state.__repr__()


class Config(object):

    root_dir = os.path.dirname(os.path.abspath(__file__))

    # Global tools attributes
    qt_company_name="Mikros"
    qt_app_name="PuliMonitor"
    version=0.1

    log_level="debug"

    # Initial server/port config
    hostname="puliserver"
    port="8004"

    # Default formating & enums
    date_format = '%m/%d %H:%M'
    time_format = '%H:%M'
    precise_date_format = '%m/%d %H:%M:%S'
    precise_time_format = '%H:%M:%S'
