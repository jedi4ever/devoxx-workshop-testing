#https://skeptric.com/python-diffs/
from itertools import zip_longest
import html

def html_sidebyside(a, b):
    # Set the panel display
    out = '<div style="display: grid;grid-template-columns: 1fr 1fr;grid-gap: 20px;">'
    # There's some CSS in Jupyter notebooks that makes the first pair unalign. This is a workaround
    out += '<p></p><p></p>'
#    for left, right in zip_longest(a, b, fillvalue=''):
#        out += f'<p>{left}</p>'
#        out += f'<p>{right}</p>'
#        out += '</div>'
    out +=f'<p>{a}</p>'
    out +=f'<p>{b}</p>'
    out += '</div>'

    return out

from IPython.display import HTML, display
def show_diffs(a, b):
    #print(html_sidebyside(a, b))
    display(HTML(html_sidebyside(a, b)))
