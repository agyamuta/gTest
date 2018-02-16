# Copyright (C) 2018 - TODAY, Open Source Integrators
# Integrators License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import api, fields, models


class ProductTemplate(models.Model):
    _inherit = 'product.template'

    ovh_status = fields.Selection(
        [('proto', '[1]Proto R&D'), ('indus', '[10]Preserie Indus'),
         ('pprod', '[100]Preserie Prod'), ('mprod', '[1000]Mass-Prod'),
         ('eol', 'End of Life'), ('inactive', 'Inactive')],
        default='proto',
        compute='_compute_ovh_status',
        inverse='_inverse_ovh_status',
        string='OVH Status',
        track_visibility='onchange')

    @api.depends('product_variant_ids', 'product_variant_ids.ovh_status')
    def _compute_ovh_status(self):
        unique_variants = self.filtered(
            lambda template: len(template.product_variant_ids) == 1)
        for template in unique_variants:
            template.ovh_status = template.product_variant_ids.ovh_status

    @api.multi
    def _inverse_ovh_status(self):
        if len(self.product_variant_ids) == 1:
            self.product_variant_ids.ovh_status = self.ovh_status

    @api.model
    def _prepare_product_workflow(self):
        # TBD: need to check for the author
        mail_msg = self.env['mail.message'].browse(
            self.env.ref(
             'ovh_product_workflow.mail_message_product_workflow').id)
        msg_values = {
            'res_id': mail_msg.res_id,
            'model': mail_msg.model,
            'subject': mail_msg.subject,
            'message_type': mail_msg.message_type,
            'subtype_id': mail_msg.subtype_id.id}
        return msg_values

    @api.model
    def email_product_state_change(self, product_change):
        if not product_change:
            return
        msg_values = self._prepare_product_workflow()
        product_change.message_post_with_view(
            'ovh_product_workflow.message_product_workflow',
            values={'self': self, 'origin': product_change},
            **msg_values)

    @api.onchange('ovh_status')
    def _onchange_ovh_status(self):
        for template in self:
            # self.ovh_status holds the new OVH status of the product
            if self.ovh_status == 'indus':
                # When status is changed to 10, check the box "Can be sold"
                template.sale_ok = True
            elif self.ovh_status == 'eol':
                # When status is changed to EoL,
                # uncheck the box "Can be purchased"
                template.purchase_ok = False
            self.email_product_state_change(template.product_variant_id)
        return

    @api.model
    def send_notify_product_state_change(self, product):
        # send email to recipients from the Product State Change Channel.
        self.email_product_state_change(product)
        return True


class ProductVariants(models.Model):
    _inherit = 'product.product'

    # TBD: check on how not to affect service/consumable product
    ovh_status = fields.Selection(
        [('proto', '[1]Proto R&D'), ('indus', '[10]Preserie Indus'),
         ('pprod', '[100]Preserie Prod'), ('mprod', '[1000]Mass-Prod'),
         ('eol', 'End of Life'), ('inactive', 'Inactive')],
        default='proto',
        string='OVH Status',
        track_visibility='onchange')

    @api.model
    def email_product_state_change(self, product_change):
        if not product_change:
            return
        msg_values = self.env['product.template']._prepare_product_workflow()
        product_change.message_post_with_view(
            'ovh_product_workflow.message_product_workflow',
            values={'self': self, 'origin': product_change},
            **msg_values)

    @api.onchange('ovh_status')
    def _onchange_ovh_status(self):
        for product in self:
            # self.ovh_status holds the new OVH status of the product
            if self.ovh_status == 'indus':
                # When status is changed to 10, check the box "Can be sold"
                product.product_variant_id.product_tmpl_id.sale_ok = True
            elif self.ovh_status == 'eol':
                # When status is changed to EoL,
                # uncheck the box "Can be purchased"
                product.product_variant_id.product_tmpl_id.purchase_ok = False
            self.email_product_state_change(product.product_variant_id)
        return
