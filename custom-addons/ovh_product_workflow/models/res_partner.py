# Copyright (C) 2018 - TODAY, Open Source Integrators
# Integrators License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import api, fields, models


class ResPartner(models.Model):
    _inherit = "res.partner"

    broker = fields.Boolean(string='Is a Broker')
    customer = fields.Boolean(
        string='Is a Customer', default=True,
        help="Check this box if this contact is a customer.")

    @api.onchange('broker')
    def _on_change_isbroker(self):
        if self.broker and not self.customer:
            self.customer = True

    @api.onchange('customer')
    def _on_change_customer(self):
        if self.broker and not self.customer:
            self.broker = False
