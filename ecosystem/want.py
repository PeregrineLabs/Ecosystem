import re


class Want(object):
    """Defines a request, possibly with a specific version"""

    def __init__(self,
                 requirement):
        self.requirement = requirement

    @property
    def tool(self):
        return re.findall(r".*?(?=[0-9])", self.requirement + '0')[0]

    @property
    def version(self):
        result = re.findall(r"(?=[0-9]).*", self.requirement)
        return result[0] if result else ''
