#coding=utf-8
__author__='silver'
from controller.base import BaseHandler
from util.filemanager import getdocumentdetail
from util.filemanager import getdocumentlist
from util.mdparser import article
import tornado.web


class SpecialPageListHandler(BaseHandler):
    def get(self, *args, **kwargs):
        special_page_root_dir=self.opts.document_location+"/pages"
        try:
            lst=getdocumentlist(special_page_root_dir, recursive=False)
            if len(lst)==0:
                raise FileNotFoundError
        except FileNotFoundError:
            raise tornado.web.HTTPError(404, reason='No special pages.')
        for i in range(len(lst)):
            lst[i].update(article(lst[i]['path']).extract())
        lst[:] = [d for d in lst if d.get('filename') != 'index']

        lst.sort(key=lambda i:i['title'])
        self.render('list.htm', disphandler='page.aspx', pagetitle="Some lonely pages.", articleList=lst, pagenum=1, max_page=1)

    def post(self):
        self.get()

class SpecialPageHandler(BaseHandler):
    def get(self, filename, *args, **kwargs):
        special_page_root_dir=self.opts.document_location+"/pages"
        try:
            fileinfo=getdocumentdetail(special_page_root_dir+'/'+filename+'.md')
            if (filename == 'index') and (kwargs['flag']!=1):
                raise FileNotFoundError
        except FileNotFoundError:
            raise tornado.web.HTTPError(404, reason='Non-existing article.')
        blog=article(fileinfo['path'])
        blog.render()
        self.render("article.htm", title=blog.info['title'], md_html=blog.html, articleInfo=blog.info)

    def post(self):
        self.get()


class IndexPage(SpecialPageHandler):
    def get(self, *args, **kwargs):
        super(IndexPage, self).get(filename='index', flag=1, comment=False)

    def post(self):
        self.get()
