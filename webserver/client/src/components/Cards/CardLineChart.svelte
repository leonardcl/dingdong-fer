<script>
  import { onMount } from "svelte";
  // library that creates chart objects in page
  import Chart from "chart.js/auto/auto.esm";
  import "chartjs-adapter-moment";

  // init chart

  let emotionData = [];
  let promise = Promise.resolve([]);

  onMount(async () => {
    graphLineChart();
  });

  export function handleShowGraph(data) {
    console.log("Gettting the data...");
    emotionData = data;
    graphLineChart();
  }

  async function graphLineChart() {
    const skipped = (ctx, value) =>
      ctx.p0.skip || ctx.p1.skip ? value : undefined;                              
    var config = {
      type: "line",
      data: {
        datasets: [
          {
            label: "Emotion",
            color: "#adadad",
            fill: false,
            borderColor: "#ebd217",
            backgroundColor: "#ebd217",
            stepped: true,
            pointRadius: 0,
            segment: {
              borderColor: (ctx) => skipped(ctx, "rgb(240,31,191,0.8)"),                
            },
            spanGaps: true,
            data: emotionData,
          },
        ],
      },
      options: {
        interaction: {
          intersect: false,
        },
        maintainAspectRatio: false,
        responsive: true,
        title: {
          display: false,
          text: "Emotion Chart",
          color: "#adadad",
        },
        plugins: {
          legend: {
            labels: {
              color: "#adadad",
              usePointStyle: true,
            },
            color: "#adadad",
            align: "end",
            position: "bottom",
          },
        },
        tooltips: {
          mode: "index",
          intersect: false,
        },
        hover: {
          mode: "nearest",
          intersect: true,
        },
        scales: {
          y: {
            type: "category",
            labels: [
              "Surprise",
              "Happy",
              "Neutral",
              "Sad",
              "Fear",
              "Disgust",
              "Angry",
            ],
            ticks: {
              color: "#adadad",
            },
            offset: true,
            position: "left",
            display: true,
            title: {
              display: true,
              text: "Value",
              color: "#ffffff",
            },
            grid: {
              borderDash: [3],
              borderDashOffset: [3],
              drawBorder: false,
              color: "#adadad",
              zeroLineColor: "#7d7c7c",
              zeroLineBorderDash: [2],
              zeroLineBorderDashOffset: [2],
            },
          },
          x: {
            color: "#adadad",
            type: "time",
            ticks: {
              color: "#adadad",
              autoSkip: true,
            },
            time: {
              unit: "second",
            },
            title: {
              display: true,
              text: "Time",
              color: "#ffffff",
            },
            display: true,
            grid: {
              color: "#ffffff",
              display: false,
              borderDash: [2],
              borderDashOffset: [2],
              zeroLineColor: "rgba(0, 0, 0, 0)",
              zeroLineBorderDash: [2],
              zeroLineBorderDashOffset: [2],
            },
          },
        },
      },
    };
    var ctx = document.getElementById("line-chart").getContext("2d");
    if (window.myLine) {
      window.myLine.destroy();
    }
    window.myLine = new Chart(ctx, config);
  }
</script>

<div
  class="relative flex flex-col min-w-0 break-words w-full mb-6 shadow-lg rounded bg-blueGray-700"
>
  <div class="rounded-t mb-0 px-4 py-3 bg-transparent">
    <div class="flex flex-wrap items-center">
      <div class="relative w-full max-w-full flex-grow flex-1">
        <h6 class="uppercase text-blueGray-100 mb-1 text-xs font-semibold">
          Overview
        </h6>
        <h2 class="text-white text-xl font-semibold">Emotion Data</h2>
      </div>
    </div>
  </div>
  <div class="relative p-4 flex-auto">
    <!-- Chart -->
    <div class="overflow-x-scroll">
      <div class="h-350-px" style="width: 7000px;">
        <canvas id="line-chart" />
      </div>
    </div>
  </div>
</div>
