# -*- coding: utf-8 -*-
# ***********************************************************************
# ******************  CANADIAN ASTRONOMY DATA CENTRE  *******************
# *************  CENTRE CANADIEN DE DONNÉES ASTRONOMIQUES  **************
#
#  (c) 2016.                            (c) 2016.
#  Government of Canada                 Gouvernement du Canada
#  National Research Council            Conseil national de recherches
#  Ottawa, Canada, K1A 0R6              Ottawa, Canada, K1A 0R6
#  All rights reserved                  Tous droits réservés
#
#  NRC disclaims any warranties,        Le CNRC dénie toute garantie
#  expressed, implied, or               énoncée, implicite ou légale,
#  statutory, of any kind with          de quelque nature que ce
#  respect to the software,             soit, concernant le logiciel,
#  including without limitation         y compris sans restriction
#  any warranty of merchantability      toute garantie de valeur
#  or fitness for a particular          marchande ou de pertinence
#  purpose. NRC shall not be            pour un usage particulier.
#  liable in any event for any          Le CNRC ne pourra en aucun cas
#  damages, whether direct or           être tenu responsable de tout
#  indirect, special or general,        dommage, direct ou indirect,
#  consequential or incidental,         particulier ou général,
#  arising from the use of the          accessoire ou fortuit, résultant
#  software.  Neither the name          de l'utilisation du logiciel. Ni
#  of the National Research             le nom du Conseil National de
#  Council of Canada nor the            Recherches du Canada ni les noms
#  names of its contributors may        de ses  participants ne peuvent
#  be used to endorse or promote        être utilisés pour approuver ou
#  products derived from this           promouvoir les produits dérivés
#  software without specific prior      de ce logiciel sans autorisation
#  written permission.                  préalable et particulière
#                                       par écrit.
#
#  This file is part of the             Ce fichier fait partie du projet
#  OpenCADC project.                    OpenCADC.
#
#  OpenCADC is free software:           OpenCADC est un logiciel libre ;
#  you can redistribute it and/or       vous pouvez le redistribuer ou le
#  modify it under the terms of         modifier suivant les termes de
#  the GNU Affero General Public        la “GNU Affero General Public
#  License as published by the          License” telle que publiée
#  Free Software Foundation,            par la Free Software Foundation
#  either version 3 of the              : soit la version 3 de cette
#  License, or (at your option)         licence, soit (à votre gré)
#  any later version.                   toute version ultérieure.
#
#  OpenCADC is distributed in the       OpenCADC est distribué
#  hope that it will be useful,         dans l’espoir qu’il vous
#  but WITHOUT ANY WARRANTY;            sera utile, mais SANS AUCUNE
#  without even the implied             GARANTIE : sans même la garantie
#  warranty of MERCHANTABILITY          implicite de COMMERCIALISABILITÉ
#  or FITNESS FOR A PARTICULAR          ni d’ADÉQUATION À UN OBJECTIF
#  PURPOSE.  See the GNU Affero         PARTICULIER. Consultez la Licence
#  General Public License for           Générale Publique GNU Affero
#  more details.                        pour plus de détails.
#
#  You should have received             Vous devriez avoir reçu une
#  a copy of the GNU Affero             copie de la Licence Générale
#  General Public License along         Publique GNU Affero avec
#  with OpenCADC.  If not, see          OpenCADC ; si ce n’est
#  <http://www.gnu.org/licenses/>.      pas le cas, consultez :
#                                       <http://www.gnu.org/licenses/>.
#
#  $Revision: 4 $
#
# ***********************************************************************
#

"""
A collection of utility methods for CAOM2.

This module contains a number of 'TYPED' objects for use in CAOM2.
These Typed versions were implemented so that content checking near
the first point of use could be implemented.  This helps the data
engineer get the correct meta data more quickly.
"""

from __future__ import (absolute_import, division, print_function,
                        unicode_literals)

import collections
import struct
import sys
import uuid
from datetime import datetime

__all__ = ['TypedList', 'TypedSet', 'TypedOrderedDict', 'ClassProperty']


# TODO both these are very bad, implement more sensibly
IVOA_DATE_FORMAT = "%Y-%m-%dT%H:%M:%S.%f"


def validate_path_component(caller, name, test):
    """
    Function to validate a URI path component. Component is invalid
    if it contains space ( ), slash (/), escape (\\) or percent (%) characters.

    Arguments:
    caller : caller object
    name : name of the component
    test : component to be tested

    An assertionError is thrown when the the provided test argument
    is invalid
    """

    assert (' ' not in test and
            '/' not in test and
            '||' not in test and
            '%' not in test), (
        caller.__class__.__name__ + ": invalid " + name +
        ": may not contain space ( ), slash (/), escape (\\), or percent (%)")


def date2ivoa(d):
    """
    Takes a datetime and returns a string formatted
    to the IVOA date format yyyy-MM-dd'T'HH:mm:ss.SSS
    """

    if d is None:
        return None
    return d.strftime(IVOA_DATE_FORMAT)[:23]


def str2ivoa(s):
    """Takes a IVOA date formatted string and returns a datetime"""

    if s is None:
        return None
    return datetime.strptime(s, IVOA_DATE_FORMAT)


def attr2str(s):
    pass


def repr2str(s):
    pass


def uuid2long(uid):
    """
    UUID is 128 bits (32 bytes). Unpack the 32 bytes into two
    16 byte longs. For CAOM-2.0 compatibility only the least significant
    16 bytes in the UUID should have a value.

    return the UUID least significant bytes as a long.
    """
    longs = struct.unpack(str('>qq'), str(uid.bytes))
    if longs[0] != 0:
        raise ValueError("lossy conversion from UUID to long: {}".format(uid))
    return longs[1]


def long2uuid(l):
    """
    Takes a long and creates a UUID using the 16 byte long
    as the least significant bytes in the 32 byte UUID.
    """
    if l.bit_length() > 63:
        raise ValueError("expected 64 bit long {}".format(l))
    if l < 0:
        l = (1<<64L) + l
    return uuid.UUID(int=l)


def type_check(value, value_type, variable, override=None):
    """Check value is of type value_type, or is override"""

    sys.tracebacklimit = None
    if not isinstance(value, value_type) and value is not override:
        if override is not False:
            raise TypeError(
                "Excepted {} or {} for {}, received {}".format(value_type,
                                                               override,
                                                               variable,
                                                               type(value)))
        else:
            raise TypeError(
                "Expected {} for {}, received {}".format(value_type,
                                                         variable,
                                                         type(value)))
    return True


def value_check(value, min_value, max_value, variable, override=None):
    """Check if value is inside allowed range, or override"""

    sys.tracebacklimit = None
    if value != override and not (min_value <= value <= max_value):
        if override is not False:
            raise ValueError(
                "Expected {} <= {} <= {} or {}, received {}".format(
                    min_value, variable, max_value, override, value))
        else:
            raise ValueError(
                "Expected {} <= {} <= {}, received {}".format(
                    min_value, variable, max_value, value))

    return True


class TypedList(collections.MutableSequence):
    """
    Class that implements a typed list in Python. Supported types
    are specified when instance is created. Example:

       obstype = TypedList((str), "calibration", "science")
       emptylist = TypedList((str), )
       multipletypes = TypedList((str, int, long), 1, 12L, "ABC")

    An AssertionError is thrown when the caller attempts to insert
    objects with the wrong type.
    """

    def __init__(self, oktypes, *args):
        """
        Initializes a TypedList.

        Arguments:
        oktypes : a list of types accepted in this list
        *args : values to be stored in the list

        AssertionError will be raised if the types of the arguments
        are not found in the list of oktypes.
        """
        self._oktypes = oktypes
        self.list = list()
        self.extend(list(args))

    def __str__(self):
        return "\n".join(["{}".format(v) for v in self])

    def __repr__(self):
        return "TypedList((%r))," % self._oktypes + (
            "(".join(["(%r)" % v for v in self]) + ")")

    def check(self, v):
        assert isinstance(v, self._oktypes), (
            "Wrong type in list. OK Types: {0}".format(self._oktypes))

    def __len__(self):
        return len(self.list)

    def __getitem__(self, i):
        return self.list[i]

    def __delitem__(self, i):
        del self.list[i]

    def __setitem__(self, i, v):
        self.check(v)
        self.list[i] = v

    def insert(self, i, v):
        self.check(v)
        self.list.insert(i, v)


class TypedSet(collections.MutableSet):
    """
    Class that implements a typed set in Python. Supported types
    are specified when instance is created. Example:

       obstype = TypedSet((str), "calibration", "science")
       emptyset = TypedSet((str), )
       multipletypes = TypedSet((str, int, long), 1, 12L, "ABC")

    An AssertionError is thrown when the caller attempts to insert
    objects with the wrong type.
    """

    def __init__(self, oktypes, *args):
        """
        Initializes a TypedSet.

        Arguments:
        oktypes : a list of types accepted in this set
        *args : values to be stored in the set

        AssertionError will be raised if the types of the arguments
        are not found in the list of oktypes.
        """
        self._oktypes = oktypes
        self._set = set()
        for arg in args:
            self.add(arg)

    def check(self, v):
        assert isinstance(v, self._oktypes), (
            "Wrong type in list. OK Types: {0}".format(self._oktypes))

    def add(self, v):
        """Add an element."""
        self.check(v)
        self._set.add(v)

    def update(self, other):
        """Add all elements in other."""
        for v in other:
            self.check(v)
        self._set.update(other)

    def discard(self, v):
        """Remove an element. Do not raise an exception if absent."""
        self._set.discard(v)

    def __iter__(self):
        return iter(self._set)

    def __len__(self):
        return len(self._set)

    def __contains__(self, item):
        try:
            return item in self._set
        except AttributeError:
            return False


class TypedOrderedDict(collections.OrderedDict):
    """
    Class that implements a typed ordered dictionary in Python. Supported
    type is specified when an instance is created. A supported type
    must have a key property that is used as the key in the dictionary.

    Example:

       obsType = TypedOrderedDict((Plane), ("productID1", Plane('productID1')))
       emptyDict = TypedSet((Plane), )

    A TypeError is thrown when the caller attempts to insert objects
    with the wrong type.
    """

    def __init__(self, key_type, *args):
        """
        Initializes a TypedOrderedDict.

        Arguments:
        keyType : the type values that will be stored in this dictionary
        *args : (key, value) tuples to be stored in the dictionary
        (value must match type)

        AssertionError will be raised if the type of the arguments
        is not the same as keyType.
        """
        super(TypedOrderedDict, self).__init__(self)
        self._keyType = key_type
        for arg in args:
            self.__setitem__(arg[0], arg[1])

    def __str__(self):
        return "\n".join(["{} => {}".format(k, v)
                          for k, v in self.iteritems()])

    def __repr__(self):
        return "TypeOrderedDict((%r))," % self._keyType + (
            "(".join(["(%r,%r)" % (k, v) for k, v in self.iteritems()]) + ")")

    def check(self, key, value):
        """
        Check that the value is of the correct type for this typed
        dictionary and that the key attribute of value matches the 'key'
        passed to check
        """

        if not isinstance(value, self._keyType):
            raise TypeError("Wrong type in dictionary. Key Type: {0}"
                            .format(self._keyType))
        if not value.key == key:
            raise ValueError("Key mismatch, key in object: {0}"
                             .format(value.key))

    def add(self, value):
        """Adds a new entry, value must be of type {0}"""
        self.__setitem__(value.key, value)

    def __setitem__(self, key, value):
        """Add an item."""
        self.check(key, value)
        super(TypedOrderedDict, self).__setitem__(key, value)


class ClassProperty(property):
    """ """
    def __get__(self, cls, owner):
        return self.fget.__get__(None, owner)()
