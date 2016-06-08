#!/usr/bin/env python

from setuptools import setup

setup(name='yatank-online',
      version='1.8.1',
      description='Yandex.Tank Report plugin',
      author='Alexey Lavrenuke',
      author_email='direvius@gmail.com',
      url='https://github.com/yandex-load/yatank-online/',
      packages=['yandextank.plugins.Report'],
      package_data={'yandextank.plugins.Report': [
          'templates/*',
          'static/favicon.ico',
          'static/css/*',
          'static/js/*.js',
          'static/js/*.coffee',
          'static/js/vendor/*.js',
          'static/fonts/*',
      ]},
      namespace_packages=['yandextank', 'yandextank.plugins'],
      install_requires=[
          'tornado',
          'tornadio2',
          'pyjade>=4.0.0',
      ], )
