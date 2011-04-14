from setuptools import setup, find_packages

version = '0.0.6'

setup(
    name = 'isotoma.recipe.squid',
    version = version,
    url = "http://github.com/isotoma/isotoma.recipe.squid",
    description = "Set up squid",
    long_description = open("README.rst").read() + "\n" + \
                       open("CHANGES.txt").read(),
    classifiers = [
        "Framework :: Buildout",
        "Intended Audience :: System Administrators",
        "Operating System :: POSIX",
        "License :: OSI Approved :: Apache Software License",

    ],
    package_data = {
        '': ['README.rst', 'CHANGES.txt'],
        'isotoma.recipe.squid': ['squid.conf']
    },
    keywords = "squid proxy cache buildout",
    author = "John Carr",
    author_email = "john.carr@isotoma.com",
    license="Apache Software License",
    packages = find_packages(exclude=['ez_setup']),
    namespace_packages = ['isotoma', 'isotoma.recipe'],
    include_package_data = True,
    zip_safe = False,
    install_requires = [
        'setuptools',
        'zc.buildout',
        'Cheetah',
        'isotoma.recipe.gocaptain',
    ],
    extras_require=dict(
        test = ['zope.testing',],
    ),
    entry_points = {
        "zc.buildout": [
            "default = isotoma.recipe.squid:Squid",
        ],
    }
)
