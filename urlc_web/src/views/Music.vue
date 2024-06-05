<template>
    <div class="divs">
        <a-row  align="middle">
            <a-col :span="2" > </a-col>
            <a-col :span="4" style="transform: scale(1.5);color: green"> {{getmusic}}</a-col>
            <a-col :span="10">            
                <audio ref="music_audio" controls style="margin: 6px 0;width: 80%;"></audio>
            </a-col>
            <a-col :span="1" style="font-size: x-large;">
                <a @click="after_music()"><StepBackwardOutlined /></a>
                </a-col>
            <a-col :span="1" style="font-size: x-large;">
                <a @click="next_music()"><StepForwardOutlined /></a></a-col>
            <a-col :span="1" style="font-size: x-large;">
                <a style="white-space:nowrap;" @click="this.play_soft = 0" v-if="this.play_soft" ><RetweetOutlined/>
                <span style="color: black;font-size: medium;">循环播放</span></a>
                <a style="white-space:nowrap;" @click="this.play_soft = 1" v-else ><SwapOutlined />
                <span style="color: black;font-size: medium;">随机播放</span></a>
            </a-col>
            <a-col :span="5"> 
                
            </a-col>
        </a-row> 
        <a-list bordered :data-source="data"  :pagination="pagination" >
            <template #renderItem="{ item,index }">
                <a-list-item :class="{ischecked:getmusic==item}"> 
                    <router-link :to="'/urils/index/?title='+item">{{ item }}</router-link>
                    <template #actions>                
                        <a @click="playMusic(index)" style="font-size: 21px;color: black;"><CaretRightOutlined /></a>
                    </template>
                </a-list-item>
            </template>
            <template #header>
                <a-row align="middle">
                <a-col :span="18" ><strong>本地音乐</strong> </a-col>
                <a-col :span="6" > 
                    <a-input-search
                    v-model:value="val"
                    placeholder="搜索歌曲"
                    enter-button
                    size="large"
                    @search="onSearch"
                    />
                </a-col>
            </a-row>
            </template>
        </a-list>
        
    </div>
</template>

<script>
    import {CaretRightOutlined,StepForwardOutlined,StepBackwardOutlined,EnterOutlined,RetweetOutlined,SwapOutlined} from '@ant-design/icons-vue';
    export default {
        components:{
            CaretRightOutlined,
            StepForwardOutlined,
            StepBackwardOutlined,
            EnterOutlined,
            RetweetOutlined,
            SwapOutlined
        },
        data(){
            return {
                data:[],
                now_index:0,
                val:'',
                play_soft:0,//0循环，1随机
                pagination:{
                    onChange: page => {
                        this.pagination.current=page
                    },
                    pageSize: 8,
                    current:1
                    }
            }
        },
        computed:{
            getmusic(){
                return this.data[this.now_index]
            }
        },
        async created(){
            await this.load_data()
            const name = this.data[this.now_index];
            this.$refs.music_audio.src=this.$http.defaults.baseURL+ '/home/play/?name='+name
            this.$refs.music_audio.addEventListener('ended', ()=> {
                if (this.play_soft) {
                    //循环播放
                    this.next_music()
                }else{
                    //随机播放
                    const num = Math.floor(Math.random() * (this.data.length))
                    this.now_index = num
                    this.play()
                }
                
            }, false);

        },
        methods:{
            async load_data(){
                const res = await this.$http.get('/home/music_list/')
                this.data=res.data
            },
            play(){
                const name = this.data[this.now_index];
                this.$refs.music_audio.src=this.$http.defaults.baseURL+ '/home/play/?name='+name
                this.$refs.music_audio.play()
                this.pagination.current=Math.ceil((this.now_index+1)/this.pagination.pageSize)  
            },
            playMusic(index){
                this.now_index = ((this.pagination.current -1 ) * this.pagination.pageSize)+index
                this.play()
            },
            after_music(){
                if(this.now_index == 0){
                    return
                }
                this.now_index--
                this.play()
            },next_music(){
                if (this.play_soft == 1){
                    this.now_index = Math.floor(Math.random() * (this.data.length))
                }
                else{
                    if(this.now_index == this.data.length-1){
                        this.now_index=0
                    }else{
                    this.now_index++ 
                    }
                }
                this.play()
            },
            async onSearch(){
                await this.load_data()
                this.data = this.data.filter(i=>{return i.includes(this.val)})
            }
        }
    }
</script>

<style >
.ischecked{
    background: azure;
    font-size: x-large;
    transition: 0.5s;
}
</style>