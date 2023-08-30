export function get_border_spinner() {
    return '<div class="spinner-border" role="status">\n' +
        '  <span class="visually-hidden">Loading...</span>\n' +
        '</div>'
}

export function get_btn_loading(min, max) {
  return '<span class="spinner-border spinner-border-sm" role="status" aria-hidden="true"></span>\n' +
      '  <span class="visually-hidden">Loading...</span>';
}

export function get_end_point() {
    return import.meta.env.VITE_BE_URL
}

export function convert_space_to_dash(str) {
    return str.replaceAll(' ', '-')
}

export function remove_protocol(url) {
    return url.replace(/(^\w+:|^)\/\//, '');
}
