// # indexでリンク先を変更する処理
function goToUrl() {
    var selectElement = document.getElementsByName("application_name")[0];
    var url = selectElement.value;
    if (url != '') {
        window.location = url;
    }
}