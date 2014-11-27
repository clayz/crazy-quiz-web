"""`appengine_config` gets loaded when starting a new application instance."""
import sys
import os.path

# add `lib` subdirectory to `sys.path`, so our `main` module can load
# third-party libraries.
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'lib'))
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'lib/PyAPNs'))
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'lib/facebook-sdk'))
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'lib/requests'))
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'lib/tweepy'))

# add source code subdirectory
sys.path.append(os.path.join(os.path.dirname(__file__), "src"))
