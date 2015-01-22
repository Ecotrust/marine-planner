# -*- coding: utf-8 -*-
#
# http://djangosnippets.org/snippets/1550/
# Got this from http://opensourcehacker.com/2013/05/16/putting-breakpoints-to-html-templates-in-python/
#
# Insert the following into any django template to trigger the debugger
# {% load debug %}
# {% pdb %}
# and did something similar to the following in the debugging environment
# for d in context.dicts: print d.keys()
# context['asdf'].adsf.asdf

import pdb as pdb_module

from django.template import Library, Node

register = Library()

class PdbNode(Node):

    def render(self, context):
        pdb_module.set_trace()
        return ''

@register.tag
def pdb(parser, token):
    return PdbNode()