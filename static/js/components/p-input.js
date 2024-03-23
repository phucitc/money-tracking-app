export default {
    mounted() {
        console.log('mounted input');
    },
    created() {
        console.log('created input');
        if ( !this.comProps.hasOwnProp('ruleValidate') ) {
            this.comProps.ruleValidate = ''
        }

    },
    methods: {
        handleBlur() {
            if ( this.comProps.val !== undefined ) {
                console.log("AAA")
                console.log(this.comProps.val)
                this.comProps.val = this.comProps.val.trim();
            }

            if ( this.comProps.ruleValidate !== '' ) {
                if ( this.comProps.ruleValidate == 'url' ) {
                    if ( !this.globalProps.helper.isValidURL(this.comProps.val) ) {
                        this.comProps.error = true;
                    } else {
                        this.comProps.error = false;
                    }
                }
            }
        }
    },
    props:['comProps', 'globalProps'],
    template: `
        <div class="form-group mb-3">
            <label for="long_url" class="form-label"><strong>{{this.comProps.label}}</strong></label>
            <input class="form-control" 
                type="text" 
                v-model="this.comProps.val"
                :placeholder="this.comProps.placeHolder"
                :disabled="this.comProps.disabled"
                @blur="handleBlur"
            >
        </div>
    `,
}