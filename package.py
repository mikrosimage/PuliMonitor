name = 'puliMonitor'
version = '0.0.1'

# If your tool depends on some other package(s)
requires = [
    'puli',
    'python-2',
    'tornado-2.2.1',
    'requests-2.4.3',
    'psutil-2.1.3',
    'pyqt',
]


# If you need to define some environment variables
def commands():

    # Need to prepend the package root to make package version accessible (and not overidden by other packages like tornado)
    env.PYTHONPATH.append('{root}/src')

    alias('puliMonitor', 'python {root}/src/main.py')
