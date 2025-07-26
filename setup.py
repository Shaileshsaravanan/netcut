from setuptools import setup, find_packages

setup(
    name='netcut',
    version='1.0.0',
    author='Shailesh Saravanan',
    description='All-in-one terminal network toolkit for diagnostics, security, and web intelligence.',
    packages=find_packages(where="src"),
    package_dir={"": "src"},
    install_requires=[
        'requests',
        'scapy',
        'dnspython',
        'beautifulsoup4',
        'speedtest-cli',
        'python-whois',
        'psutil',
        'ping3'
    ],
    entry_points={
        'console_scripts': [
            'netcut=netcut.main:main',
        ],
    },
    classifiers=[
        'Programming Language :: Python :: 3',
        'Environment :: Console',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.7',
)