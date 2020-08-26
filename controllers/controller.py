# -*- coding: utf-8 -*-

from openerp import models, fields, api
import logging
logger = logging.getLogger(__name__)
import urllib
from werkzeug.wrappers import Response
import odoo

from openerp import http, SUPERUSER_ID
from openerp.http import request
import requests
from odoo.addons.web.controllers.main import ensure_db, Home

class website_login_token(http.Controller):
    
    @http.route('/login_token/<string:token>', type='http', auth="public",website=True)
    def login_token(self,token,**post):
        user_obj = request.env['res.users'].sudo()
        uid = request.session.authenticate(request.session.db, token, '')
        if uid is not False:
            user = user_obj.browse(uid)
            request.params['login_success'] = True
            return http.redirect_with_hash(user.redirect or '/web')