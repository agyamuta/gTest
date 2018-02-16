# Copyright (C) 2018 - TODAY, Open Source Integrators
# Integrators License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import fields, models


class Location(models.Model):
    _inherit = "stock.location"

    hors_prod_location = fields.Boolean(
        'Not a Production Location?',
        help='Check this box if this location is not for Production')
