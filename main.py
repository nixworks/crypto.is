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
		self.render("blog.html")
class BlogArchiveHandler(tornado.web.RequestHandler):
	def get(self):
		bloglist = open('/web/crypto.is/templates/bloglist.txt', 'r')
		lines = bloglist.readlines()
		posts = []
		for p in lines:
			f = open('/web/crypto.is/templates/blog/' + p.strip() + '.html', 'r')
			title = [i for i in f.readlines() if '<h1>' in i][0].replace('</', '').replace('<', '').replace('h1>', '')
			posts.append((title.strip(), p.strip()))
		self.render("blogarchives.html", posts=posts)
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
			(r"/blog/archives?/?", BlogArchiveHandler),
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
	application.listen(8888)
	tornado.ioloop.IOLoop.instance().start()
