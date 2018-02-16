# Copyright (C) 2018 - TODAY, Open Source Integrators
# Integrators License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import api, fields, models


class ProductTemplate(models.Model):
    _inherit = 'product.template'

    status = fields.Selection(
        [('proto', '[1]Proto R&D'), ('indus', '[10]Preserie Indus'),
         ('pprod', '[100]Preserie Prod'), ('mprod', '[1000]Mass-Prod'),
         ('eol', 'End of Life'), ('inactive', 'Inactive')],
        default='proto',
        compute='_compute_status',
        inverse='_inverse_status',
        string='OVH Status',
        track_visibility='onchange')

    @api.depends('product_variant_ids', 'product_variant_ids.status')
    def _compute_status(self):
        for template in self:
            if len(template.product_variant_ids) != 1:
                continue
            template.status = template.product_variant_ids.status

    @api.multi
    def _inverse_status(self):
        if len(self.product_variant_ids) == 1:
            self.product_variant_ids.status = self.status

    @api.onchange('status')
    def _onchange_status(self):
        for template in self:
            # self holds the new status of the product
            if template.status == 'indus':
                # When status is changed to 10, check the box "Can be sold"
                template.sale_ok = True
            elif template.status == 'eol':
                # When status is changed to EoL,
                # uncheck the box "Can be purchased"
                template.purchase_ok = False
            template.product_variant_id.email_product_state_change(
             template, template.product_variant_id)
        return

    @api.model
    def send_notify_product_state_change(self, product):
        # send email to recipients from the Product State Change Channel.
        self.email_product_state_change(product)
        return True


class ProductProduct(models.Model):
    _inherit = 'product.product'

    # TBD: check on how not to affect service/consumable product
    status = fields.Selection(
        [('proto', '[1]Proto R&D'), ('indus', '[10]Preserie Indus'),
         ('pprod', '[100]Preserie Prod'), ('mprod', '[1000]Mass-Prod'),
         ('eol', 'End of Life'), ('inactive', 'Inactive')],
        default='proto',
        string='OVH Status',
        track_visibility='onchange')

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
    def email_product_state_change(self, new_object, product_change):
        if not product_change:
            return
        msg_values = self._prepare_product_workflow()
        product_change.message_post_with_view(
            'ovh_product_workflow.message_product_workflow',
            values={'self': new_object, 'origin': product_change},
            **msg_values)

    @api.onchange('status')
    def _onchange_status(self):
        context = self._context
        product_id = context.get('product_id') or False
        if product_id:
            for product in self:
                # self.status holds the new OVH status of the product
                if product.status == 'indus':
                    # When status is changed to 10, check the box "Can be sold"
                    product.product_tmpl_id.sale_ok = True
                elif product.status == 'eol':
                    # When status is changed to EoL,
                    # uncheck the box "Can be purchased"
                    product.product_tmpl_id.purchase_ok = False
                # get active product that is being updated
                active_product = product.browse(product_id)
                product.email_product_state_change(product, active_product)
        return
