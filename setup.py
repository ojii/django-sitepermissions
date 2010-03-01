APP_NAME = 'sitepermissions'
PACKAGE_NAME = 'django-%s' % APP_NAME
DESCRIPTION = 'django sitepermissions app'
PROJECT_URL = 'http://github.com/ojii/%s/' % PACKAGE_NAME

INSTALL_REQUIRES = [
]

AUTHOR = "Jonas Obrist"

EXTRA_CLASSIFIERS = [
]


# DO NOT EDIT ANYTHING DOWN HERE... this should be common to all django app packages
from setuptools import setup, find_packages
import os

version = __import__(APP_NAME).__version__

classifiers = [
    'Environment :: Web Environment',
    'Framework :: Django',
    'Intended Audience :: Developers',
    'License :: OSI Approved :: BSD License',
    'Operating System :: OS Independent',
    'Programming Language :: Python',
    'Topic :: Internet :: WWW/HTTP :: Dynamic Content',
    'Topic :: Software Development',
    'Topic :: Software Development :: Libraries :: Application Frameworks',
]
if not 'a' in version and not 'b' in version: classifiers.append('Development Status :: 5 - Production/Stable')
elif 'a' in version: classifiers.append('Development Status :: 3 - Alpha')
elif 'b' in version: classifiers.append('Development Status :: 4 - Beta')

for c in EXTRA_CLASSIFIERS:
    if not c in classifiers:
        classifiers.append(c)

media_files = []

setup(
    author=AUTHOR,
    name=PACKAGE_NAME,
    version=version,
    url=PROJECT_URL,
    description=DESCRIPTION,
    long_description=DESCRIPTION,
    platforms=['OS Independent'],
    classifiers=classifiers,
    requires=INSTALL_REQUIRES,
    packages=find_packages(),
    package_dir={
        APP_NAME: APP_NAME,
    },
    zip_safe = False
)