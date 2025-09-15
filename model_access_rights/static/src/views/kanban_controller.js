/** @odoo-module */
/**
 * This file will used to hide the selected options from the list view
 */
import { KanbanController } from '@web/views/kanban/kanban_controller';
import { patch} from "@web/core/utils/patch";
import {useService} from "@web/core/utils/hooks";
const {onWillStart} = owl;
patch(KanbanController.prototype,{
/**
 * This function will used to hide the selected options from the Kanban view
 */
    setup() {
        super.setup(...arguments);
        this.rpc = useService("rpc")
        this.user = useService("user");
        onWillStart(async () => {
            var self = this
            var result;
            result = await this.env.services.orm.silent.call(
                "access.right",
                "hide_buttons",
            );
            for (var i = 0; i < result.length; i++) {
                var group = result[i].module + "." + result[i].group_name
                if (result[i].models.includes(self.props.resModel)) {
                    if (result[i].restriction_type == "group") {
                        if (await self.user.hasGroup(group)) {
                            if (!self.user.isAdmin) {
                                if (result[i].is_create_or_update) {
                                    self.props.archInfo.activeActions.create = false
                                    self.props.archInfo.activeActions.edit = false
                                }
                                if (result[i].is_delete) {
                                    self.props.archInfo.activeActions.delete = false
                                }
                            }
                        }
                    } else {
                        if (await self.user.userId == result[i].user[0]) {
                            if (!self.user.isAdmin) {
                                if (result[i].is_create_or_update) {
                                    self.props.archInfo.activeActions.create = false
                                    self.props.archInfo.activeActions.edit = false
                                }
                                if (result[i].is_delete) {
                                    self.props.archInfo.activeActions.delete = false
                                }
                            }
                        }
                    }

                }
            }
        });
    }
});
