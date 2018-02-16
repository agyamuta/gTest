# Copyright (C) 2018 - TODAY, Open Source Integrators
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

{
    "name": "OVH Product Work Flow",
    "summary": "OVH has a specific workflow to manage parts and servers with specific statuses",
    "version": "11.0.1.0.0",
    "license": "AGPL-3",
    "author": "Open Source Integrators",
    "category": "Product",
    "website": "http://www.opensourceintegrators.com",
    "depends": ["product", "stock", "purchase", "sale", "base"],
    "data": [
        "views/product_view.xml",
        "data/mail_channel_data.xml",
        "views/mail_templates.xml",
        "views/res_partner_view.xml",
        "views/stock_location_view.xml",
    ],
    "installable": True,
}
