/*
注册登录Vue组件

组件1
名称:login-and-register
用途:注册与登录共用同一组件，方便方法复用
props:{
    type:类型，login/register
}
data:{
    email:邮箱
    account:账号
    password:密码
    repeat_password:重复密码
    login_tips:错误提示
}
methods:{
    login:注册
    register:登录
}
*/

Vue.component("login-and-register", {
    props: ["type"],
    data: function () {
        return {
            email: "",
            account: "",
            password: "",
            repeat_password: "",
            login_tips: ""
        }
    },
    methods: {
        login: function () {
            var vm = this;
            var post_data = new URLSearchParams();
            post_data.append("username",this.account);
            post_data.append("password",this.password);
            axios({
                method: "post",
                url: "https://api.trickydeath.xyz/login/",
                withCredentials: true,
                data: post_data
            })
            .then(function (response) {
                vm.login_tips = response.data.message;
                if (response.data.status == 1) {
                    window.location.assign("index.html");
                }
            })
            .catch(function (error) {
                console.log(error);
            })
        },
        register: function () {
            var vm = this;
            var post_data = new URLSearchParams();
            post_data.append("email",this.email);
            post_data.append("username",this.account);
            post_data.append("password",this.password);
            post_data.append("repeat_password",this.repeat_password);
            axios({
                method: "post",
                url: "https://api.trickydeath.xyz/register/",
                withCredentials: true,
                data: post_data
            })
            .then(function (response) {
                vm.login_tips = response.data.message;
                if (response.data.status == 1) {
                    vm.login()
                }
            })
            .catch(function (error) {
                console.log(error);
            })
        }
    },
    template:`
    <div>
        <template v-if="type == 'login'">
            <p class="login-main-char">登录CIVITAS2</p>
            <div class="login-inputdiv">
                <input type="text" class="form-control login-input" v-model="account" placeholder="账号（暂时使用用户名登录，不是邮箱）">
                <input type="password" class="form-control login-input" v-model="password" placeholder="密码">
                <button class="btn btn-block btn-primary" v-on:click="login">登录</button>
                <p class="login-message">{{ login_tips }}</p>
            </div>
            <a href="register.html">还没有账号？点击这里注册</a>
            <a href="#password_reset.html">忘记密码</a>
        </template>
        <template v-else-if="type == 'register'">
            <p class="login-main-char">注册CIVITAS2</p>
            <div class="login-inputdiv">
                <input type="text" class="form-control login-input" v-model="email" placeholder="邮箱">
                <input type="text" class="form-control login-input" v-model="account" placeholder="用户名">
                <input type="password" class="form-control login-input" v-model="password" placeholder="密码">
                <input type="password" class="form-control login-input" v-model="repeat_password" placeholder="再次输入密码">
                <button class="btn btn-block btn-primary" v-on:click="register">注册</button>
                <p class="login-message">{{ login_tips }}</p>
            </div>
            <a href="login.html">已有账号？点击这里登录</a>
            <div class="form-check login-tiantang">
                <label class="form-check-label">
                    <input type="radio" class="form-check-input" name="optradio">我同意接受CIVITAS服务条款<br>并遵守严格禁止一人多身份的底线
                </label>
            </div>
        </template>
	</div>
    `
})