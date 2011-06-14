function choose_new_group_manager() {
    $(".manager_checkbox").show();
}

function new_group_manager_selected(group_slug, group_member_pk) {
    $.ajax({
        url     : '/group/' + group_slug + '/settings/set_new_group_manager/' + group_member_pk + '/',
        type    : 'post',
        success : function (response) {
            window.location = "";
        }
    });
}