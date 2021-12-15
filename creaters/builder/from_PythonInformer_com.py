# https://pythoninformer.com/programming-techniques/design-patterns/builder/
class IBuilder:

    def addHeader(self):
        pass

    def addMean(self, value):
        pass

    def addMin(self, value):
        pass

    def addMax(self, value):
        pass

    def addFooter(self):
        pass

    def build(self):
        return ''


class ReportGenerator:
    def __init__(self, data):
        self.data = data

    def create(self, builder):
        builder.addHeader()
        builder.addMean(sum(self.data)//len(self.data))
        builder.addMin(min(self.data))
        builder.addMax(max(self.data))
        builder.addFooter()

        return builder.build()


class TextReportBuilder(IBuilder):

    def __init__(self):
        self.report = ''

    def addHeader(self):
        pass

    def addMean(self, value):
        self.report += 'Mean {}\n'.format(value)

    def addMin(self, value):
        self.report += 'Min {}\n'.format(value)

    def addMax(self, value):
        self.report += 'Max {}\n'.format(value)

    def addFooter(self):
        pass

    def build(self):
        return self.report


class HTMLReportBuilder(IBuilder):

    def __init__(self):
        self.report = ''

    def addHeader(self):
        self.report += '<html>\n'

    def addMean(self, value):
        self.report += '  <p>Mean {}</p>\n'.format(value)

    def addMin(self, value):
        self.report += '  <p>Min {}</p>\n'.format(value)

    def addMax(self, value):
        self.report += '  <p>Max {}</p>\n'.format(value)

    def addFooter(self):
        self.report += '</html>\n'

    def build(self):
        return self.report



