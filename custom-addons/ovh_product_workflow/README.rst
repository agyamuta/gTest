.. image:: https://img.shields.io/badge/licence-AGPL--3-blue.svg
   :target: http://www.gnu.org/licenses/agpl-3.0-standalone.html
   :alt: License: AGPL-3

=================================================
OVH Product Workflow
=================================================

This module extends Product functionality to implement OVH specific workflow
to manage parts and server with specific statuses .

Standard workflow is linear: 1 → 10 → 100 → 1000 → EoL → Inactive, 
but products may change stages backward or skip stages.

When the status is changed, a specific list of persons from the 
"Product State Change" channel will be notified thru email. 
Message is also posted thru that channel.

Configuration
=============

Discuss Channel
---------------

* Look for the the Private Channel -> Product State Change.
* Click settings and add members on this channel.


Usage
=====

Product Template/Product Variant
a. Add a Selection field "Status" with the following values: 
   "('1', 'Proto R&D'), ( '10', 'Preserie Indus'), ('100', 'Preserie Prod'), 
   ('1000', 'Mass-Prod'), ('EoL', 'End of Life'), ('Inactive', 'Inactive')"
b. Add the "Product Status Change" channel to all existing and new products
c. When status is changed to 10, check the box "Can be sold"
d. When status is changed to EoL, uncheck the box "Can be purchased"
e. When EoL Date is reached, automatically change status to Eol state.

Partner
Add a boolean field "Is Broker". If the Partner is a broker, it is automatically a customer.

Bill of Materials
The "Consumed in Operation" field is empty if the product is in status 1 and Inactive.

Requests for Quotations (Purchase)
When the quotation is confirmed, display the error message 
"The Product X is in status Y. It cannot be purchased." where Y product status may be EoL or Inactive.

Stock Moves
When the stock moves is transferred, display the error message "The Product X is in status Y. 
It cannot be stored." if the product is in status 1 and the destination location is the stock location or a sublocation of stock.

Manufacturing Order
Filter the produced product field with only products in status 100, 1000 and EoL
When the MO is confirmed, display the error message "The component X is in status Y. 
It cannot be used in a manufacturing order." if one of the component is not in status 100, 1000 and EoL.

Sales Order Line
Filter the list of products to hide the ones in status Inactive if the customer is not a broker.

Sales Order
When the quotation is confirmed, display the error message "The product X is in status Y. It cannot be sold." if 
the box "Can be sold" is unchecked on the product
the customer is not a broker and the product is in status Inactive


Contributors
------------

* Antonio Yamuta <ayamuta@opensourceintegrators.com>


