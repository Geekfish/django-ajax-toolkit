from setuptools import setup

setup(name='django-ajax-toolkit',
      version='',
      url='https://github.com/Geekfish/django-ajax-toolkit',
      author="Eleni Lixourioti",
      author_email="contact@eleni.co",
      description="",
      long_description=open('README.rst').read(),
      keywords="Ajax utilities for Django",
      license='BSD',
      platforms=['linux'],
      packages=('ajaxtoolkit'),
      include_package_data=True,
      install_requires=[
          'simplejson==2.5.2',
          ],
      # See http://pypi.python.org/pypi?%3Aaction=list_classifiers
      classifiers=['Environment :: Web Environment',
                   'Framework :: Django',
                   'Intended Audience :: Developers',
                   'License :: OSI Approved :: BSD License',
                   'Operating System :: Unix',
                   'Development Status :: 3 - Alpha',
                   'Programming Language :: Python']
      )
