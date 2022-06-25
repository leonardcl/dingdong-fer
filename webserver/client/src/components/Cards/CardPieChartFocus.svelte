<script>
  import { onMount } from "svelte";
  // library that creates chart objects in page
  import Chart from "chart.js/auto/auto.esm";
  import "chartjs-adapter-moment";

  // init chart

  let emotionData = [];
  let classDuration = [];
  let promise = Promise.resolve([]);

  onMount(async () => {
    graphPieChart();
  });

  export function handleShowGraph(emoData, classDur) {
    console.log("Gettting the data...");
    emotionData = emoData;
    classDuration = classDur;
    graphPieChart();
  }

  async function graphPieChart() {
    var config = {
      type: "doughnut",
      data: {
        labels: ["Face Detected", "Face Not Detected"],
        datasets: [
          {
            // label: new Date().getFullYear(),
            label: "Emotion Summary",
            backgroundColor: ["rgb(255, 99, 132)", "rgb(54, 162, 235)"],
            stepped: true,
            segment: {
              // borderDash: (ctx) => skipped(ctx, [6, 6]),
              borderColor: (ctx) => skipped(ctx, "rgb(200,200,200,0.8)"),
            },
            spanGaps: true,
            data: [
              ((emotionData.positive +
                emotionData.negative +
                emotionData.neutral) *
                100) /
                classDuration,
              ((classDuration -
                emotionData.positive -
                emotionData.negative -
                emotionData.neutral) *
                100) /
                classDuration,
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
        plugins: {
          legend: {
            labels: {
              color: "#1c1c1c",
              usePointStyle: true,
              font: {
                size: 14,
              },
            },
            color: "#1c1c1c",
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
    var ctx = document.getElementById("pie-focus-chart").getContext("2d");
    if (window.myPieFocus) {
      window.myPieFocus.destroy();
    }
    window.myPieFocus = new Chart(ctx, config);
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
        <h2 class="text-blueGray-700 text-xl font-semibold">Face Detection</h2>
      </div>
    </div>
  </div>
  <div class="p-4 flex-auto">
    <!-- Chart -->
    <div class="relative h-350-px overflow-x-auto">
      <canvas id="pie-focus-chart" />
    </div>
  </div>
</div>
