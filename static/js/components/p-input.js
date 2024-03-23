export default {
    mounted() {
        console.log('mounted input');
    },
    created() {
        console.log('created input');
        if ( !this.comProps.hasOwnProperty('ruleValidate') ) {
            this.comProps.ruleValidate = ''
        }
        if ( !this.comProps.hasOwnProperty('type') ) {
            this.comProps.type = ''
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
        <div class="mb-3 p-input" :class="{'form-group': comProps.type == '', 'input-group': comProps.type == 'inputGroup'}" >
            <label for="long_url" class="form-label"><strong>{{comProps.label}}</strong></label>
            <input class="form-control" 
                type="text" 
                v-model="comProps.val"
                :placeholder="comProps.placeHolder"
                :disabled="comProps.disabled"
                @blur="handleBlur"
            ><span v-if="comProps.type == 'inputGroup'" class="input-group-text" id="basic-addon2">Copy</span>
            
        </div>
    `,
}