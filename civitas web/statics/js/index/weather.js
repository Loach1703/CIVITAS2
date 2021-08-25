/*
天气Vue组件

组件1
名称:skill-show
用途:整体大框架
props:{
    prop:{
        uid:对应用户的uid
        username:对应用户的用户名
    },
    type:类型，index/people
}
data:{
    skills:参考接口文档getskills的data项
}

组件2
名称:skill-detail
用途:显示某个大类技能
props:{
    skill:参考接口文档getskills的data项中其中一项
}
data:{
    close_show:折叠/展开的显示
    skill_dict:门槛对应表
}
*/

Vue.component("weather-detail", {
    props: ["prop","city"],
    data: function () {
        return {
            weather_svg_dict: {"晴":"qingtian.svg","多云":"duoyun.svg","阴":"yintian.svg","小雨":"xiaoyu.svg","大雨":"dayu.svg","小雪":"xiaoxue.svg","大雪":"daxue.svg","台风":"taifeng.svg"},
            weather: "",
            temperature: "",
            rain_num: "",
            day: ""
        }
    },
    created: function () {
        axios({
            method: "get",
            url: "https://api.trickydeath.xyz/getweather/",
            withCredentials: true,
            params: {
                city: this.city,
                day: this.prop.total_day
            },
        })
        .then(function (response) {
            vm.weather = response.data.data.weather;
            vm.temperature = response.data.data.temperature;
            vm.rain_num = response.data.data.rain_num;
            vm.day = response.data.data.day;
        })
        .catch(function (error) {
            console.log(error);
        })
    },
    template:`
    <div>
        <p class="location">位于京兆尹，长安县 今天是{{ prop.season }}的第{{ day }}天</p>
        <span v-bind:src="'civitas/svg/weather/'+weather_svg_dict[prop.weather]"></span>
        <p class="weather-main">今日天气：<strong>{{ weather }}</strong> 温度：<strong>{{ temperature.toFixed(2) }}</strong>摄氏度 降水量：<strong>{{ rain_num.toFixed(2) }}</strong>mm</p>
    </div>
    `
})