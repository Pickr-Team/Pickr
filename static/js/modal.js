class ConfirmSystem {
  constructor(options = {}) {
    const defaultOptions = {
      confirmModalId: 'confirmModal',
      resultModalId: 'resultModal',
      autoCloseDelay: 2000,
      dangerClass: 'btn-danger'
    }

    this.config = {...defaultOptions, ...options}
    this.initModals()
    this.bindGlobalEvents()
  }

  initModals() {
    this.confirmModal = new bootstrap.Modal(`#${this.config.confirmModalId}`)
    this.resultModal = new bootstrap.Modal(`#${this.config.resultModalId}`)

    this.confirmButton = document.querySelector(
      `#${this.config.confirmModalId} .confirm-button`
    )
  }

  bindGlobalEvents() {
    // 全局捕获未处理的Promise异常
    window.addEventListener('unhandledrejection', (event) => {
      this.showResult(false, event.reason?.message || '操作失败')
    })
  }

  async confirm(params = {}) {
    return new Promise((resolve) => {
      const {
        title = '确认操作',
        message = '确定要执行此操作吗？',
        confirmText = '确定',
        cancelText = '取消',
        danger = false
      } = params

      // 更新Modal内容
      const modal = document.getElementById(this.config.confirmModalId)
      modal.querySelector('.modal-title').textContent = title
      modal.querySelector('.confirm-message').textContent = message
      modal.querySelector('.confirm-button').textContent = confirmText
      modal.querySelector('[data-bs-dismiss="modal"]').textContent = cancelText

      // 设置危险操作样式
      if (danger) {
        modal.querySelector('.confirm-button').classList.add(this.config.dangerClass)
      } else {
        modal.querySelector('.confirm-button').classList.remove(this.config.dangerClass)
      }

      // 清理旧事件
      const cleanUp = () => {
        this.confirmButton.replaceWith(this.confirmButton.cloneNode(true))
        this.confirmButton.removeEventListener('click', onConfirm)
        this.confirmModal._element.removeEventListener('hide.bs.modal', onCancel)
      }

      const onConfirm = async () => {
        this.confirmButton.disabled = true
        this.confirmButton.innerHTML = `
          <span class="spinner-border spinner-border-sm"></span>
          ${confirmText}
        `

        try {
          resolve(true)
        } finally {
          cleanUp()
          this.confirmModal.hide()
          setTimeout(() => {
            this.confirmButton.disabled = false
            this.confirmButton.textContent = confirmText
          }, 500)
        }
      }

      const onCancel = () => {
        resolve(false)
        cleanUp()
      }

      this.confirmButton.addEventListener('click', onConfirm)
      this.confirmModal._element.addEventListener('hide.bs.modal', onCancel)
      this.confirmModal.show()
    })
  }

  showResult(isSuccess, message, options = {}) {
    const {
      autoClose = true,
      closeDelay = this.config.autoCloseDelay
    } = options

    const iconElement = document.querySelector(`#${this.config.resultModalId} .result-icon i`)
    const messageElement = document.querySelector(`#${this.config.resultModalId} .result-message`)

    // 设置图标和颜色
    iconElement.className = isSuccess
      ? 'bi bi-check-circle-fill text-success'
      : 'bi bi-x-circle-fill text-danger'

    messageElement.textContent = message

    if (autoClose) {
      setTimeout(() => {
        this.resultModal.hide()
      }, closeDelay)
    }

    this.resultModal.show()
  }
}

// 导出单例实例
export const modalSystem = new ConfirmSystem()