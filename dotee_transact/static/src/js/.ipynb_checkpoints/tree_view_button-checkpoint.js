odoo.define('dotee_transact.tree_view_button', function (require){
"use strict";

var core = require('web.core');
var ListView = require('web.ListView');
var QWeb = core.qweb;

// ListView.include({       

//         render_buttons: function($node) {
//                 var self = this;
//                 this._super($node);
//                     this.$buttons.find('.o_list_tender_button_create').click(this.proxy('tree_view_action'));
//         },

//         tree_view_action: function () {   
//             return this.do_action({
//                 type: "ir.actions.act_window",
//                 name: 'report',
//                 res_model: 'res.partner',
// //                 domain: domain,
//                 views: [
//                     [false, "list"],
//                     [false, "form"],
//                 ],
//                 target: "current",
//             });
//         } 

// });
let ListController = require('web.ListController');

let JsTocallWizard = ListController.include({
      renderButtons: function($node){
            this._super.apply(this, arguments);
            if (this.$buttons) {
                this.$buttons.on('click', '.o_button_to_call_wizard', this.proxy('action_to_call_wizard'));
                this.$buttons.appendTo($node);
            }
      },
      action_to_call_wizard: function(event) {
            event.preventDefault();
            var self = this;
            self.do_action({
                name: "Open a wizard",
                type: 'ir.actions.act_window',
                res_model: 'res.partner.debtor.wizard',
                view_type: 'form',
                views: [[false, 'form']],
                target: 'new',
             });

      },
});
});