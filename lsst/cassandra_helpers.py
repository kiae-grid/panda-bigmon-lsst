import itertools
import re

from cassandra.auth import PlainTextAuthProvider
from cqlengine import connection


# XXX: Doesn't really belongs here, probably can be transformed
# XXX: into some Django'ish stuff.  Should investigate and fix.
def connectToCassandra(dbaccess):
    """
    Sets up Cassandra connection for Django

    Arguments:
     - dbaccess: common hash that describes Django DB connections
       in a usual way.  Must have key 'cassandra' from which we
       will take 'NAME', 'USER', 'PASSWORD' and 'HOST'.
       'HOST' can contain multiple comma-separated host names.
       'NAME' specifies Cassandra keyspace to connect to.
    """

    sectionName = 'cassandra'
    if sectionName not in dbaccess:
        raise KeyError("Passed 'dbaccess' dict does not contain key '%s'" % \
          (sectionName))
    section = dbaccess[sectionName]
    missing_keys = []
    for k in ('USER', 'PASSWORD', 'HOST', 'NAME'):
        if k not in section:
            missing_keys.append(k)
    if len(missing_keys):
        raise KeyError("dbaccess['%s'] is missing the following keys: %s" % \
          sectionName, ", ".join(missing_keys))
    user = section['USER']
    password = section['PASSWORD']
    hosts = re.split(r'\s*,\s*', section['HOST'])
    keyspace = section['NAME']

    auth = PlainTextAuthProvider(username = user, password = password)
    connection.setup(hosts, keyspace, protocol_version = 2,
      auth_provider = auth)


def cqlValuesDict(fields, query):
    """
    Cqlengine helper that acts like a .values() function in Django

    Transform query result list into usual list of dicts.

    Arguments:
     - fields: names of fields to select
     - query: cqlengine query (XXX.objects.filter(...).limit())
    """

    retval = map(lambda x: dict(itertools.izip(fields, x)), query.values_list(*fields))
    return retval
