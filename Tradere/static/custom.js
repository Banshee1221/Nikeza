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
        $('input:checkbox.groupcheckbox').each(function () {
            var sThisVal = (this.checked ? $(this).val() : "");
            console.log(sThisVal);
        });
    }
}