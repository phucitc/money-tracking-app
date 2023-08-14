export function get_border_spinner() {
    return '<div class="spinner-border" role="status">\n' +
        '  <span class="visually-hidden">Loading...</span>\n' +
        '</div>'
}

export function get_btn_loading(min, max) {
  return '<span class="spinner-border spinner-border-sm" role="status" aria-hidden="true"></span>\n' +
      '  <span class="visually-hidden">Loading...</span>';
}