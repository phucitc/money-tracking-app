<template>
  <main>
      <div class="container">
            <input v-model="this.email">
          <button @click="this.validate_dulieu_dauvao()">Submit</button>
      </div>
  </main>
</template>
<script>
    export default {
        data() {
            return {
                email: '',
            }
        },
        setup() {

        },
        created() {
            // Sau khi website load xong
            //alert("Xin chao");
            // a di lay thu
            //
            // b lay thu tu a di giao c
            // het code
        },
        mounted() {
            //alert("Xin chao 111");
            //
        },
        updated() {
            //  duoc chay khi co su thay doi ve html
        },
        methods: {
            //dinh nghia nhieu cong cong viec can lam
            validate_dulieu_dauvao() {
                // email
                // ho ten
                if ( this.email === '') {
                    alert("email ko hop le")
                } else {
                    alert("email hop le")
                    // gui du lieu len server
                }

            }
        }
    }
</script>