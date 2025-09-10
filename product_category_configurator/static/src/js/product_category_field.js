/** @odoo-module */

import { serializeDateTime } from "@web/core/l10n/dates";
import { x2ManyCommands } from "@web/core/orm_service";
import { WarningDialog } from "@web/core/errors/error_dialogs";
import { useService } from "@web/core/utils/hooks";
import { patch } from "@web/core/utils/patch";
import { CategoryConfiguratorDialog } from "./category_configurator_dialog/category_configurator_dialog";
import { CategoryProductField } from "./widget/category_product_widget";

patch(CategoryProductField.prototype, {

    setup() {
        super.setup(...arguments);

        this.dialog = useService("dialog");
        this.notification = useService("notification");
        this.orm = useService("orm");
    },

    _editCategoryConfiguration() {
        super._editCategoryConfiguration(...arguments);
        // Product Category Configurator
        this._openCategoryConfigurator(true);
    },

    get isConfigurableCategory() {
        return this.props.record.data.is_category_configurable;
    },

    async _openCategoryConfigurator(edit=false) {
        // console.log(':::::::::::::::')
        const ProductRecord = this.props.record.model.root;
        // console.log(":::::ProductRecord",ProductRecord)
        // console.log('\n\n ---------ProductRecord---------', ProductRecord)

        // if (edit) {
        //     /**
        //      * no_variant and custom attribute don't need to be given to the configurator for new
        //      * products.
        //      */
        //     console.log('Is Edit Mode')
        // }
        // console.log("::::12",this.props.record)
        // console.log("::::34",this.props)
        this.dialog.add(CategoryConfiguratorDialog, {
            productId: this.props.record.resId,
            productTemplateId: this.props.record.resId,
            categoryId: this.props.record.data.asset_type_id[0],
            companyId: this.props.record.currentCompanyId,
            edit: edit,
            save: async () => {
                console.log('\n\n ++++++++++++Configurator Save++++++++++++', this.props)
                // await applyProduct(this.props.record, mainProduct);
            },
            discard: () => {
                console.log('\n\n ++++++++++++Configurator Discard++++++++++++', this.props)
            },
        });
    },
});
