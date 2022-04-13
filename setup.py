from setuptools import setup
from pathlib import Path

this_directory = Path(__file__).parent
long_description = (this_directory / "README.md").read_text()

setup(name='longtrends',
      version='0.5',
      description='Download long-term Google Trends',
      long_description=long_description,
      long_description_content_type='text/markdown',
      url='http://github.com/mikedbjones/longtrends',
      author='Mike Jones',
      author_email='mikedbjones@gmail.com',
      license='MIT',
      packages=['longtrends'],
      install_requires=[
          'pytrends',
      ],
      zip_safe=False)
