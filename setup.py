from distutils.core import setup

setup(
    name='enroll_gcalendar',
    packages=['enroll_gcalendar'],
    version='0.5',
    license='MIT',
    description='Convert enroll-me.iiet.pl schedules to google calendar for CS IET students',
    author='Hubert Pelczarski',
    author_email='pelczarskihubert@gmail.com',
    url='https://github.com/hoob3rt/enroll-gcalendar',
    download_url='https://github.com/hoob3rt/enroll-gcalendar/archive/0.1.tar.gz',
    keywords=['agh', 'google-calendar-api', 'enroll-me.iiet.pl'],
    install_requires=[
        'selenium',
        'google_auth_oauthlib',
        'google_api_python_client',
        'google-auth-httplib2',
    ],
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'Topic :: Education',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3.8',
    ],
)
