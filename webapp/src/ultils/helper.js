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

export function get_favicon_by_domain(domain, size=64) {
    domain = domain.replace('https://', '')
    domain = domain.replace('http://', '')
    return 'https://t1.gstatic.com/faviconV2?client=SOCIAL&type=FAVICON&fallback_opts=TYPE,SIZE,URL&url=https://'+domain+'&size='+size
}