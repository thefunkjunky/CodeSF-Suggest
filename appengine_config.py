from google.appengine.ext import vendor
import os

# Add any libraries installed in the "lib" folder.
print(os.getcwd())
vendor.add('lib')