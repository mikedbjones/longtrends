from setuptools import setup

setup(name='longtrends',
      version='0.1',
      description='Download long-term Google Trends.',
      url='http://github.com/mikedbjones/longtrends',
      author='Mike Jones',
      author_email='mikedbjones@gmail.com',
      license='MIT',
      packages=['longtrends'],
      install_requires=[
          'pytrends',
      ],
      zip_safe=False)
