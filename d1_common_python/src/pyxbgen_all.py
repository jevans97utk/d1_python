#!/usr/bin/env python

# Generate PyXB binding classes from schemas.

import datetime
import glob
import optparse
import os
from xml.etree.ElementTree import parse
try:
  import pysvn
except ImportError:
  print 'Try: sudo apt-get install python-svn'
  raise


def generateVersion(schema_path, binding_path):
  '''Given a DataONE schema, generates a version module that contains version
  information about the file.
  '''
  cli = pysvn.Client()
  svninfo = cli.info(schema_path)
  if svninfo is None:
    return
  svnrev = str(svninfo.revision.number)
  svnpath = svninfo.url
  xml = parse(schema_path)
  version = xml.getroot().attrib["version"]
  tstamp = datetime.datetime.utcnow().isoformat()
  fdest = file(binding_path, "w")
  fdest.write(
    """#This file is automatically generated. Manual edits will be erased.

# When this file was generated
TIMESTAMP="%s"

# Path of the schema used in the repository
SVNPATH="%s"

# SVN revision of the schema that was used
SVNREVISION="%s"

# The version tag of the schema
VERSION="%s"
  
  """ % (tstamp, svnpath, svnrev, version)
  )
  fdest.close()


def main():
  # Command line opts.
  parser = optparse.OptionParser()
  # The default location for the schemas relative to d1_common_python if both were checked out as part of cicore.
  parser.add_option(
    '-s',
    '--schemas',
    dest='schemas_path',
    action='store',
    type='string',
    default='./d1_schemas'
  )
  parser.add_option(
    '-t',
    '--bindings',
    dest='bindings_path',
    action='store',
    type='string',
    default='./d1_common/types/generated'
  )
  parser.add_option(
    '-p',
    '--process',
    dest='process_schemas',
    action='store',
    type='string',
    default='dataoneTypes.xsd;dataoneErrors.xsd'
  )

  (opts, args) = parser.parse_args()

  if not os.path.exists(opts.bindings_path):
    print 'The destination folder for the bindings does not exist.'
    print 'This script should be run from ./d1_common_python/src'
    exit()

  process_schemas_list = opts.process_schemas.split(';')

  for schema_filename in process_schemas_list:
    schema_name = os.path.splitext(schema_filename)[0]
    print 'Processing: {0}'.format(schema_name)
    schema_path = os.path.join(opts.schemas_path, schema_filename)
    binding_path = os.path.join(
      opts.bindings_path, os.path.splitext(schema_filename)[0] + '.py'
    )

    # pyxbgen sometimes does not want to overwrite existing binding classes.
    try:
      os.unlink(binding_path)
    except OSError:
      pass

    # Create file containing version information.
    version_path = os.path.splitext(binding_path)[0] + '_version.txt'
    generateVersion(schema_path, version_path)

    # Run pyxbgen.
    args = []
    args.append('--binding-root=\'{0}\''.format(opts.bindings_path))
    #args.append('--location-prefix-rewrite=\'https://repository.dataone.org/software/cicore/trunk/schemas/={0}\''.format(opts.schema_path))
    # Note: If we split the schema out to multiple files, pyxbgen is still
    # run only once, but with multiple sets of -u and -m.
    args.append('-u \'{0}\' -m \'{1}\''.format(schema_path, schema_name))
    cmd = 'pyxbgen {0}'.format(' '.join(args))
    print(cmd)
    os.system(cmd)


if __name__ == '__main__':
  main()
