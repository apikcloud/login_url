# -*- coding: utf-8 -*-

from odoo import api, models, registry, SUPERUSER_ID,fields
import logging
logger = logging.getLogger(__name__)
import uuid

class res_users(models.Model):
    _name = "res.users"
    _inherit = 'res.users'

    @api.depends("login")
    def get_token(self):
        for u in self:
            u.token = str(uuid.uuid5(uuid.NAMESPACE_DNS,u.login))
    
    @api.depends('token')
    def get_url(self):
        base_url = self.env['ir.config_parameter'].sudo().get_param('web.base.url')
        for u in self:
            u.url_token = base_url + "/login_token/" + u.token
    
    token = fields.Char('Token',compute=get_token,store=True)
    url_token = fields.Char('URL',compute=get_url)
    redirect = fields.Char('Redirection',default='/web')
    
    @api.model
    def get_user(self,token):
        user_obj = self.env['res.users'].sudo()
        return user_obj.search([('token','=',token)])

    @classmethod
    def _login(cls, db, login, password):
        user_id = super(res_users, cls)._login(db, login, password)
        if user_id:
            return user_id
        with registry(db).cursor() as cr:
            env = api.Environment(cr, SUPERUSER_ID, {})
            user_id = env['res.users'].get_user(login)
            logger.info(user_id)
            if len(user_id)>0:
                return user_id.id
            