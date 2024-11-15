/**
 * custom alert
 */
function customAlert() {
    const $alert = $('#my-alert');
    $alert.removeClass('down up');
    $alert.addClass('down');
    setTimeout(function () {
        $alert.removeClass('down').addClass('up');
    }, 4000);
}

/**
 * close confirm modal
 * @param button close button
 */
/*function CustomConfirm(content) {
    const pickrConfirm = document.querySelector('.pickr-confirm')
    pickrConfirm.style.display = 'block'
    const pcContent = document.querySelector('.pickr-confirm .pc-content')
    pcContent.innerHTML = content
}
function closePickrConfirm(button) {
    let pickrConfirm = button.parentNode.parentNode;
    pickrConfirm.style.display = 'none';
}
function confirmYes(button) {
    let pickrConfirm = button.parentNode.parentNode;
    pickrConfirm.style.display = 'none';
    return true
}*/
