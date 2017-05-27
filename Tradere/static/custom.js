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
            console.log(i)
            if (checkboxes[i].type == 'checkbox') {
                checkboxes[i].checked = false;
            }
        }
    }
}

document.getElementById("stopcluster").onclick = function () {
    document.getElementById("clusterForm").submit();
}

setInterval(function() {
  update_values()
}, 5000);