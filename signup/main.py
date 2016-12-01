import os
import jinja2

import webapp2
import cgi
import re


#
# Variables
#

template_dir = os.path.join(os.path.dirname(__file__), 'html')
jinja_env = jinja2.Environment(loader = jinja2.FileSystemLoader(template_dir),
                               autoescape = True)

USER_RE = re.compile(r"^[a-zA-Z0-9_-]{3,20}$")
PASS_RE = re.compile(r"^.{3,20}$")
EMAIL_RE = re.compile(r"^[\S]+@[\S]+.[\S]+$")


#
# Methods
#

def valid_username(username):
    return USER_RE.match(username)

def valid_password(username):
    return PASS_RE.match(username)

def valid_email(username):
    return EMAIL_RE.match(username)


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
        self.run()

    def post(self):
        # Variables
        user_error=''
        pass_error=''
        verify_error=''
        email_error=''

        username = self.request.get('username')
        password = self.request.get('password')
        verify = self.request.get('verify')
        email = self.request.get('email')

        # Validation
        if not valid_username(username):
            user_error="That's not a valid username."

        if not valid_password(password):
            pass_error="That's not a valid password."

        elif not (password==verify):
            verify_error="Your passwords didn't match."

        if email and (not valid_email(email)):
            email_error="That's not a valid email."

        # TODO: Body

        # Output
        if (user_error+pass_error+verify_error+email_error):
            self.run( user_error, pass_error, verify_error, email_error,
            username, email )
        else:
            self.redirect('/welcome?username='+username)

    def run( self, user_error='', pass_error='', verify_error='',
    email_error='', username='', email='' ):
        style = self.render_str('main.css')
        self.render('signup.html', style=style, user_error=user_error,
                    pass_error=pass_error, verify_error=verify_error,
                    email_error=email_error, username=username, email=email)


class WelcomePage(Handler):
    def get(self):
        username = self.request.get('username')
        self.write("<h1>Welcome, %s!</h1>"%username)


#
# Output
#

app = webapp2.WSGIApplication([
    ('/', MainPage),
    ('/welcome', WelcomePage)
], debug=True)
