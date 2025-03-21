let _type, _id, _parentNode;
const $confirmModal = $('#confirmModal')
const $confirmModalBody = $('#confirmModal-body')
const $secondConfirmModal = $('#secondConfirmModal')
const $secondConfirmModalBody = $('#secondConfirmModal-body')
const $loading = $('#modal-loading')
const $confirmText = $('#confirm-text')
const $confirmBtn = $('#confirm-btn')

const operationHandlers = {
    del: {
        confirmText: 'Are you sure to delete?',
        execute: () => sendRequest({
            url: `/delete/${_type}/${_id}`,
            method: 'GET',
            successHandler: (response) => {
                if (response.success) _parentNode.remove()
                return response.message
            }
        })
    },
    resetSystem: {
        confirmText: 'Are you sure to reset system?',
        execute: () => sendRequest({
            url: '/manager/resetting',
            method: 'GET',
            successHandler: (response) => {
                if (response.code === 200) {
                    setTimeout(() => location.reload(), 1000)
                }
                return response.message || response.error
            }
        })
    },
    resetPwd: {
        confirmText: 'Confirm password reset?',
        execute: () => sendRequest({
            url: "/manager/reset_password",
            method: "POST",
            data: {
                user_id: window.appState.params.user_id,
                user_type: window.appState.params.user_type
            },
            successHandler: () => 'Password has been reset to 123456.'
        })
    }
}

function sendRequest({url, method, data, successHandler}) {
    return $.ajax({
        url,
        method,
        data,
        success: (response) => {
            const message = successHandler(response)
            showResultModal(message, !response.error && response.code !== 400)
        },
        error: (xhr) => {
            showResultModal(`Operation failed: ${xhr.status} ${xhr.statusText}`, false)
        }
    })
}

function setLoadingState(isLoading = true) {
    $loading.toggle(isLoading)
    $confirmText.text(isLoading ? 'Loading' : 'Confirm')
    $confirmBtn.prop('disabled', isLoading)
}

function showResultModal(message, isSuccess = true) {
    $confirmModal.modal('hide')
    $secondConfirmModalBody
        .text(message)
        .css('color', isSuccess ? 'white' : 'var(--accent)')
    $secondConfirmModal.modal('show')
}

function initModal(type, params = {}) {
    $confirmBtn.prop('disabled', false);
    $confirmText.text('Confirm');
    $loading.hide();

    window.appState = { operation: type, params }
    const handler = operationHandlers[type]

    if (!handler) return console.error('Unknown operation')

    $confirmModalBody.text(handler.confirmText)
    setLoadingState(false)
    $confirmModal.modal('show')
}

function del(type, id, parentDivClass) {
    if (type === 'topic') return

    _type = type
    _id = id
    const button = document.querySelector(`button[data-${type}-id="${id}"]`)
    _parentNode = parentDivClass ? button.closest(parentDivClass) : button.closest('tr')

    initModal('del')
}

$('#confirmModal .btn-danger').on('click', () => {
    setLoadingState()
    operationHandlers[window.appState.operation]?.execute()
})

$('#secondConfirmModal .btn-secondary').on('click', () => {
    $secondConfirmModal.modal('hide')
})