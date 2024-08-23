this is a database to track and manage item orders, useage, deliveries, and statements

from an item database, tables to track and organize orders generated, vendors, deliveries, and invoices are logged and stored

based on real world user input, item orders are generated per vendor according to predefined order points

upon delivery confirmation(user confirms items, quantities, received, and invoice details), 
item tables are updated, invoices are stored with vendor name, delivery date, invoice ID, amount due, and due date

delivery statements then generated in .csv, .pdf, or spreadsheet format according to the user need

to do:
[complete gui or google sheets API0] web-based python flask interface, store to cloud

complete main module logic

confirm report outputs and useability

test for missing functionality

create user access rules: employee-general, employee-count, manager, owner

  employee general: view stock/ 86 reports, submit item requests
  
  employee count: input real world inventory count
  
  owner: view and download all reports and tables, all access except place or generate orders
  
  manager: all access, place and create orders, receive/ override delivery
