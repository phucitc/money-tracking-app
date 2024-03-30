export default {
    data() {
        return {
            item: {},
            bsModal: null
        }
    },
    created() {
        this.bsModal = $('#' + this.comProps.id);
    },
    updated() {
        this.bsModal = $('#' + this.comProps.id);
        this.item = this.comProps.item;
        this.handleOpenModal();

    },
    mounted() {
        this.bsModal.on('hidden.bs.modal', () => {
            console.log('hidden modal')
            this.comProps.isVisible = false;
        })
    },
    watch: {
        comProps: {
            handler: function (newVal) {
                console.log(newVal.isVisible)
                if ( newVal.isVisible ) {
                    this.handleOpenModal();
                } else {
                    this.handleCloseModal();
                }
            },
            deep: true
        }
    },
    methods: {
        handleCloseModal() {
            this.comProps.isVisible = false;
            this.bsModal.modal('hide');

        },
        handleOpenModal() {
            this.comProps.isVisible = true;
            this.bsModal.modal('show');
        }
    },
    props:['comProps', 'globalProps'],
    template: `
    <div class="modal fade" :id="comProps.id" 
        :class="{'on': comProps.isVisible, 'off': !comProps.isVisible}"
        tabindex="-1" :aria-labelledby="comProps.modalLabel" aria-hidden="true">
        <div class="modal-dialog">
            <div class="modal-content">
                <div class="modal-header">
                    <h5 class="modal-title">Edit: {{item.public_id}}</h5>
                    <button type="button" class="btn-close" data-bs-dismiss="modal" aria-label="Close"></button>
                </div>
                <div class="modal-body">
                    <p>Modal body text goes here.</p>
                </div>
                <div class="modal-footer">
                    <button type="button" class="btn btn-secondary" @click="handleCloseModal">Close</button>
                    <button type="button" class="btn btn-primary">Save changes</button>
                </div>
            </div>
        </div>
    </div>
    `
}