/*
 * File Name : PaymentLineTableView.js
 *
 * Copyright (C) 2017 Gaston TJEBBES g.t@majerti.fr
 * Company : Majerti ( http://www.majerti.fr )
 *
 * This software is distributed under GPLV3
 * License: http://www.gnu.org/licenses/gpl-3.0.txt
 *
 */
import Mn from 'backbone.marionette';
import PaymentDepositView from './PaymentDepositView.js';
import PaymentLineModel from '../models/PaymentLineModel.js';
import PaymentLineCollectionView from './PaymentLineCollectionView.js';
import PaymentLineFormView from './PaymentLineFormView.js';
import PaymentLineView from './PaymentLineView.js';
import Radio from 'backbone.radio';
import {strToFloat} from '../../math.js';

const PaymentLineTableView = Mn.View.extend({
    template: require('./templates/PaymentLineTableView.mustache'),
    regions: {
        lines: '.paymentlines',
        modalRegion: '.payment-line-modal-container',
        deposit: ".deposit",
    },
    ui: {
        btn_add: ".btn-add"
    },
    events: {
        "click @ui.btn_add": "onLineAdd"
    },
    childViewEvents: {
        'line:edit': 'onLineEdit',
        'line:delete': 'onLineDelete',
        'destroy:modal': 'render'

    },
    initialize(options){
        this.collection = options['collection'];
        this.message = Radio.channel('message');
        this.facade = Radio.channel('facade');
        this.totalmodel = this.facade.request('get:totalmodel');
        this.depositmodel = new PaymentLineModel(
            {
                description: "Facture d'acompte",
                date: "À la commande",
                amount: this.collection.depositAmount(this.model.get('deposit'))
            }
        );
        this.listenTo(
            this.totalmodel,
            'change:ttc',
            this.updateDeposit.bind(this)
        );
        this.listenTo(
            this.facade,
            'update:payment_lines',
            this.updateDeposit.bind(this)
        );
        this.listenTo(
            this.model,
            'change:deposit',
            this.updateDeposit.bind(this)
        )
        this.edit = this.getOption('edit');
    },
    onLineAdd(){
        var model = new PaymentLineModel(
            {
                task_id: this.model.get('id'),
                order: this.collection.getMaxOrder() - 1,
            }
        );
        this.showPaymentLineForm(model, "Ajouter une échéance", false);
    },
    onLineEdit(childView){
        this.showPaymentLineForm(childView.model, "Modifier l'échéance", true);
    },
    showPaymentLineForm: function(model, title, edit){
        let edit_amount = false;
        if (this.edit){
            edit_amount = true;
            if (edit){
                if (model.isLast()){
                    edit_amount = false;
                }
            }
        }
        var form = new PaymentLineFormView(
            {
                model: model,
                title: title,
                destCollection: this.collection,
                edit: edit,
                edit_amount: edit_amount,
                show_date: this.getOption('show_date'),
            });
        this.showChildView('modalRegion', form);
    },
    onDeleteSuccess(){
        this.message.trigger('success', "Vos données ont bien été supprimées");
    },
    onDeleteError(){
        this.message.trigger(
            'error',
            "Une erreur a été rencontrée lors de la suppression de cet élément"
        );
    },
    onLineDelete(childView){
        var result = window.confirm(
            "Êtes-vous sûr de vouloir supprimer cette échéance ?"
        );
        if (result){
            childView.model.destroy(
                {
                    success: this.onDeleteSuccess.bind(this),
                    error: this.onDeleteError.bind(this),
                }
            );
        }
    },
    templateContext(){
        return {
            show_date: this.getOption('show_date'),
            show_add: this.getOption('edit'),
        };
    },
    updateDeposit(){
        console.log("PaymentLineTableView.updateDeposit");
        var deposit = this.model.get('deposit');
        var deposit_amount = this.collection.depositAmount(deposit);
        this.depositmodel.set({amount: deposit_amount});
        this.updateLines()
    },
    updateLines(){
        console.log("PaymentLineTableView.updateLines");
        var payment_times = this.model.get('payment_times');
        var deposit = this.model.get('deposit');

        payment_times = strToFloat(payment_times);
        if (payment_times > 0){
            this.collection.genPaymentLines(payment_times, deposit);
        } else {
            this.collection.updateSold(deposit);
        }
    },
    showDeposit(){
        var view = new PaymentDepositView({
            model:this.depositmodel,
            show_date: this.getOption('show_date'),
        });
        this.showChildView('deposit', view);
    },
    showLines(){
        this.showChildView(
            'lines',
            new PaymentLineCollectionView({
                collection: this.collection,
                show_date: this.getOption('show_date'),
                edit: this.getOption('edit'),
            })
        );
    },
    onRender(){
        this.showDeposit();
        this.showLines();
    },
});
export default PaymentLineTableView;
