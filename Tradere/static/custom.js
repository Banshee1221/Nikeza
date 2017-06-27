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
