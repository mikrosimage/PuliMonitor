'''
Created on Jan 27, 2015

@author: Sebastian Elsner
@organization: rise|fx GmbH
'''

from PyQt4.QtGui import QFrame


def VLine(parent=None):
    f = QFrame(parent)
    f.setFrameShape(QFrame.VLine)
    f.setFrameShadow(QFrame.Sunken)
    return f


def dictToHtmlTable(dictionary, cssClass=''):
    # could be nicer with jinja/mako templates
    '''
    Taken from: http://www.stevetrefethen.com/blog/pretty-printing-a-python-dictionary-to-html
    pretty prints a dictionary into an HTML table(s)
    '''
    if isinstance(dictionary, str):
        return '<td>' + dictionary + '</td>'
    s = ['<table ']
    if cssClass != '':
        s.append('class="%s"' % (cssClass))
    s.append('>\n')
    for key, value in dictionary.iteritems():
        s.append('<tr>\n  <td valign="top"><strong>%s</strong></td>\n' % str(key))
        if isinstance(value, dict):
            if key == 'picture' or key == 'icon':
                s.append('  <td valign="top"><img src="%s"></td>\n' % dictToHtmlTable(value, cssClass))
            else:
                s.append('  <td valign="top">%s</td>\n' % dictToHtmlTable(value, cssClass))
        elif isinstance(value, list):
            s.append("<td><table>")
            for i in value:
                s.append('<tr><td valign="top">%s</td></tr>\n' % dictToHtmlTable(i, cssClass))
            s.append('</table>')
        else:
            if key == 'picture' or key == 'icon':
                s.append('  <td valign="top"><img src="%s"></td>\n' % value)
            else:
                s.append('  <td valign="top">%s</td>\n' % value)
        s.append('</tr>\n')
    s.append('</table>')
    return '\n'.join(s)

if __name__ == '__main__':
    d = {u'distribname': u'unknown', u'mikdistrib': u'unknown', u'cpuname': u'Intel(R) Xeon(R) CPU E5-2630 0 @ 2.30GHz', u'openglversion': u'', u'os': u'linux', u'softs': []}
    print dictToHtmlTable(d)
