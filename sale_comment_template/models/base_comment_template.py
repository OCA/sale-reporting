from odoo import models


class BaseCommentTemplate(models.Model):
    """Comment templates printed on reports"""

    _name = "base.comment.template"
    _inherit = ["base.comment.template", "mail.render.mixin"]
