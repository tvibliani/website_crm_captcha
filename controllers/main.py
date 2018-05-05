# -*- coding: utf-8 -*-
import base64

import werkzeug
import werkzeug.urls

from openerp import http, SUPERUSER_ID
from openerp.http import request
from openerp.tools.translate import _

import logging
_logger = logging.getLogger(__name__)

from openerp.addons.website_crm.controllers.main import contactus as super_contactus

from captcha.image import ImageCaptcha
import random


class contactus(super_contactus):

    
    def gen_captcha(self,values):

        image = ImageCaptcha()
        captcha_value = str(random.randint(100,999))
        image_data = image.generate(captcha_value)

        values['captcha_src_data'] = base64.b64encode(image_data.getvalue())
        request.session['captcha_sent'] = captcha_value 

        image_data.close()



    @http.route(['/page/website.contactus', '/page/contactus'], type='http', auth="public", website=True)
    def contact(self, **kwargs):
        values = {}
        self.gen_captcha(values)
    
        for field in ['description', 'partner_name', 'phone', 'contact_name', 'email_from', 'name']:
            if kwargs.get(field):
                values[field] = kwargs.pop(field)
        values.update(kwargs=kwargs.items())
        return request.website.render("website.contactus", values)


    @http.route(['/crm/contactus'], type='http', auth="public", website=True)
    def contactus(self, **kwargs):
        captcha_reseived = kwargs.pop("captcha",False)
        captcha_sent = request.session.get("captcha_sent",False)
        error = False
        if (not captcha_reseived or not captcha_sent or not captcha_reseived == captcha_sent):
            values = {}
            for field in ['description', 'partner_name', 'phone', 'contact_name', 'email_from', 'name']:
                if kwargs.get(field):
                    values[field] = kwargs.pop(field)
            self.gen_captcha(values)
            error = set(['captcha'])
            values = dict(values, error=error, kwargs=kwargs.items())
            _logger.info("Captcha error by user: Captcha received (%s) != Captcha Sent (%s)\n"%(captcha_reseived,captcha_sent))
            return request.website.render(kwargs.get("view_from", "website.contactus"), values)
    
        return super_contactus.contactus(self, **kwargs)


