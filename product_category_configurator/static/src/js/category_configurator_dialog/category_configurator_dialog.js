/** @odoo-module **/
import { Component, onWillStart, useState, useSubEnv } from "@odoo/owl";
import { Dialog } from '@web/core/dialog/dialog';
import { _t } from "@web/core/l10n/translation";
import { rpc } from "@web/core/network/rpc";

export class CategoryConfiguratorDialog extends Component {
    static components = { Dialog };
    static template = 'category_configurator.dialog';
    static props = {
        productId: Number,
        productTemplateId: Number,
        categoryId: Number,
        companyId: Number,
        edit: { type: Boolean, optional: true },
        save: Function,
        discard: Function,
        close: Function, // This is the close from the env of the Dialog Component
    };
    static defaultProps = {
        edit: true,
    }

    setup() {
        this.title = _t("Custom Fields");
        this.env.dialogData.dismiss = !this.props.edit && this.props.discard.bind(this);
        this.state = useState({
            categories: [], // Get category and it's items lines
            selected_item_value_ids: [], // Store updated item values
            selectedItemIds: [], // Store selected values
            warning_msg: false // Visible warning if value not filled
        });
        this.getOptionValuesUrl = '/product_category_configurator/get_option_values';
        this.getValuesUrl = '/product_category_configurator/get_values';
        this.createProductItemUrl = '/product_category_configurator/create_product_item';

        useSubEnv({
            mainProductTmplId: this.props.productTemplateId,
            categoryId: this.props.categoryId,
            addCategoryProduct: this._addCategoryProduct.bind(this),
            updateItemGenerateFieldValue: this._updateItemGenerateFieldValue.bind(this),
            updateItemSelectedFieldValue: this._updateSelectedItemValue.bind(this),
        });

        onWillStart(async () => {
            const {
                categories,
                selectedItemIds,
            } = await this._loadData(this.props.edit);
            this.state.categories = categories;
            this.state.selectedItemIds = selectedItemIds;
        });
    }

    //--------------------------------------------------------------------------
    // Data Exchanges
    //--------------------------------------------------------------------------

    async _loadData(onlyMainProduct) {
        return rpc(this.getValuesUrl, {
            product_id: this.props.productId,
            product_template_id: this.props.productTemplateId,
            category_id: this.props.categoryId,
            company_id: this.props.companyId,
        });
    }

    async _createProductItem(category, item_ids) {
        return rpc(this.createProductItemUrl, {
            product_id: this.props.productId,
            category_id: category.category_id,
            item_ids: item_ids,
        });
    }

    //--------------------------------------------------------------------------
    // Handlers
    //--------------------------------------------------------------------------

    /**
     * Change the value of `selected_attribute_value_ids` on the given PTAL in the product.
     *
     * @param {Number} itemId - The item id, as a `item.generate.field` id.
     * @param {String} value - The item value id, as a `item.generate.field.value` name.
     * @param {String} field_type - Whether field type can be selected.
     */
    async _updateSelectedItemValue(itemId, value, field_type) {
        // when field_type 'option' get option object value
        if (field_type === 'option') {
            const optionRecord = await rpc(this.getOptionValuesUrl, {
                item_id: itemId,
                value: parseInt(value),
            });
            value = optionRecord;
        }
        // Find index of existing item in selectedItemIds
        const existingitem = this.state.selectedItemIds.findIndex(i => i.item_id === itemId);
        if (existingitem !== -1) {
            // Update existing item
            this.state.selectedItemIds[existingitem].value = value;
            this.state.selectedItemIds[existingitem].field_type = field_type;
        } else {
            // Add new item
            this.state.selectedItemIds.push({
                'item_id': itemId,
                'value': value,
                'field_type': field_type
            });
        }
        // console.log("Updated selectedItemIds:", this.state.selectedItemIds);
    }

    /**
     * Change the value of `selected_attribute_value_ids` on the given PTAL in the product.
     *
     * @param {Number} productlId - The product template id, as a `product.template` id.
     * @param {Number} itemId - The item id, as a `item.generate.field` id.
     * @param {String} value - The item value id, as a `item.generate.field.value` name.
     * @param {String} field_type - Whether field type can be selected.
     */
    async _updateItemGenerateFieldValue(productId, itemId, value, field_type) {
        // Find index of existing item in selected_item_value_ids
        const existingitem = this.state.selected_item_value_ids.findIndex(i => i.item_id === itemId);
        if (existingitem !== -1) {
            // Update existing item
            this.state.selected_item_value_ids[existingitem].value = value;
            this.state.selected_item_value_ids[existingitem].field_type = field_type;
        } else {
            // Add new item
            this.state.selected_item_value_ids.push({
                'product_id': productId,
                'item_id': itemId,
                'value': value,
                'field_type': field_type
            });
        }
        // console.log("Updated selected_item_value_ids:", this.state.selected_item_value_ids);
    }

    /**
     * Update in the state the custom value of the selected Item.
     *
     * @param {Event} event
     */
    updateItemValue(event) {
        // Extract Item ID and new value
        const itemId = parseInt(event.target.id); // Ensure item ID is an integer
        var newValue = event.target.value;

        let field_type = 'text';
        if (event.target.type === 'number') {
            field_type = 'integer';
        } else if (event.target.type === 'select-one') {
            field_type = 'option';
        } else if (event.target.type === 'checkbox') {
            field_type = event.target.type;
            var newValue = event.target.checked ? true : false;
        }

        // Updated selected value to the backend
        this.env.updateItemSelectedFieldValue(
            itemId, newValue, field_type
        );
        // Updated item field value to the backend
        this.env.updateItemGenerateFieldValue(
            this.props.productId, itemId, newValue, field_type
        );

        // // update product name onchange options and input
        // this.updateProductName();
    }

    // /**
    //  * Update configurator product name on change values.
    //  */
    // updateProductName() {
    //     for (const category of this.state.categories) {
    //         let values = [];
    //         for (const item of category.item_ids) {
    //             const selected = this.state.selectedItemIds.find((s) => s.item_id === item.id);
    //             if (selected && selected.value !== undefined && selected.value !== '') {
    //                 if (item.field_type === "option") {
    //                     const option = item.options.find((opt) => opt.id == selected.value);
    //                     if (option) values.push(option.name);
    //                 } else if (item.field_type === "checkbox") {
    //                     values.push(selected.value ? "True" : "False");
    //                 } else {
    //                     values.push(selected.value);
    //                 }
    //             }
    //         }
    //         category.product_name = values.join(" ");
    //     }
    // }

    /**
     * Confirm the current combination(s).
     *
     * @return {undefined}
     */
    async _addCategoryProduct(template) {
        // console.log('IS Call onConfirm', this.state);
        // Find missing required fields
        let missingFields = [];
        for (const category of this.state.categories) {
            for (const item of category.item_ids) {
                if (item.required === 'true' || item.required === true) { // Check if the field is required
                    let iteminput = document.getElementById(item.id);
                    let value = iteminput ? iteminput.value.trim() : null;

                    // Handle different input types
                    if (iteminput) {
                        if (iteminput.type === "checkbox") {
                            if (!iteminput.checked) {
                                missingFields.push(item.label);
                            }
                        } else if (iteminput.tagName === "SELECT") {
                            if (!value || value === "none") {
                                missingFields.push(item.label);
                            }
                        } else if (iteminput.type === "number") {
                            if (value === "" || isNaN(value)) {
                                missingFields.push(item.label);
                            }
                        } else {
                            // Default case (text inputs, etc.)
                            if (!value) {
                                missingFields.push(item.label);
                            }
                        }

                        // Highlight missing fields
                        if (missingFields.includes(item.label)) {
                            iteminput.style.backgroundColor = "rgba(255, 0, 0, 0.2)"; // Light red background
                            iteminput.style.border = "2px solid red"; // Add red border
                        } else {
                            // Reset styling if the field is correctly filled
                            iteminput.style.backgroundColor = "";
                            iteminput.style.border = "";
                        }
                    }
                }
            }
        }

        // If there are missing fields, show a warning
        if (missingFields.length > 0) {
            var msg = `Please fill the following required fields:\n ${missingFields.join(', ')}`
            // Set warning in confgurator
            this.state.warning_msg = msg
            // Popup Warning
            // alert(msg);
            return;
        }


        // Proceed with product creation if all required fields are filled
        for (const category of this.state.categories) {
            try {
                const productId = await this._createProductItem(category, this.state.selected_item_value_ids);
                category.id = parseInt(productId);
            } catch (e) {
                // e.message.data.message
                alert(`Error: ${JSON.stringify(e.message)}`);
                return;
            }
        }
        // Close configurator
        this.props.close();

        // Reload the current view to reflect updated data
        window.location.reload();
    }

    /**
     * Discard the modal.
     */
    onDiscard() {
        if (!this.props.edit) {
            this.props.discard(); // clear the line
        }
        this.props.close();
    }
}
