from odoo import models, fields


class HrEmployeeInherit(models.Model):
    _inherit = "hr.employee"

    militray_certificate = fields.Binary()
