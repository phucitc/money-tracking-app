class Helper {
    static getBaseUrl() {
        return 'http://localhost:3000';
    }

    isValidURL(urlString) {
        const urlRegex = new RegExp(/^(http|https):\/\/[^ "]+$/);
        return urlRegex.test(urlString);
    }

    isEmpty(input) {
        if ( input == undefined || input == '' ) {
            return true;
        }
    }

    getMetaContent(name) {
        return document.querySelector(`meta[name=${name}]`).content;
    }

}
