let _type, _id, _parentNode;
const $confirmModal = $('#confirmModal')
const $secondConfirmModal = $('#secondConfirmModal')
const $secondConfirmModalBody = $('#secondConfirmModal-body')
const $loading = $('#modal-loading')
const $confirmText = $('#confirm-text')
const $confirmBtn = $('#confirm-btn')

function del(type, id, parentDivClass) {
    if (type === 'topic') return

    _type = type;
    _id = id;

    const button = document.querySelector(`button[data-${type}-id="${id}"]`);
    _parentNode = parentDivClass ? button.closest(parentDivClass) : button.closest('tr');

    $confirmBtn.prop('disabled', false);
    $confirmText.text('Confirm');
    $loading.hide();

    $confirmModal.modal('show')
    $('#confirmModal-body').text(`Are you sure to delete?`);
}

function confirmDel() {
    $loading.show()
    $confirmText.text('Loading')
    $confirmBtn.prop('disabled', true)

    $.ajax({
        url: `/delete/${_type}/${_id}`,
        type: 'GET',
        success: function (response) {
            $confirmModal.modal('hide')
            if (response.success) {
                _parentNode.remove();
                $secondConfirmModalBody.text(response.message).css('color', 'white');
            } else {
                $secondConfirmModalBody.text(response.message).css('color', 'var(--accent)');
            }
            $secondConfirmModal.modal('show');
        },
        error: function (response) {
            $confirmModal.modal('hide')
            const msg = xhr.responseJSON?.message || "Deletion failed.";
            $secondConfirmModalBody.text(msg).css('color', 'var(--accent)');
            $secondConfirmModal.modal('show');
        }
    });
}

$('#confirmModal .btn-danger').on('click', confirmDel);

$('#secondConfirmModal .btn-secondary').on('click', function () {
    $secondConfirmModal.modal('hide');
});