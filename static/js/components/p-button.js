export default {
    data() {
        return {
            // comProps: {
            //     label: 'Button',
            //     class: 'btn btn-primary btn-large blue-btn',
            //     disabled: false,
            // }
            defaultClass: 'btn btn-primary btn-large',
        }
    },
    mounted() {
        console.log('mounted button');
    },
    created() {
        console.log('created button');
        if ( !this.comProps.hasOwnProperty('class') || this.comProps.class === '') {
            this.defaultClass += ' blue-btn'
        }
    },
    methods: {
        handleClick() {
            console.log("Button clicked 1");
            this.$emit('button-clicked');
        }
    },
    props:['comProps', 'globalProps'],
    template: `
        <button 
            type="button"
            :class="this.defaultClass + ' ' + this.comProps.class"
            :disabled="this.comProps.disabled"
            @click="handleClick"
        ><span>{{this.comProps.label}}</span></button>
    `,
}