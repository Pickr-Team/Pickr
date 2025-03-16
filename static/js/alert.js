/**
 * alert animation
 */
function customAlert() {
    const $alert = $('#my-alert');
    $alert.removeClass('down up');
    $alert.addClass('down');
    let i = setTimeout(function () {
        $alert.removeClass('down').addClass('up');
        i = null
    }, 4000);
}

/**
 * custom pickr alert to replace bom build-in alert
 * @param msg
 * @param type success, danger, warning
 */
function pickrAlert(msg, type = 'success') {
    const alert = document.querySelector('#pickr-alert')
    alert.classList.remove('down', 'up', 'alert-success', 'alert-danger', 'alert-warning')
    alert.classList.add(`alert-${type}`)
    alert.classList.add('down')
    alert.innerText = msg
    let i = setTimeout(function () {
        alert.classList.remove('down')
        alert.classList.add('up')
        i = null
    }, 4000);
}