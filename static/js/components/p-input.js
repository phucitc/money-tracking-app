export default {
    data() {
        return {
        }
    },
    mounted() {
    },
    created() {
        if ( !this.comProps.hasOwnProperty('ruleValidate') ) {
            this.comProps.ruleValidate = ''
        }
        if ( !this.comProps.hasOwnProperty('type') ) {
            this.comProps.type = ''
        }
        if ( !this.comProps.hasOwnProperty('copyText') ) {
            this.comProps.copyText = 'Copy'
        }

    },
    methods: {
        handleBlur() {
            if ( this.comProps.val !== undefined ) {
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
        },
        handleClickIcon() {
            this.$emit('button-icon-clicked');

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
            ><span v-if="comProps.type == 'inputGroup'" 
                class="input-group-text pointer"
                @click="handleClickIcon"
                id="basic-addon2">{{comProps.copyText}}</span>
            
        </div>
    `,
}