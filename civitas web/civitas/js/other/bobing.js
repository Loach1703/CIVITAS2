function randomNum(minNum,maxNum){ 
    switch(arguments.length){ 
        case 1: 
            return parseInt(Math.random()*minNum+1,10); 
        break; 
        case 2: 
            return parseInt(Math.random()*(maxNum-minNum+1)+minNum,10); 
        break; 
            default: 
                return 0; 
            break; 
    } 
}

Array.prototype.duplicate=function() {  
    var tmp = [];  
    this.concat().sort().sort(function(a,b){  
        if(a==b && tmp.indexOf(a) === -1) tmp.push(a);  
    });  
    return [tmp.length,tmp[0]];  
}  

Vue.component("bo-bing", {
    data: function () {
        return {
            level: "无",
            number: [0,0,0,0,0,0]
        }
    },
    created: function () {
    },
    methods: {
        bb: function () {
            for (var i = 0; i < 6; i++) {
                this.$set(this.number,i,randomNum(1,6));
            }
            n = [this.number[0],this.number[1],this.number[2],this.number[3],this.number[4],this.number[5]]
            n.sort()
            console.log(n)
            if (n.toString() == [1,1,4,4,4,4].toString()) {
                this.level = "状元-状元插金花"
            }
            else if (n.toString() == [4,4,4,4,4,4].toString() || n.toString() == [1,1,1,1,1,1].toString()) {
                this.level = "状元-六杯红"
            }
            else if (n.toString() == [2,2,2,2,2,2].toString() || n.toString() == [3,3,3,3,3,3].toString() || n.toString() == [5,5,5,5,5,5].toString() || n.toString() == [6,6,6,6,6,6].toString()) {
                this.level = "状元-六杯黑"
            }
            else if (n.slice(0,5).toString() == [4,4,4,4,4].toString() || n.slice(1,6).toString() == [4,4,4,4,4].toString()) {
                this.level = "状元-五王"
            }
            else if (n.slice(0,5).toString() == [1,1,1,1,1].toString() || n.slice(1,6).toString() == [1,1,1,1,1].toString()) {
                this.level = "状元-五子登科"
            }
            else if (n.slice(0,5).toString() == [2,2,2,2,2].toString() || n.slice(1,6).toString() == [2,2,2,2,2].toString()) {
                this.level = "状元-五子登科"
            }
            else if (n.slice(0,5).toString() == [3,3,3,3,3].toString() || n.slice(1,6).toString() == [3,3,3,3,3].toString()) {
                this.level = "状元-五子登科"
            }
            else if (n.slice(0,5).toString() == [5,5,5,5,5].toString() || n.slice(1,6).toString() == [5,5,5,5,5].toString()) {
                this.level = "状元-五子登科"
            }
            else if (n.slice(0,5).toString() == [6,6,6,6,6].toString() || n.slice(1,6).toString() == [6,6,6,6,6].toString()) {
                this.level = "状元-五子登科"
            }
            else if (n.slice(0,4).toString() == [4,4,4,4].toString() || n.slice(1,5).toString() == [4,4,4,4].toString() || n.slice(2,6).toString() == [4,4,4,4].toString()) {
                this.level = "状元"
            }
            else if (n.toString() == [1,2,3,4,5,6].toString()) {
                this.level = "对堂"
            }
            else if (n.slice(0,3).toString() == [4,4,4].toString() || n.slice(1,4).toString() == [4,4,4].toString() || n.slice(2,5).toString() == [4,4,4].toString() || n.slice(3,6).toString() == [4,4,4].toString()) {
                this.level = "三红"
            }
            else if (n.slice(0,4).toString() == [1,1,1,1].toString() || n.slice(1,5).toString() == [1,1,1,1].toString() || n.slice(2,6).toString() == [1,1,1,1].toString()) {
                this.level = "四进"
            }
            else if (n.slice(0,4).toString() == [2,2,2,2].toString() || n.slice(1,5).toString() == [2,2,2,2].toString() || n.slice(2,6).toString() == [2,2,2,2].toString()) {
                this.level = "四进"
            }
            else if (n.slice(0,4).toString() == [3,3,3,3].toString() || n.slice(1,5).toString() == [3,3,3,3].toString() || n.slice(2,6).toString() == [3,3,3,3].toString()) {
                this.level = "四进"
            }
            else if (n.slice(0,4).toString() == [5,5,5,5].toString() || n.slice(1,5).toString() == [5,5,5,5].toString() || n.slice(2,6).toString() == [5,5,5,5].toString()) {
                this.level = "四进"
            }
            else if (n.slice(0,4).toString() == [6,6,6,6].toString() || n.slice(1,5).toString() == [6,6,6,6].toString() || n.slice(2,6).toString() == [6,6,6,6].toString()) {
                this.level = "四进"
            }
            else if (n.slice(0,2).toString() == [4,4].toString() || n.slice(1,3).toString() == [4,4].toString() || n.slice(2,4).toString() == [4,4].toString() || n.slice(3,5).toString() == [4,4].toString() || n.slice(2,6).toString() == [4,4].toString()) {
                this.level = "二举"
            }
            else if (n.indexOf(4) != -1) {
                this.level = "一秀"
            }
            else {
                this.level = "无"
            }
        },
    },
    template:`
    <div class="main-double">
        <p class="main-char">中秋博饼</p>
        <p class="explain">请截图在QQ群领取奖品！QQ群号857703332</p>
        <button class="btn btn-success" v-on:click="bb">博饼</button>
        <p>{{ number[0] }} {{ number[1] }} {{ number[2] }} {{ number[3] }} {{ number[4] }} {{ number[5] }}</p>
        <p>{{ level }}</p>
    </div>
    `
})