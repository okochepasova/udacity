import os
import jinja2

import webapp2
import cgi


#
# Variables
#

template_dir = os.path.join(os.path.dirname(__file__), 'html')
jinja_env = jinja2.Environment(loader = jinja2.FileSystemLoader(template_dir),
                               autoescape = True)


#
# Methods
#

# ROT13 encription
def encript(text):
    output = ""
    if text:
        text = ""+text
        for c in text:
            output += encript_letter(c)
    return output

def encript_letter(c):
    if (c >= 'a' and c <='z') or (c >= 'A' and c <='Z'):
        c = ord(c) + 13
        if c > ord('z') or (c > ord('Z') and c <= (ord('Z')+13)):
            c -= 26
        c = chr(c)
    return c


#
# Classes
#

class Handler(webapp2.RequestHandler):
    def write(self, *a, **k):
        self.response.out.write(*a, **k)

    def render_str(self, template, **params):
        t = jinja_env.get_template(template)
        return t.render(params)

    def render(self, template, **kw):
        self.write(self.render_str(template, **kw))


class MainPage(Handler):
    def get(self):
        self.run('')

    def post(self):
        text = self.request.get('text')
        self.run(encript(text))

    def run(self, text):
        style = self.render_str('main.css')
        self.render('rot13.html', style=style, text=text)


#
# Output
#

app = webapp2.WSGIApplication([
    ('/', MainPage)
], debug=True)
