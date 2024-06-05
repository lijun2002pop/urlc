<template>
  <div class="about">
    <h1>This is an about page</h1>
    <a-input-search
      v-model:value="val"
      placeholder="input search text"
      enter-button="Search"
      size="large"
      @search="searched"
    />
    <a-row>
      <a-col id="main" style="height: 500px" :span="12"></a-col>
      <a-col id="main2" style="height: 500px" :span="12"></a-col>
    </a-row>
  </div>
</template>
<script >
import * as echarts from "echarts";
export default {
  data() {
    return {
      val: "",
      checked: false,
    };
  },
  methods: {
    run(data,myChart){
      for (var i = 0; i < data.length; ++i) {
          if (Math.random() > 0.9) {
            data[i] += Math.round(Math.random() * 2000);
          } else {
            data[i] += Math.round(Math.random() * 200);
          }
        }
        myChart.setOption({
          series: [
            {
              type: "bar",
              data,
            },
          ],
        });
    },
    searched() {
      let url = "/sug?code=utf-8&q=" + this.val + "&callback=cb";
      this.$http
        .get("/api" + url)
        .then((res) => {
          console.log(res.data);
        })
        .catch((err) => {
          console.log(err);
        });
    },
    init_echart() {
      var chartDom = document.getElementById("main");
      console.log(chartDom);
      var myChart = echarts.init(chartDom);
      var option;
      option = {
        tooltip: {
          trigger: "item",
        },
        legend: {
          top: "5%",
          left: "center",
        },
        series: [
          {
            name: "Access From",
            type: "pie",
            radius: ["40%", "70%"],
            avoidLabelOverlap: false,
            itemStyle: {
              borderRadius: 10,
              borderColor: "#fff",
              borderWidth: 2,
            },
            label: {
              show: false,
              position: "center",
            },
            emphasis: {
              label: {
                show: true,
                fontSize: 40,
                fontWeight: "bold",
              },
            },
            labelLine: {
              show: false,
            },
            data: [
              { value: 1048, name: "Search Engine" },
              { value: 735, name: "Direct" },
              { value: 580, name: "Email" },
              { value: 484, name: "Union Ads" },
              { value: 300, name: "Video Ads" },
            ],
          },
        ],
      };
      option && myChart.setOption(option);
    },
    init_echart02() {
      var chartDom = document.getElementById("main2");
      console.log(chartDom);
      var myChart = echarts.init(chartDom);
      var option;
      const data = [];
      for (let i = 0; i < 5; ++i) {
        data.push(Math.round(Math.random() * 200));
      }
      option = {
        xAxis: {
          max: "dataMax",
        },
        yAxis: {
          type: "category",
          data: ["A", "B", "C", "D", "E"],
          inverse: true,
          animationDuration: 300,
          animationDurationUpdate: 300,
          max: 2, // only the largest 3 bars will be displayed
        },
        series: [
          {
            realtimeSort: true,
            name: "X",
            type: "bar",
            data: data,
            label: {
              show: true,
              position: "right",
              valueAnimation: true,
            },
          },
        ],
        legend: {
          show: true,
        },
        animationDuration: 0,
        animationDurationUpdate: 3000,
        animationEasing: "linear",
        animationEasingUpdate: "linear",
      };
      setTimeout(()=> {
        this.run(data,myChart);
      }, 0);
      setInterval(()=> {
        this.run(data,myChart);
      }, 3000);

      option && myChart.setOption(option);
    },
  },
  mounted() {
    this.init_echart();
    this.init_echart02();
  },
};
</script>
