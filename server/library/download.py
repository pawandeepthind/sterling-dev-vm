#!/usr/bin/python
# -*- coding: utf-8 -*-
#
# Author: Pawandeep Singh
#
#  Ansible module to download file from ftp.
#

#---- Documentation Start ----------------------------------------------------#
DOCUMENTATION = '''
---
version_added: "2.0.1"
module: download
short_description: download
description:
  - This module downloads a file from ftp to a local
options:
  url:
    description:
      Ftp url to download the file
    required: true
  dest:
    description:
      Path to the destination.
    required: true
requirements: []
author: Pawandeep Singh
'''

EXAMPLES = '''
- name: "Download the file"
  download: url="Url to download" dest_path="/path/to/destination"
'''
import urllib

#---- Logic Start ------------------------------------------------------------#

def main():
    # Note: 'AnsibleModule' is an Ansible utility imported below
    module = AnsibleModule(
        argument_spec=dict(
            url=dict(required=True),
            dest=dict(required=True),
        ),
        supports_check_mode=True
    )
    url = module.params['url']
    dest = module.params['dest']    
    urllib.urlretrieve (url, dest)
    module.exit_json(text="File (%s) successfully downloaded at (%s)" % (url, dest))

#---- Import Ansible Utilities (Ansible Framework) ---------------------------#
from ansible.module_utils.basic import *
main()