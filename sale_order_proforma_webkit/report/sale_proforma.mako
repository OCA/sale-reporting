## -*- coding: utf-8 -*-
<html>
<head>
    <style type="text/css">
        ${css}

.list_main_table {
    border:thin solid #E3E4EA;
    text-align:center;
    border-collapse: collapse;
}
table.list_main_table {
    margin-top: 20px;
}
.list_main_headers {
    padding: 0;
}
.list_main_headers th {
    border: thin solid #000000;
    padding-right:3px;
    padding-left:3px;
    background-color: #EEEEEE;
    text-align:center;
    font-size:12;
    font-weight:bold;
}
.list_main_table td {
    padding-right:3px;
    padding-left:3px;
    padding-top:3px;
    padding-bottom:3px;
}
.list_main_lines,
.list_main_footers {
    padding: 0;
}
.list_main_footers {
    padding-top: 15px;
}
.list_main_lines td,
.list_main_footers td,
.list_main_footers th {
    border-style: none;
    text-align:left;
    font-size:12;
    padding:0;
}
.list_main_footers th {
    text-align:right;
}

td .total_empty_cell {
    width: 77%;
}
td .total_sum_cell {
    width: 13%;
}

.nobreak {
    page-break-inside: avoid;
}
caption.formatted_note {
    text-align:left;
    border-right:thin solid #EEEEEE;
    border-left:thin solid #EEEEEE;
    border-top:thin solid #EEEEEE;
    padding-left:10px;
    font-size:11;
    caption-side: bottom;
}
caption.formatted_note p {
    margin: 0;
}

.main_col1 {
    width: 40%;
}
td.main_col1 {
    text-align:left;
}
.main_col2,
.main_col3,
.main_col4,
.main_col6 {
    width: 10%;
}
.main_col5 {
    width: 7%;
}
td.main_col5 {
    text-align: center;
    font-style:italic;
    font-size: 10;
}
.main_col7 {
    width: 13%;
}

.list_bank_table {
    text-align:center;
    border-collapse: collapse;
    page-break-inside: avoid;
    display:table;
}

.act_as_row {
   display:table-row;
}
.list_bank_table th {
    background-color: #EEEEEE;
    text-align:left;
    font-size:12;
    font-weight:bold;
    padding-right:3px;
    padding-left:3px;
}
.list_bank_table td {
    text-align:left;
    font-size:12;
    padding-right:3px;
    padding-left:3px;
    padding-top:3px;
    padding-bottom:3px;
}


.list_tax_table {
}
.list_tax_table td {
    text-align:left;
    font-size:12;
}
.list_tax_table th {
}
.list_tax_table thead {
    display:table-header-group;
}


.list_total_table {
    border:thin solid #E3E4EA;
    text-align:center;
    border-collapse: collapse;
}
.list_total_table td {
    border-top : thin solid #EEEEEE;
    text-align:left;
    font-size:12;
    padding-right:3px;
    padding-left:3px;
    padding-top:3px;
    padding-bottom:3px;
}
.list_total_table th {
    background-color: #EEEEEE;
    border: thin solid #000000;
    text-align:center;
    font-size:12;
    font-weight:bold;
    padding-right:3px
    padding-left:3px
}
.list_total_table thead {
    display:table-header-group;
}


.no_bloc {
    border-top: thin solid  #ffffff ;
}

.right_table {
    right: 4cm;
    width:"100%";
}

.std_text {
    font-size:12;
}

tfoot.totals tr:first-child td{
    padding-top: 15px;
}

th.date {
    width: 90px;
}

td.amount, th.amount {
    text-align: right;
    white-space: nowrap;
}
.header_table {
    text-align: center;
    border: 1px solid lightGrey;
    border-collapse: collapse;
}
.header_table th {
    font-size: 12px;
    border: 1px solid lightGrey;
}
.header_table td {
    font-size: 12px;
    border: 1px solid lightGrey;
}

td.date {
    white-space: nowrap;
    width: 90px;
}

td.vat {
    white-space: nowrap;
}
.address .recipient {
    font-size: 12px;
    position: absolute;
    left: 101mm;
    width: 83mm;
}
.address .shipping {
    margin-left: 0px;
    margin-right: 500px;
}

    </style>
</head>
<body>
    <%page expression_filter="entity"/>
    <%
    def carriage_returns(text):
        return text.replace('\n', '<br />')
    %>

    <%def name="address(partner, commercial_partner=None)">
        <%doc>
            XXX add a helper for address in report_webkit module as this won't be suported in v8.0
        </%doc>
        <% company_partner = False %>
        %if commercial_partner:
            %if commercial_partner.id != partner.id:
                <% company_partner = commercial_partner %>
            %endif
        %elif partner.parent_id:
            <% company_partner = partner.parent_id %>
        %endif

        %if company_partner:
            <tr><td class="name">${company_partner.name or ''}</td></tr>
            <tr><td>${partner.title and partner.title.name or ''} ${partner.name}</td></tr>
            <% address_lines = partner.contact_address.split("\n")[1:] %>
        %else:
            <tr><td class="name">${partner.title and partner.title.name or ''} ${partner.name}</td></tr>
            <% address_lines = partner.contact_address.split("\n") %>
        %endif
        %for part in address_lines:
            % if part:
                <tr><td>${part}</td></tr>
            % endif
        %endfor
    </%def>

    %for inv in objects:
    <% setLang(inv.partner_id.lang) %>
    <div class="address">
        <table class="recipient">
          ${address(partner=inv.partner_id)}
        </table>
      %if inv.partner_shipping_id:
        <table class="shipping">
          <tr><td class="address_title">${_("Shipping address:")}</td></tr>
          ${address(partner=inv.partner_shipping_id)}
        </table>
      %endif
    </div>
    <p class="std_text">
        ${_("Identification number : ")} ${inv.partner_id.vat or ''}
    </p>
    <h1 style="clear: both; padding-top: 20px;">
            ${_("PRO-FORMA")} ${inv.name or ''}
    </h1>
    <h3  style="clear: both; padding-top: 20px;">
        ${_("Subject : ")} ${inv.client_order_ref or ''}
    </h3>

    <table class="basic_table" width="100%">
        <tr>
            <th class="date">${_("Invoice Date")}</td>
            <th class="date">${_("Due Date")}</td>
            <th style="text-align:center;width:120px;">${_("Responsible")}</td>
            <th style="text-align:center">${_("Payment Term")}</td>
            <th style="text-align:center">${_("Our reference")}</td>
        </tr>
        <tr>
            <td class="date">${formatLang(inv.date_order, date=True)}</td>
            <td class="date"></td>
            <td style="text-align:center;width:120px;">${inv.user_id and inv.user_id.name or ''}</td>
            <td style="text-align:center">${inv.payment_term and inv.payment_term.note or ''}</td>
            <td style="text-align:center">${inv.name or ''}</td>
        </tr>
    </table>

    <div>
    </div>

    <table class="list_main_table" width="100%" style="margin-top: 20px;">
      <thead>
        <tr>
          <th class="list_main_headers" style="width: 100%">
            <table style="width:100%">
              <tr>
                <th class="main_col1">${_("Description")}</th>
                <th class="amount main_col2">${_("Qty")}</th>
                <th class="amount main_col3">${_("UoM")}</th>
                <th class="amount main_col4">${_("Unit Price")}</th>
                <th class="main_col5">${_("Taxes")}</th>
                <th class="amount main_col6">${_("Disc.(%)")}</th>
                <th class="amount main_col7">${_("Net Sub Total")}</th>
              </tr>
            </table>
          </th>
        </tr>
      </thead>
      <tbody>
        %for line in inv.order_line:
          <tr>
            <td class="list_main_lines" style="width: 100%">
              <div class="nobreak">
                <table style="width:100%">
                  <tr>
                    <td class="main_col1">${line.name.replace('\n','<br/>') or '' | n}</td>
                    <td class="amount main_col2">${formatLang(line.product_uom_qty or 0.0,digits=get_digits(dp='Account'))}</td>
                    <td class="amount main_col3">${line.product_uos and line.product_uos.name or ''}</td>
                    <td class="amount main_col4">${formatLang(line.price_unit)}</td>
                    <td class="main_col5">${ ', '.join([tax.description or tax.name for tax in line.tax_id])}</td>
                    <td class="amount main_col6">${line.discount and formatLang(line.discount, digits=get_digits(dp='Account')) or ''} ${line.discount and '%' or ''}</td>
                    <td class="amount main_col7">${formatLang(line.price_subtotal, digits=get_digits(dp='Account'))} ${inv.currency_id.symbol}</td>
                  </tr>
                </table>
              </div>
            </td>
          </tr>
        %endfor
      </tbody>
      <tfoot class="totals">
        <tr>
          <td class="list_main_footers" style="width: 100%">
            <div class="nobreak">
              <table style="width:100%">
                <tr>
                  <td class="total_empty_cell"/>
                  <th>
                    ${_("Net :")}
                  </th>
                  <td class="amount total_sum_cell">
                    ${formatLang(inv.amount_untaxed, digits=get_digits(dp='Account'))} ${inv.currency_id.symbol}
                  </td>
                </tr>
                <tr>
                  <td class="total_empty_cell"/>
                  <th>
                    ${_("Taxes:")}
                  </th>
                  <td class="amount total_sum_cell">
                    ${formatLang(inv.amount_tax, digits=get_digits(dp='Account'))} ${inv.currency_id.symbol}
                  </td>
                </tr>
                <tr>
                  <td class="total_empty_cell"/>
                  <th>
                    ${_("Total:")}
                  </th>
                  <td class="amount total_sum_cell">
                    <b>${formatLang(inv.amount_total, digits=get_digits(dp='Account'))} ${inv.currency_id.symbol}</b>
                  </td>
                </tr>
              </table>
            </div>
          </td>
        </tr>
      </tfoot>
    </table>
        <br/>

        <br/>
        <br/>
        <h4>
                ${_("Thank you for your prompt payment")}
        </h4>
        <br/>
    <br/>
    %if inv.note :
        <p class="std_text">${inv.note | carriage_returns}</p>
    %endif
    %if inv.fiscal_position :
        <br/>
        <p class="std_text">
        ${inv.fiscal_position.note | n}
        </p>
    %endif
    %if inv != objects[-1]:
        <p style="page-break-after:always"/>
    %endif
    %endfor
</body>
</html>
