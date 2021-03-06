# -*- coding: utf-8 -*-
# Copyright (c) 2018, earthians and contributors
# For license information, please see license.txt
from __future__ import unicode_literals
import frappe

from frappe import _
import datetime, json
from frappe.desk.form import assign_to
from frappe.utils import get_datetime, cint, getdate, nowdate

@frappe.whitelist()
def make_project_estimate(opportunity):
	if not opportunity:
		return False

	if frappe.db.exists("Opportunity", opportunity):
		opportunity_doc = frappe.get_doc("Opportunity", opportunity)
	else:
		return False

	new_estimate = frappe.new_doc("eSS Project Estimate")
	new_estimate.opportunity = opportunity_doc.name
	new_estimate.estimation_date = nowdate()
	new_estimate.customer_or_lead_name = opportunity_doc.customer_name
	new_estimate.total_item_cost = 0
	for opportunity_item in opportunity_doc.items:
		new_item = new_estimate.append('items')
		new_item.item_code = opportunity_item.item_code
		new_item.qty = opportunity_item.qty
		new_item.item_name = opportunity_item.item_name
		new_item.uom = opportunity_item.uom
		new_item.price_list_rate = frappe.get_value('Item Price', {'item_code': opportunity_item.item_code, 'price_list': "Standard Buying"}, 'price_list_rate')
		new_item.amount = new_item.price_list_rate * new_item.qty
		new_estimate.total_item_cost += new_item.amount
	new_estimate.total_estimated_cost = new_estimate.total_item_cost
	return new_estimate.as_dict()

@frappe.whitelist()
def make_quotation(opportunity):
	if not opportunity:
		return False

	if frappe.db.exists("Opportunity", opportunity):
		opportunity_doc = frappe.get_doc("Opportunity", opportunity)
	else:
		return False

	new_quote = frappe.new_doc("Quotation")
	new_quote.opportunity = opportunity_doc.name
	new_quote.estimation_date = nowdate()
	new_quote.quotation_to = "Lead"
	new_quote.lead = opportunity_doc.lead
	new_quote.customer_or_lead_name = opportunity_doc.customer_name
	new_quote.estimated_cost_of_boq_items = opportunity_doc.estimated_cost_of_boq_items
	new_quote.estimated_expenses = opportunity_doc.estimated_expenses
	new_quote.estimated_activity_costs = opportunity_doc.estimated_activity_costs
	new_quote.total_estimated_cost = opportunity_doc.total_estimated_cost
	for opportunity_item in opportunity_doc.items:
		new_item = new_quote.append('items')
		new_item.item_code = opportunity_item.item_code
		new_item.qty = opportunity_item.qty
		new_item.item_name = opportunity_item.item_name
		new_item.uom = opportunity_item.uom
		new_item.description = opportunity_item.item_name
	return new_quote.as_dict()
