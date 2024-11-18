/**
 * alert animation
 */
function customAlert() {
    const $alert = $('#my-alert');
    $alert.removeClass('down up');
    $alert.addClass('down');
    setTimeout(function () {
        $alert.removeClass('down').addClass('up');
    }, 4000);
}
