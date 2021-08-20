<template>
    <div>
        <div class="depository-box bottomline-dashed" data-toggle="collapse" v-bind:data-target="'#material'+material.id">
            <img v-bind:src="'civitas/icon/goods/'+material.id+'.png'" width="60px" height="60px" class="depository-mainimg"/>
            <span class="depository-text1">
                <p class="depository-name">{{ material.name }}<br></p>
                <p class="depository-loss">仓储损耗 {{ material.wastage.toFixed(1) }}%</p>
            </span>
            <span class="depository-text2">
                <p class="depository-num">{{ material.total.toFixed(2) }}<br></p>
                <p class="depository-loss">总量</p>
            </span>
            <span class="depository-text2">
                <p class="depository-num">{{ (material.total * material.unitmass).toFixed(2) }}<br></p>
                <p class="depository-loss">每单位重量 {{ material.unitmass.toFixed(2) }}</p>
            </span>
        </div>
        <div class="depository-detail bottomline-dashed collapse" v-bind:id="'material'+material.id" v-for="detailmes in material.detail" v-bind:key="detailmes.level">
            <span class="depository-star">
                <img v-bind:src="'civitas/icon/star/star.png'"/>
                <img v-bind:src="'civitas/icon/star/star.png'" v-if="detailmes.level >= 2"/>
                <img v-bind:src="'civitas/icon/star/star-none.png'" v-else/>
                <img v-bind:src="'civitas/icon/star/star.png'" v-if="detailmes.level >= 3"/>
                <img v-bind:src="'civitas/icon/star/star-none.png'" v-else/>
            </span>
            <span class="depository-text3">
                <p class="depository-num">{{ detailmes.count.toFixed(2) }}<br></p>
            </span>
            <span class="depository-text3">
                <p class="depository-num">{{ (detailmes.count * material.unitmass).toFixed(2) }}<br></p>
            </span>
        </div>
    </div>
</template>
<script>
module.exports = {
    
}
</script>
>
<style scoped>
    .depository-box-top
    {
        height: 50px;
    }

    .depository-box
    {
        height: 70px;
        padding-top: 5px;
    }

    .depository-box p
    {
        display: inline;
        margin: 0;
    }

    .depository-detail
    {
        height: 28px;
    }

    .depository-detail p
    {
        display: inline;
        margin: 0;
    }

    .depository-mainimg
    {
        float: left;
    }

    .depository-text-top
    {
        padding-top: 5px;
        margin-left: 80px;
        float: left;
        width: 100px;
    }

    .depository-text1
    {
        padding-top: 5px;
        margin-left: 20px;
        float: left;
        width: 100px;
    }

    .depository-text2
    {
        padding-top: 5px;
        float: left;
        width: 100px;
    }

    .depository-star
    {
        margin-left: 80px;
        float: left;
        width: 100px;
    }

    .depository-star img
    {
        margin: 0;
    }

    .depository-text3
    {
        padding-top: 2px;
        float: left;
        width: 100px;
    }

    .depository-name
    {
        color: rgb(100,100,100);
        font-weight: bold;
        font-size: 16px;
    }

    .depository-loss
    {
        color: rgb(100,100,100);
        font-size: 12px;
    }

    .depository-num
    {
        color: rgb(50,100,150);
        font-weight: bold;
        font-size: 16px;
    }
</style>