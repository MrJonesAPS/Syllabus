#####
# To use this script, create a new .md file in the /templates folder
# and then provide the name of that file (without the md extension)
# as a command line argument. Example:
# python3 ./generatepdfs.py F_24_ITD110

#
# Explanation: uses Jinja2 to create a complete markdown file
# and then uses pypandoc to convert to a PDF. In addition to the
# packages below, the system must have pandoc installed.
#####

from jinja2 import Environment, FileSystemLoader, TemplateNotFound
from jinja2.ext import Extension
import re
import os
import pypandoc
import sys


class RelativeInclude(Extension):
    # This Jinja2 extension Created 2014 by Janusz Skonieczny
    # Source https://gist.github.com/wooyek/8d4c37d684a5ba38b8c1
    """Allows to import relative template names"""
    tags = set(["include2"])

    def __init__(self, environment):
        super(RelativeInclude, self).__init__(environment)
        self.matcher = re.compile("\\.*")

    def parse(self, parser):
        node = parser.parse_include()
        template = node.template.as_const()
        if template.startswith("."):
            # determine the number of go ups
            up = len(self.matcher.match(template).group())
            # split the current template name into path elements
            # take elements minus the number of go ups
            seq = parser.name.split("/")[:-up]
            # extend elements with the relative path elements
            seq.extend(template.split("/")[1:])
            template = "/".join(seq)
            node.template.value = template
        return node


# Setup environment for Jinja
env = Environment(
    loader=FileSystemLoader("templates"),
    extensions=[RelativeInclude],
    trim_blocks=True,
    lstrip_blocks=True,
)

filename = sys.argv[1]
template = env.get_template(filename + ".md")
rendered_template = template.render()
os.makedirs(os.path.dirname("markdown/" + filename + ".md"), exist_ok=True)
os.makedirs(os.path.dirname("pdfs/" + filename + ".pdf"), exist_ok=True)
with open("markdown/" + filename + ".md", "w") as fh:
    fh.write(rendered_template)

pypandoc.convert_file(
    "markdown/" + filename + ".md", to="pdf", outputfile="pdfs/" + filename + ".pdf"
)
