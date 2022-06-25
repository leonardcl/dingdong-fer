<script>
  import { onMount } from "svelte";
  // library that creates chart objects in page
  import Chart from "chart.js/auto/auto.esm";
  import "chartjs-adapter-moment";

  // init chart

  let emotionData = [];
  let promise = Promise.resolve([]);

  onMount(async () => {
    graphPieChart();
  });

  export function handleShowGraph(data) {
    console.log("Gettting the data...");
    emotionData = data;
    graphPieChart();
  }

  async function graphPieChart() {
    var config = {
      type: "doughnut",
      data: {
        labels: ["Positive", "Negative", "Neutral"],
        datasets: [
          {
            // label: new Date().getFullYear(),
            label: "Emotion Summary",
            backgroundColor: [
              "rgb(255, 99, 132)",
              "rgb(54, 162, 235)",
              "rgb(255, 205, 86)",
            ],
            stepped: true,
            segment: {
              // borderDash: (ctx) => skipped(ctx, [6, 6]),
              borderColor: (ctx) => skipped(ctx, "rgb(200,200,200,0.8)"),            
            },
            spanGaps: true,
            data: [
              (emotionData.positive * 100) /
                (emotionData.positive +
                  emotionData.negative +
                  emotionData.neutral),
              (emotionData.negative * 100) /
                (emotionData.positive +
                  emotionData.negative +
                  emotionData.neutral),
              (emotionData.neutral * 100) /
                (emotionData.positive +
                  emotionData.negative +
                  emotionData.neutral),
            ],
          },
        ],
      },
      options: {
        maintainAspectRatio: false,
        responsive: true,
        title: {
          display: false,
          text: "Emotion Chart",
          color: "#adadad",
        },
        legend: {
            labels: {
              fontColor: "#1c1c1c",
            },
          },
        plugins: {
          legend: {
            labels: {
              color: "#1c1c1c",
              usePointStyle: true,
              font: {
                size: 14,
              },
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
      },
    };
    var ctx = document.getElementById("pie-emotion-chart").getContext("2d");
    if (window.myPieEmotion) {
      window.myPieEmotion.destroy();
    }
    window.myPieEmotion = new Chart(ctx, config);
  }
</script>

<div
  class="relative flex flex-col min-w-0 break-words w-full mb-6 shadow-lg rounded bg-white"
>
  <div class="rounded-t mb-0 px-4 py-3 bg-transparent">
    <div class="flex flex-wrap items-center">
      <div class="relative w-full max-w-full flex-grow flex-1">
        <h6 class="uppercase text-blueGray-400 mb-1 text-xs font-semibold">
          Summary
        </h6>
        <h2 class="text-blueGray-700 text-xl font-semibold">Emotion Summary</h2>
      </div>
    </div>
  </div>
  <div class="p-4 flex-auto">
    <!-- Chart -->
    <div class="relative h-350-px overflow-x-auto">
      <canvas id="pie-emotion-chart" />
    </div>
  </div>
</div>
