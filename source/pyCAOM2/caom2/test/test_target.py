#!/usr/bin/env python2.7
# -*- coding: utf-8 -*-
#***********************************************************************
#******************  CANADIAN ASTRONOMY DATA CENTRE  *******************
#*************  CENTRE CANADIEN DE DONNÉES ASTRONOMIQUES  **************
#
#  (c) 2010.                            (c) 2010.
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
#***********************************************************************
#

""" Defines TestTarget class """


from caom2.caom2_target import Target
from caom2.caom2_enums import TargetType
from caom2.util.caom2_util import TypedList
import os
import sys
import unittest

# put build at the start of the search path
sys.path.insert(0, os.path.abspath('../../lib.local/lib'))


class TestTarget(unittest.TestCase):

    def testAll(self):

        target = Target("myTarget")
        self.assertEqual("myTarget", target.name, "target name")
        target.target_type = TargetType.FIELD
        self.assertEqual(TargetType.FIELD, target.target_type, "target type")
        self.assertEqual(0, len(target.keywords), "Default number of keywords")
        target.keywords.append("optical")
        self.assertEqual(1, len(target.keywords), "Number of keywords")
        self.assertEqual("optical", target.keywords[0], "Keyword")
        self.assertIsNone(target.redshift, "Default redshift")
        target.redshift = 123.321
        self.assertEqual(123.321, target.redshift, "Redshift")
        self.assertIsNone(target.standard, "Default standard")
        target.standard = True
        self.assertTrue(target.standard, "Standard")
        self.assertIsNone(target.moving, "Default moving")
        target.moving = True
        self.assertTrue(target.moving, "Moving")

        target = Target("myOtherTarget", TargetType.OBJECT, False, 1.2,
                        TypedList((str), "radio"), False)
        self.assertEquals("myOtherTarget", target.name, "target name")
        self.assertEquals(TargetType.OBJECT, target.target_type, "target type")
        self.assertFalse(target.standard, "Standard")
        self.assertEquals(1.2, target.redshift, "Redshift")
        self.assertEquals(1, len(target.keywords), "Keywords")
        self.assertEquals("radio", target.keywords[0], "Keywords")
        self.assertFalse(target.moving, "Moving")


if __name__ == '__main__':
    unittest.main()