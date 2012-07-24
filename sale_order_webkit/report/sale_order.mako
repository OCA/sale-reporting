<html>
<head>
    <style type="text/css">
        ${css}
			.list_sale_table {
			border:thin solid #E3E4EA;
			text-align:center;
			border-collapse: collapse;
			}
			.list_sale_table td {
			border-top : thin solid #EEEEEE;
			text-align:right;
			font-size:12;
			padding-right:3px
			padding-left:3px
			padding-top:3px
			padding-bottom:3px
			}

			.list_bank_table {
			text-align:center;
			border-collapse: collapse;
			}
			.list_bank_table td {
			text-align:left;
			font-size:12;
			padding-right:3px
			padding-left:3px
			padding-top:3px
			padding-bottom:3px
			}

			.list_bank_table th {
			background-color: #EEEEEE;
			text-align:left;
			font-size:12;
			font-weight:bold;
			padding-right:3px
			padding-left:3px
			}
			
			.list_sale_table th {
			background-color: #EEEEEE;
			border: thin solid #000000;
			text-align:center;
			font-size:12;
			font-weight:bold;
			padding-right:3px
			padding-left:3px
			}
			
			.list_table thead {
			    display:table-header-group;
			}


			.list_tax_table {
			}
			.list_tax_table td {
			text-align:left;
			font-size:12;
			}
			
			.list_tax_table th {
			}


			.list_table thead {
			    display:table-header-group;
			}


			.list_total_table {
				border-collapse: collapse;
			}
			.list_total_table td {
			text-align:right;
			font-size:12;
			}

			.no_bloc {
				border-top: thin solid  #ffffff ;
			}

			
			.list_total_table th {
				background-color: #F7F7F7;
				border-collapse: collapse;
			}


			.right_table {
			right: 4cm;
			width:"100%";
			}
			
			.std_text {
				font-size:12;
				}


    </style>
</head>
<body>
    <%page expression_filter="entity"/>
    <%
    def carriage_returns(text):
        return text.replace('\n', '<br />')

    %>
    %for order in objects:
    <% setLang(order.partner_id.lang) %>
    <%
      quotation = order.state == 'draft'
    %>
    <div class="address">
        <table class="recipient">
            <tr><td class="name">${order.partner_id.title or ''}  ${order.partner_id.name }</td></tr>
            <tr><td>${order.partner_order_id.street or ''}</td></tr>
            <tr><td>${order.partner_order_id.street2 or ''}</td></tr>
            <tr><td>${order.partner_order_id.zip or ''} ${order.partner_order_id.city or ''}</td></tr>
            %if order.partner_order_id.state_id:
            <tr><td>${order.partner_order_id.state_id.name or ''} </td></tr>
            %endif
            %if order.partner_order_id.country_id:
            <tr><td>${order.partner_order_id.country_id.name or ''} </td></tr>
            %endif
            %if order.partner_order_id.phone:
            <tr><td>${_("Tel")}: ${order.partner_order_id.phone}</td></tr>
            %endif
            %if order.partner_order_id.fax:
            <tr><td>${_("Fax")}: ${order.partner_order_id.fax}</td></tr>
            %endif
            %if order.partner_order_id.email:
            <tr><td>${_("E-mail")}: ${order.partner_order_id.email}</td></tr>
            %endif
            %if order.partner_id.vat:
            <tr><td>${_("VAT")}: ${order.partner_id.vat}</td></tr>
            %endif
        </table>

        <table class="shipping">
            <tr><td class="address_title">${_("Shipping address:")}</td></tr>
            <tr><td >${order.partner_id.title or ''}  ${order.partner_id.name }</td></tr>
            <tr><td>${order.partner_shipping_id.street or ''}</td></tr>
            <tr><td>${order.partner_shipping_id.street2 or ''}</td></tr>
            <tr><td>${order.partner_shipping_id.zip or ''} ${order.partner_shipping_id.city or ''}</td></tr>
            %if order.partner_shipping_id.state_id:
            <tr><td>${order.partner_shipping_id.state_id.name or ''} </td></tr>
            %endif
            %if order.partner_shipping_id.country_id:
            <tr><td>${order.partner_shipping_id.country_id.name or ''} </td></tr>
            %endif
        </table>

        <table class="invoice">
            <tr><td class="address_title">${_("Invoice address:")}</td></tr>
            <tr><td>${order.partner_id.title or ''}  ${order.partner_id.name }</td></tr>
            <tr><td>${order.partner_invoice_id.street or ''}</td></tr>
            <tr><td>${order.partner_invoice_id.street2 or ''}</td></tr>
            <tr><td>${order.partner_invoice_id.zip or ''} ${order.partner_invoice_id.city or ''}</td></tr>
            %if order.partner_invoice_id.state_id:
            <tr><td>${order.partner_invoice_id.state_id.name or ''} </td></tr>
            %endif
            %if order.partner_invoice_id.country_id:
            <tr><td>${order.partner_invoice_id.country_id.name or ''} </td></tr>
            %endif
        </table>
    </div>
    <div>
    	
    %if order.note1_webkit :
    	<p class="std_text"> ${order.note1_webkit | carriage_returns} </p>
    %endif
    </div>

    <h1 style="clear:both;">${quotation and _(u'Quotation N°') or _(u'Order N°') } ${order.name}</h1>

    <table class="basic_table" width="100%">
        <tr>
            <td>${quotation and _("Date Ordered") or _("Quotation Date")}</td>
            <td>${_("Your Reference")}</td>
            <td>${_("Salesman")}</td>
            <td>${_('Payment Term')}</td>
            <td>${_('Incoterm')}</td>
        </tr>
        <tr>
            <td>${formatLang(order.date_order, date=True)}</td>
            <td>${order.client_order_ref or ''}</td>
            <td>${order.user_id and order.user_id.name or ''}</td>
            <td>${order.payment_term and order.payment_term.name or ''}</td>
            <td>${order.incoterm and order.incoterm.name or ''}</td>
        </tr>
    </table>

    <table class="list_sale_table" width="100%" style="margin-top: 20px;">
        <thead>
            <tr>
                <th>${_("Description")}</th>
                <th>${_("VAT")}</th>
                <th class="amount">${_("Quantity")}</th>
                <th class="amount">${_("Unit Price")}</th>
                <th class="amount">${_("Disc.(%)")}</th>
                <th class="amount">${_("Price")}</th>
            </tr>
        </thead>
        <tbody>
            %for line in order.order_line:
                <tr class="line">
                    <td style="text-align:left;">${ line.name }</td>
                    <td>${ ', '.join([tax.name or '' for tax in line.tax_id]) }</td>
                    <td class="amount">${ formatLang(line.product_uos and line.product_uos_qty or line.product_uom_qty) } ${ line.product_uos and line.product_uos.name or line.product_uom.name }</td>
                    <td class="amount">${formatLang(line.price_unit)}</td>
                    <td class="amount">${formatLang(line.discount, digits=get_digits(dp='Sale Price'))}</td>
                    <td class="amount">${formatLang(line.price_subtotal, digits=get_digits(dp='Sale Price'))}&nbsp;${order.pricelist_id.currency_id.symbol}</td>
                </tr>
                %if line.notes:
                    <tr class="line">
                        <td colspan="6" class="note" style="font-style:italic; font-size: 10; border-top: thin solid  #ffffff ; text-align:left; padding:20;">${line.notes  | carriage_returns}</td>
                    </tr>
                %endif
            %endfor
        </tbody>
        <tfoot>
            <tr>
                <td colspan="4" style="border-style:none"/>
                <td style="border-style:none"><b>${_("Net Total:")}</b></td>
                <td class="amount" style="border-style:none">${formatLang(order.amount_untaxed, get_digits(dp='Sale Price'))} ${order.pricelist_id.currency_id.symbol}</td>
            </tr>
            <tr>
                <td colspan="4" style="border-style:none"/>
                <td style="border-style:none"><b>${_("Taxes:")}</b></td>
                <td class="amount"style="border-style:none">${formatLang(order.amount_tax, get_digits(dp='Sale Price'))} ${order.pricelist_id.currency_id.symbol}</td>
            </tr>
            <tr>
                <td colspan="4" style="border-style:none"/>
                <td style="border-style:none"><b>${_("Total:")}</b></td>
                <td class="amount" style="border-style:none">${formatLang(order.amount_total, get_digits(dp='Sale Price'))} ${order.pricelist_id.currency_id.symbol}</td>
            </tr>
        </tfoot>
    </table>
    <p style="margin-top: 20px;">${order.payment_term and order.payment_term.note or '' | carriage_returns}</p>

    %if order.note :
    	<p class="std_text">${order.note | carriage_returns}</p>
    %endif
    %if order.note2_webkit :
    	<p class="std_text">${order.note2_webkit | carriage_returns}</p>
    %endif

    <p style="page-break-after: always"/>
    <br/>
    %endfor
</body>
</html>
