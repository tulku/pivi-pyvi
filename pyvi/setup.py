from distutils.core import setup

setup(name='pyvi',
      version='0.1',
      packages=['pyvi', 'utils'],
      scripts=['scripts/pyvi'],
      # metadata for upload to PyPI
      author="Lucas Chiesa",
      author_email="lucas@lessindustries.com",
      description="Uploads power measurments to LESS cloud",
      license="CC Share Alike",
      keywords="power, serial, IoT"
      )
