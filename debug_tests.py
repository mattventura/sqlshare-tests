# Shell entry point

from sqlshare_tests_c import *

import code

c = get_test_class()

code.interact(local=locals())

c.tearDown()
