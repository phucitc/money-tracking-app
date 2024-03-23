export default {
    mounted() {
        console.log('mounted button');
    },
    created() {
        console.log('created button');
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
            type="button" class="btn btn-primary btn-large blue-btn"
            :disabled="this.comProps.disabled"
            @click="handleClick"
        ><span>{{this.comProps.label}}</span></button>
    `,
}