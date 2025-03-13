let _type, _id, _parentNode;
const $confirmModal = $('#confirmModal')
const $secondConfirmModal = $('#secondConfirmModal')
const $secondConfirmModalBody = $('#secondConfirmModal-body')
const $loading = $('#modal-loading')
const $confirmText = $('#confirm-text')
const $confirmBtn = $('#confirm-btn')

window.appState = {
    operation: '',
    params: {}
};

function del(type, id, parentDivClass) {
    if (type === 'topic') return

    _type = type;
    _id = id;

    const button = document.querySelector(`button[data-${type}-id="${id}"]`);
    _parentNode = parentDivClass ? button.closest(parentDivClass) : button.closest('tr');

    $confirmBtn.prop('disabled', false);
    $confirmText.text('Confirm');
    $loading.hide();
    window.appState.operation = 'del';
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
            $secondConfirmModalBody.text('Deletion failed: ' + response.status + ' ' + response.statusText).css('color', 'var(--accent)');
            $secondConfirmModal.modal('show');
        }
    });
}

function resetSystem() {
    $loading.show()
    $confirmText.text('Loading')
    $confirmBtn.prop('disabled', true)

    $.ajax({
        url: '/manager/resetting',
        method: 'GET',
        success: function (response) {
            $confirmModal.modal('hide')
            if (response.code === 200) {
                $secondConfirmModalBody.text(response.message).css('color', 'white');
                setTimeout(() => {
                    location.reload();
                }, 1000)
            } else {
                $secondConfirmModalBody.text(response.error).css('color', 'var(--accent)');
            }
            $secondConfirmModal.modal('show');
        },
        error: function (response) {
            $confirmModal.modal('hide')
            $secondConfirmModalBody.text(response.status + ' ' + response.statusText).css('color', 'var(--accent)');
            $secondConfirmModal.modal('show');
        }
    })
}

function resetPassword() {
    $loading.show()
    $confirmText.text('Loading')
    $confirmBtn.prop('disabled', true)

    $.ajax({
        url: "/manager/reset_password",
        type: "POST",
        data: {
            user_id: window.appState.params.user_id,
            user_type: window.appState.params.user_type
        },
        success: function (response) {
            $confirmModal.modal('hide')
            $secondConfirmModalBody.text('Password has been reset to 123456.');
            $secondConfirmModal.modal('show');
        },
        error: function (response) {
            $confirmModal.modal('hide')
            $secondConfirmModalBody.text(response.status + ' ' + response.statusText).css('color', 'var(--accent)');
            $secondConfirmModal.modal('show');
        }
    });
}


function showResultModal() {
    if (window.appState.operation === 'del') {
        confirmDel()
    } else if (window.appState.operation === 'resetSystem') {
        resetSystem()
    } else if (window.appState.operation === 'resetPwd') {
        resetPassword()
    } else {
        console.log('error')
    }
}

$('#confirmModal .btn-danger').on('click', showResultModal);

$('#secondConfirmModal .btn-secondary').on('click', function () {
    $secondConfirmModal.modal('hide');
});