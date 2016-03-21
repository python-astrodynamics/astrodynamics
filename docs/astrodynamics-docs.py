# coding: utf-8
# This file is dual licensed under the terms of the Apache License, Version
# 2.0, and the BSD License. See the licenses/CRYPTOGRAPHY.txt file in this
# repository for complete details.
#
# This file is adapted from cryptography-docs.py by the The Cryptography
# Developers.
from __future__ import absolute_import, division, print_function

from docutils import nodes
from sphinx.util.compat import Directive, make_admonition

IMPORT_MESSAGE = """The contents of this module are placed here for
organisational reasons. They should be imported from :py:mod:`{module}`."""


class ImportFromDirective(Directive):
    has_content = True

    def run(self):
        message = IMPORT_MESSAGE.format(module=self.content[0])

        ad = make_admonition(
            ImportFrom,
            self.name,
            [],
            self.options,
            nodes.paragraph("", message),
            self.lineno,
            self.content_offset,
            self.block_text,
            self.state,
            self.state_machine
        )
        ad[0].line = self.lineno
        return ad


class ImportFrom(nodes.Admonition, nodes.Element):
    pass


def html_visit_importfrom_node(self, node):
    return self.visit_admonition(node, "note")


def latex_visit_importfrom_node(self, node):
    return self.visit_admonition(node)


def depart_importfrom_node(self, node):
    return self.depart_admonition(node)


def setup(app):
    app.add_node(
        ImportFrom,
        html=(html_visit_importfrom_node, depart_importfrom_node),
        latex=(latex_visit_importfrom_node, depart_importfrom_node),
    )
    app.add_directive('importfrom', ImportFromDirective)
