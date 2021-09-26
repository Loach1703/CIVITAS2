Vue.component("blog-display", {
    data: function () {
        return {
            title: "",
            author: "",
            time: "",
            id: "",
            text: "",
            total: 0
        }
    },
    created: function () {
        this.id = get_parameter_value("id");
        if (isNaN(this.id) || this.id == null) {
            document.title = "开发日志 - 古典社会模拟 CIVITAS2";
        }
        else {
            this.get_blog();
        }
    },
    methods: {
        get_blog: function () {
            var vm = this;
            axios({
                method: "get",
                url: "https://api.trickydeath.xyz/getblog/",
                withCredentials: true,
                params: {
                    id: this.id,
                },
            })
            .then(function (response) {
                var json_str_data = response.data.data;
                vm.total = json_str_data.total;
                document.title = "开发日志" + vm.id + json_str_data.title + " - 古典社会模拟 CIVITAS2";
                vm.title = json_str_data.title;
                vm.author = json_str_data.author;
                vm.text = json_str_data.text;
            })
            .catch(function (error) {
                console.log(error);
            })
        }
    },
    template: `
    <div class="main-double">
        <div>
            <a v-if="id == 1">没有上一篇 </a>
            <a v-bind:href="'?id='+(Number(id)-1)" v-else> 上一篇</a>
            <a v-if="id == total"> 没有下一篇</a>
            <a v-bind:href="'?id='+(Number(id)+1)" v-else> 下一篇</a>
        <div>
        <p class="main-char">{{ title }}</p>
        <p class="author">作者：{{ author }} <br>{{ time }}</p>
        <div v-html="text"></div>
    </div>
    `
})