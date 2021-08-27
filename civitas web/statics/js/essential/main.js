/*
加载主vm
注意：所有页面都需要调用此vm
*/

var main_vm;

function load_main_vm(uid) {
    //随机事件组件
    Vue.component("ranevent-modal", {
        props: ["prop"],
        methods: {
            hide_modal: function (){
                this.$emit("hide_modal");
            },
            next_modal: function (url){
                this.$emit("hide_modal");
                this.$emit("next_modal",url);
            }
        },
        template:`
        <div class="modal fade" id="ranevent" aria-hidden="true">
            <div class="modal-dialog">
                <div class="modal-content modal-background">
                    <div class="modal-body bottomline-dashed">
                      <p class="modal-title-text">{{ prop.title }}</p>
                      <button type="button" class="close" data-dismiss="modal" aria-hidden="true">&times;</button>
                    </div>
                    <div class="modal-body bottomline-dashed">
                        <p>{{ prop.statement }}</p>
                    </div>
                    <div class="modal-body ranevent-option" v-if="prop.type == 'work_strategy'">
                        <button 
                            type="button" 
                            class="btn" 
                            v-on:click="hide_modal" 
                            v-for="index in [...Array(prop.option_text.length).keys()]">
                            <img v-bind:src="'civitas/icon/work/Strategy_'+index+'.png'"/>
                            {{ prop.option_text[index] }}
                        </button>
                    </div>
                    <div class="modal-body ranevent-option" v-else>
                        <button 
                            type="button" 
                            class="btn" 
                            v-on:click="hide_modal" 
                            v-for="index in [...Array(prop.option_text.length).keys()]">
                            <img v-bind:src="'civitas/icon/choices/Choice_'+index+'.png'"/>
                            {{ prop.option_text[index] }}
                        </button>
                    </div>
                </div>
            </div>
        </div>`
    })
    main_vm = new Vue({
        el: "#main",
        data: {
            uid: uid,
            user_detail: {},
            someone_uid: undefined,
            someone_detail: {},
            speech_input: "",
            ranevent_prop: {
                title:"",
                statement:"",
                type:"normal",
                option_text:[]
            },
            date_prop: {
                total_day:0,
                time:0,
                year:0,
                season:"春天",
                day: 0
            }
        },
        created: function () {
            var vm = this;
            //获取自己的信息
            axios({
                method: "get",
                url: "https://api.trickydeath.xyz/getuserdetail/",
                withCredentials: true,
                params: {
                    uid: this.uid,
                },
            })
            .then(function (response) {
                vm.user_detail.username = response.data.data.username;
            })
            .catch(function (error) {
                console.log(error);
            })
            this.user_detail.city = "长安";
            this.user_detail.uid = this.uid;
            //如果有uid的话，拿到uid对应用户信息
            try {
                this.someone_uid = get_parameter_value("uid");
            }
            catch (error) {}
            if (this.someone_uid != undefined) {
                axios({
                    method: "get",
                    url: "https://api.trickydeath.xyz/getuserdetail/",
                    withCredentials: true,
                    params: {
                        uid: this.someone_uid,
                    },
                })
                .then(function (response) {
                    vm.someone_detail.username = response.data.data.username;
                })
                .catch(function (error) {
                    console.log(error);
                })
                this.someone_detail.uid = this.someone_uid;
            }
            //获取日期信息
            axios({
                method: "get",
                url: "https://api.trickydeath.xyz/getdate/",
                withCredentials: true,
            })
            .then(function (response) {
                vm.date_prop = response.data.data;
            })
            .catch(function (error) {
                console.log(error);
            })
        },
        methods: {
            show_ranevent_modal: function () {
                $("#ranevent").modal("show");
            },
            hide_ranevent_modal: function () {
                $("#ranevent").modal("hide");
            },
            get_ranevent: function (url) {
                var vm = this;
                axios({
                    method: "get",
                    url: url,
                    withCredentials: true,
                })
                .then(function (response) {
                    var json_str_data = response.data.data;
                    vm.prop = json_str_data.ranevent_data;
                })
                .catch(function (error) {
                    console.log(error);
                });
            },
            speech_refresh: function () {
                this.$refs.speech_popular.get_speech_popular();
                this.$refs.speech_main.page_turn(1);
            }
        }
    })
}