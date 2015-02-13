#!/usr/bin/env python

from setuptools import setup

setup(name='yatank-online',
      version='0.0.1',
      description='Yandex.Tank OnlineReport plugin',
      author='Alexey Lavrenuke',
      author_email='direvius@gmail.com',
      url='https://github.com/yandex-load/yatank-online/',
      packages=['yatank_OnlineReport'],
      package_data={'yatank_OnlineReport': [
          'templates/*',
          'static/favicon.ico',
          'static/css/*',
          'static/js/*.js',
          'static/js/*.coffee',
          'static/js/vendor/*.js',
          'static/fonts/*',
      ]}
     )
