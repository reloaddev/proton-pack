class Line(object):
    def __init__(self, line_number, line_content):
        self.line_number = line_number
        self.line_content = line_content

    def get_line_number(self):
        return self.line_number

    def get_line_content(self):
        return self.line_content