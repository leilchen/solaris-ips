#!/usr/bin/python2.4
#
# CDDL HEADER START
#
# The contents of this file are subject to the terms of the
# Common Development and Distribution License (the "License").
# You may not use this file except in compliance with the License.
#
# You can obtain a copy of the license at usr/src/OPENSOLARIS.LICENSE
# or http://www.opensolaris.org/os/licensing.
# See the License for the specific language governing permissions
# and limitations under the License.
#
# When distributing Covered Code, include this CDDL HEADER in each
# file and include the License file at usr/src/OPENSOLARIS.LICENSE.
# If applicable, add the following below this CDDL HEADER, with the
# fields enclosed by brackets "[]" replaced with your own identifying
# information: Portions Copyright [yyyy] [name of copyright owner]
#
# CDDL HEADER END
#

# Copyright 2009 Sun Microsystems, Inc.  All rights reserved.
# Use is subject to license terms.

from cli import testutils

if __name__ == "__main__":
        testutils.setup_environment("../../../proto")

try:
        import ldtp
except ImportError:
        raise ImportError, "SUNWldtp package not installed."

class TestPkgGuiHelp(testutils.SingleDepotTestCase):
        # Only start/stop the depot once (instead of for every test)
        persistent_depot = True

        foo10 = """
            open package1@1.0,5.11-0
            add set name="description" value="Some package1 description"
            close """

        def setUp(self, debug_features=None):
                testutils.SingleDepotTestCase.setUp(self)

        def tearDown(self):
                testutils.SingleDepotTestCase.tearDown(self)

        def testPmHelp(self):
                repo_url = self.dc.get_depot_url()
                self.pkgsend_bulk(repo_url, self.foo10)
                self.image_create(repo_url)

                ldtp.launchapp("%s/usr/bin/packagemanager" % testutils.g_proto_area)

                ldtp.click('frmPackageManager', 'mnuContents')

                # Verify result
                ldtp.waittillguiexist('*Online Help')
                self.assertEqual(ldtp.guiexist('*Online Help'), 1)
                        
                ldtp.selectmenuitem('*Online Help', 'mnuCloseWindow')

                
                # Quit UpdateManager
                ldtp.click('frmPackageManager', 'mnuQuit')

        def testPmAbout(self):

                ldtp.launchapp("%s/usr/bin/packagemanager" % testutils.g_proto_area)

                ldtp.selectmenuitem('frmPackageManager', 'mnuAbout')

                # Verify result
                self.assertEqual(ldtp.guiexist('About Package Manager'), 1)
                                
                ldtp.waittillguiexist('dlgAboutPackageManager')
                ldtp.click('dlgAboutPackageManager', 'btnClose')
                
                # Quit Package Manager
                ldtp.selectmenuitem('frmPackageManager', 'mnuQuit')
