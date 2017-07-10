function checkAll(ele) {
    var checkboxes = document.getElementsByClassName('groupcheckbox');
    if (ele.checked) {
        for (var i = 0; i < checkboxes.length; i++) {
            if (checkboxes[i].type == 'checkbox') {
                checkboxes[i].checked = true;
            }
        }
    } else {
        for (var i = 0; i < checkboxes.length; i++) {
            console.log(i);
            if (checkboxes[i].type == 'checkbox') {
                checkboxes[i].checked = false;
            }
        }
    }
}

function stopCluster() {
    if (confirm("Are you sure you want to stop these jobs?")) {
        var selected = [];
        $('#clusterForm input:checked').each(function () {
            selected.push($(this).attr('value'));
            console.log(selected);
        });
        $.ajax({
            type: "POST",
            contentType: "application/json; charset=utf-8",
            url: "/queue",
            data: JSON.stringify(selected),
            success: function (data) {
                console.log(data);
            },
            dataType: "json"
        });
    }
}

function arr_diff(a1, a2) {
    var a = [], diff = [];
    for (var i = 0; i < a1.length; i++) {
        a[a1[i]] = true;
    }
    for (var i = 0; i < a2.length; i++) {
        if (a[a2[i]]) {
            delete a[a2[i]];
        } else {
            a[a2[i]] = true;
        }
    }
    for (var k in a) {
        diff.push(k);
    }
    return diff;
}

$(document).ready(function () {
    $('select').material_select();

    $('#html1')
        .jstree({
            "plugins": ["json_data", "checkbox"],
            "core": {
                "themes": {
                    'name': 'proton',
                    'responsive': true
                },
                "check_callback": true,
                data: {
                    "type": 'GET',
                    "url": "/_new",
                    data: function (node) {
                        return {
                            'id': (node.id == '#') ? 'root' : node.id
                        };
                    },
                    "success": function (new_data) {
                        console.log(new_data);
                        return new_data;
                    }
                }
            }
        });
});

function update_values() {
    $.getJSON("/_updateQueue", function (data) {
        if ($(".clustertable").length > 0) {
            var existingServers = [];
            var newServers = [];
            $.each($(".clustertable"), function (index, value) {
                existingServers.push(value.id);
            });
            $.each(data.j.servers, function (index, value) {
                $("#" + value.id + "_id").html(value.id);
                $("#" + value.id + "_nm").html(value.name);
                $("#" + value.id + "_st").html(value.status);
                newServers.push(value.id)
            });
            console.log(existingServers);
            console.log(newServers);
            var diffList = arr_diff(existingServers, newServers);
            console.log(diffList);
            if (diffList.length > 0) {
                $.each(diffList, function (index, value) {
                    if (jQuery.inArray(value, existingServers) !== -1) {
                        console.log("removing element");
                        $("#" + value).remove()
                    }
                    else {
                        console.log("adding element");
                        $.each(data.j.servers, function (index, innerValue) {
                            if (innerValue.id === value) {
                                $("#tableContent").append(
                                    '<tr id=' + innerValue.id + ' class="clustertable"><td><input class="groupcheckbox" value=' + innerValue.id + ' type="checkbox" id=' + innerValue.id + '_id /><label for=' + innerValue.id + '_id >&nbsp;</label></td><td id=' + innerValue.id + '_id>' + innerValue.id + '</td><td id=' + innerValue.id + '_nm>' + innerValue.name + '</td><td id=' + innerValue.id + '_st>' + innerValue.status + '</td></tr>'
                                );
                            }
                        });

                    }
                })
            }
        }
    });
}
