export default {
    data() {
        return {
            cssClass: 'text-center '
        }
    },
    mounted() {
    },
    created() {
        if ( this.comProps.type == 'success' ) {
            this.cssClass += ' text-success';
        } else if ( this.comProps.type == 'error' ) {
            this.cssClass += 'text-danger';
        } else if ( this.comProps.type == 'warning' ) {
            this.cssClass += ' text-warning';
        }

        if ( this.comProps.hasOwnProperty('cssClass') ) {
            this.cssClass += " " + this.comProps.cssClass;
        }
    },
    methods: {
        handleClickClose() {
            this.comProps.isVisible = false;
        }
    },
    props:['comProps', 'globalProps'],
    template: `
        <div class="alert alert-dismissible"
            :class="cssClass"
            :class="{'d-none': !comProps.isVisible, '': comProps.isVisible}"
            role="alert">
            {{comProps.message}}
            <button type="button" class="btn-close" @click="handleClickClose"></button>
        </div>
    `,
}