<template>
  <div class="main">
    <audio src="" controls ref="audio"></audio>
    <div class="containar" ref="coutainer">
      <ul ref="ul"></ul>
    </div>
  </div>
</template>

<script>
import {ArrowLeftOutlined} from '@ant-design/icons-vue';
var host = 'http://127.0.0.1:8000'
export default {
  components:{
    ArrowLeftOutlined
  },
  data(){
    return {
      data:''
    }
  },
    beforeRouteLeave(to, from, next) {
      this.$refs.audio.removeEventListener('timeupdate', this.setOffest)
      next();
  },
  async mounted(){
    let music = this.$route.query.title
    try {
      let res = await this.$http.get('/home/music/?name='+ music)
      let {msg,words} = res.data;
      this.data = this.parseLar(words);
      this.$refs.audio.src = this.$http.defaults.baseURL+'/home/play/?name='+music
      this.initElement()
      this.$refs.audio.addEventListener('timeupdate', this.setOffest)
    } catch (error) {
      return
    }
    
  },
  methods: {
    parseLar(lar) {
      let lines = lar.split("\n");
      let result = [];
      for (let index = 0; index < lines.length; index++) {
        let line = lines[index];
        let parts = line.split("]");
        let timestr = parts[0].substring(1);
        let obj = {
          time: this.parsetime(timestr),
          words: parts[1],
        };
        result.push(obj);
      }
      return result;
    },
    parsetime(timeStr) {
      let li = timeStr.split(":");
      return +li[0] * 60 + +li[1];
    },
    findIndex() {
      var curtime = this.$refs.audio.currentTime;
      for (let index = 0; index < this.data.length; index++) {
        if (curtime < this.data[index].time) {
          return index - 1;
        }
      }
      return this.data.length - 1;
    },
    initElement() {
            var frag = document.createDocumentFragment()
            for (let index = 0; index < this.data.length; index++) {
                const element = this.data[index];
                var li = document.createElement('li');
                li.textContent = element.words;
                // this.$refs.ul.appendChild(li);
                frag.appendChild(li)
            }
            this.$refs.ul.appendChild(frag)
        },
        setOffest() {
            var containerHeight = this.$refs.coutainer.clientHeight;
            var liHeight = this.$refs.ul.children[0].clientHeight;
            var maxOffest = this.$refs.ul.clientHeight - containerHeight;
            var index = this.findIndex()
            var offset = liHeight * index + liHeight / 2 - containerHeight / 2
            if (offset < 0) {
                offset = 0
            }
            if (offset > maxOffest) {
                offset = maxOffest
            }
            this.$refs.ul.style.transform = `translateY(-${offset}px)`;
            var li = this.$refs.ul.querySelector('.active');
            if (li) {
                li.classList.remove('active')
            }
            li = this.$refs.ul.children[index];
            if (li) {
                li.classList.add('active')
            }
        }
  },
};
</script>

<style>
.main {
  /* background-image:url('@/assets/风景.jpg'); */
  margin: 0;
  padding: 0;
  background: black;
  color: darkgray;
  text-align: center;
  height: 100%;
}

.containar {
  margin-top: 100px;
  overflow: hidden;
  height: 400px;
  /* border: 2px solid white; */
}

.containar ul {
  /* transform: translateY(72px); */
  /* border: 2px solid white; */
  transition: 0.6s;
}

.containar ul li {
  list-style: none;
  /* border: 2px solid white; */
  line-height: 30px;
  transition: 0.2s;
}

.containar ul li.active {
  color: white;
  /* font-size: 20px; */
  transform: scale(1.4);
}

audio {
  margin: 30px 0;
  width: 650px;
}
</style>