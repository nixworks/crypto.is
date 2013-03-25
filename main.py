import os
import logging
import uuid
import tornado.ioloop
import tornado.web

class MainHandler(tornado.web.RequestHandler):
	def get(self):
		self.render("main.html")
class AboutHandler(tornado.web.RequestHandler):
	def get(self):
		self.render("about.html")
class AuditHandler(tornado.web.RequestHandler):
	def get(self):
		self.render("cpr.html")
class ProjectHandler(tornado.web.RequestHandler):
	def get(self):
		self.render("projects.html")

# Interact 
class InteractHandler(tornado.web.RequestHandler):
	def get(self):
		self.render("interact/interact.html")
class InteractTimeHandler(tornado.web.RequestHandler):
	def get(self):
		self.render("interact/time.html")
class InteractGoodsHandler(tornado.web.RequestHandler):
	def get(self):
		self.render("interact/goods.html")
# Blog Posts
class BlogHandler(tornado.web.RequestHandler):
	def get(self):
		bloglist = open('/web/crypto.is/templates/bloglist.txt', 'r')
		lines = bloglist.readlines()
		posts = []
		indx = 1
		for p in lines:
			f = open('/web/crypto.is/templates/blog/' + p.strip() + '.html', 'r')
			lines = f.readlines()
			title = [i for i in lines if '<h1>' in i][0].replace('</', '').replace('<', '').replace('h1>', '')
			details = [i for i in lines if 'blogdate' in i][0].replace('</div>', '').replace('<div class="blogdate">', '')
			posts.append((indx, title.strip(), details.strip(), p.strip()))
			indx += 1
		posts.reverse()
		self.render("blog.html", posts=posts)
class BlogPostHandler(tornado.web.RequestHandler):
	def get(self, post):
		if "." not in post and os.path.exists("/web/crypto.is/templates/blog/" + post + ".html"):
			self.render("blog/" + post + ".html")
		else:
			raise tornado.web.HTTPError(404)

class Application(tornado.web.Application):
	def __init__(self):
		handlers = [
			(r"/", MainHandler),
			(r"/about/?", AboutHandler),
			(r"/blog/?", BlogHandler),
			(r"/blog/(.*)", BlogPostHandler),
			(r"/projects/?", ProjectHandler),
			(r"/code-peer-review/?", AuditHandler),
			
			(r"/interact/?", InteractHandler),
			(r"/interact/time/?", InteractTimeHandler),
			(r"/interact/goods/?", InteractGoodsHandler)
		]
		settings = dict(
			debug=True,
			template_path=os.path.join(os.path.dirname(__file__), "templates"),
			static_path=os.path.join(os.path.dirname(__file__), "static"),
		)
		tornado.web.Application.__init__(self, handlers, **settings)
if __name__ == "__main__":
	application = Application()
	import socket
	if socket.has_ipv6:
		application.listen(8888)
	else:
		application.listen(8888, address="0.0.0.0")
	tornado.ioloop.IOLoop.instance().start()
