<script>
  import { link, navigate } from "svelte-routing";
  import { onMount } from "svelte";
  import CardLineChart from "./CardLineChart.svelte";
  import CardPieChartEmotion from "./CardPieChartEmotion.svelte";
  import CardPieChartFocus from "./CardPieChartFocus.svelte";
  import SveltyPicker from "svelty-picker";

  let class_name = "",
    login_error_status = "";
  let promise = Promise.resolve([]);
  let teacher_id = "",
    UserEmail = "",
    UserName = "";
  let classNames;
  let class_id;
  let schedule_id;
  let student_id;
  let studentList;
  let scheduleList;
  let emotionData;
  let CardLineChartComponent;
  let CardPieChartEmotionComponent;
  let CardPieChartFocusComponent;

  //Date Picker
  let start_date = "2021-11-11 12:00:00";
  let end_date = "2021-11-11 12:00:00";
                                                                               
  onMount(async () => {
    if (sessionStorage.user_id) {
      teacher_id = sessionStorage.getItem("user_id");
      UserEmail = sessionStorage.getItem("email");
      UserName = sessionStorage.getItem("username");

      // navigate("/", { replace: true });
    } else {
      console.log("No Session");
      navigate("/", { replace: true });
    }

    const res = await fetch(
      "http://iot.petra.ac.id:5000/api/user/teacher/class",
      {
        method: "POST",
        headers: {
          "Content-Type": "application/json; charset=UTF-8",
        },
        body: JSON.stringify({
          teacher_id,
        }),
      }
    ).then(function (response) {
      console.log(response.status);
      if (response.status != 200) {
        console.log("Wahh error");
      } else {
        console.log("Wahh berhasil");
      }
      return response.json();
    });
    const json = await res;
    classNames = json.data;
    console.log(classNames);
    console.log("classNames");

    if (json.success === "success") {
      console.log("Yay, berhasil");
      // console.log(json.user);
    }
  });

  async function getEmotionData(user_id, class_id, schedule_id) {
    const res = await fetch(
      "http://iot.petra.ac.id:5000/api/user/data/emotion",
      {
        method: "POST",
        headers: {
          "Content-Type": "application/json; charset=UTF-8",
        },
        body: JSON.stringify({
          user_id,
          class_id,
          schedule_id,
        }),
      }
    ).then(function (response) {
      console.log(response.status);
      if (response.status != 200) {
        console.log("Wahh error yaaa");
      } else {
        console.log("Wahh berhasil yaaa");
      }
      return response.json();
    });
    const json = await res;
    emotionData = json.data;
    console.log(emotionData);
    console.log("emotionData");

    if (json.success === "success") {
      console.log("Yay, berhasil");
      // console.log(json.user);
    }
  }

  async function handleSubmitData() {
    console.log("Get Student Data");
    let user_id = student_id;
    console.log(user_id, class_id, schedule_id);
    if (
      user_id !== undefined &&
      class_id !== undefined &&
      schedule_id !== undefined
    ) {
      await getEmotionData(user_id, class_id, schedule_id);
      await CardLineChartComponent.handleShowGraph(emotionData.emotion_data);
      CardPieChartEmotionComponent.handleShowGraph(emotionData.summary);
      CardPieChartFocusComponent.handleShowGraph(
        emotionData.summary,
        emotionData.total_time
      );
    }
  }

  
  async function getClassName() {
    const res = await fetch(
      "http://iot.petra.ac.id:5000/api/user/teacher/class",
      {
        method: "POST",
        headers: {
          "Content-Type": "application/json; charset=UTF-8",
        },
        body: JSON.stringify({
          teacher_id,
        }),
      }
    ).then(function (response) {
      console.log(response.status);
      if (response.status != 200) {
        console.log("Wahh error");
      } else {
        console.log("Wahh berhasil");
      }
      return response.json();
    });
    const json = await res;
    classNames = json.data;
    console.log(classNames);
    console.log("classNames");

    if (json.success === "success") {
      console.log("Yay, berhasil");
      // console.log(json.user);
    }
  }

  // Get Schedule
  async function getScheduleData() {
    const res = await fetch(
      "http://iot.petra.ac.id:5000/api/user/teacher/class/schedule",
      {
        method: "POST",
        headers: {
          "Content-Type": "application/json; charset=UTF-8",
        },
        body: JSON.stringify({
          class_id,
        }),
      }
    ).then(function (response) {
      console.log(response.status);
      if (response.status != 200) {
        login_error_status = "Sorry, please try again!";
      } else {
        login_error_status = "";
      }
      return response.json();
    });
    const json = await res;
    scheduleList = json.data;
    console.log(scheduleList);
    console.log("scheduleList");

    if (json.success === "success") {
      console.log("Yay, berhasil");
    }
  }

  // Get Student Data
  async function getStudentData() {
    const res = await fetch(
      "http://iot.petra.ac.id:5000/api/user/teacher/class/student",
      {
        method: "POST",
        headers: {
          "Content-Type": "application/json; charset=UTF-8",
        },
        body: JSON.stringify({
          class_id,
        }),
      }
    ).then(function (response) {
      console.log(response.status);
      if (response.status != 200) {
        login_error_status = "Sorry, please try again!";
      } else {
        login_error_status = "";
      }
      return response.json();
    });
    const json = await res;
    studentList = json.data;
    console.log(studentList);
    console.log("studentList");

    if (json.success === "success") {
      console.log("Yay, berhasil");
    }
  }

  async function classScheduleStudentListRefresh() {
    console.log(class_id);
    await getScheduleData();
    await getStudentData();
  }
  // Class Selection
  export function handleClassName() {
    promise = getClassName();
  }

  // onMount(getClassName());


</script>

<div
  class="relative flex flex-col min-w-0 break-words w-full mb-6 shadow-lg rounded-lg bg-blueGray-100 border-0"
>
  <div class="rounded-t bg-white mb-0 px-6 py-6">
    <div class="text-center flex justify-between">
      <h6 class="text-blueGray-700 text-xl font-bold">Emotion Data</h6>
    </div>
  </div>
  <div class="flex-auto px-4 lg:px-10 py-10 pt-0">
    <form on:submit|preventDefault={handleSubmitData}>
      <h6 class="text-blueGray-400 text-sm mt-3 mb-6 font-bold uppercase">
        Student & Class Information
      </h6>
      <div class="flex flex-wrap">
        <div class="w-full lg:w-full px-4">
          <div class="relative w-full mb-3">
            <label
              class="block uppercase text-blueGray-600 text-xs font-bold mb-2"
              for="grid-username"
            >
              Class Name
            </label>
            <!-- svelte-ignore a11y-no-onchange -->
            <select
              bind:value={class_id}
              on:change={() => {
                classScheduleStudentListRefresh();
              }}
              id="grid-role"
              class="border-0 px-3 py-3 placeholder-blueGray-300 text-blueGray-600 
              bg-white rounded text-sm shadow focus:outline-none focus:ring w-full 
              ease-linear transition-all duration-150"
            >
              <option value="none" selected disabled hidden
                >Select an Option</option
              >
              {#if classNames}
                {#each classNames as data}
                  <option value={data._id}>{data.class_name}</option>
                  <!-- <option value="student">Student</option> -->
                {/each}
              {/if}
            </select>
          </div>
        </div>

        <div class="w-full lg:w-full px-4">
          <div class="relative w-full mb-3">
            <label
              class="block uppercase text-blueGray-600 text-xs font-bold mb-2"
              for="grid-username"
            >
              Select Schedule
            </label>
            <!-- svelte-ignore a11y-no-onchange -->
            <select
              bind:value={schedule_id}
              id="grid-role"
              class="border-0 px-3 py-3 placeholder-blueGray-300 text-blueGray-600 bg-white rounded text-sm shadow focus:outline-none focus:ring w-full ease-linear transition-all duration-150"
            >
              <option value="none" selected disabled hidden
                >Select an Option</option
              >
              {#if scheduleList}
                {#each scheduleList as data}
                  <option value={data._id}
                    >{data.start_time} - {data.end_time}</option
                  >
                  <!-- <option value="student">Student</option> -->
                {/each}
              {/if}
            </select>
          </div>
        </div>

        <div class="w-full lg:w-full px-4">
          <div class="relative w-full mb-3">
            <label
              class="block uppercase text-blueGray-600 text-xs font-bold mb-2"
              for="grid-username"
            >
              Select Student
            </label>
            <!-- svelte-ignore a11y-no-onchange -->
            <select
              bind:value={student_id}
              id="grid-role"
              class="border-0 px-3 py-3 placeholder-blueGray-300 text-blueGray-600 bg-white rounded text-sm shadow focus:outline-none focus:ring w-full ease-linear transition-all duration-150"
            >
              <option value="none" selected disabled hidden
                >Select an Option</option
              >
              {#if studentList}
                {#each studentList as data}
                  <option value={data.user_id}
                    >{data.username} | {data.email}</option
                  >
                  <!-- <option value="student">Student</option> -->
                {/each}
              {/if}
            </select>
          </div>
        </div>

        <div class="w-full lg:w-6/12 px-4">
          <div class="relative w-full mb-3">
            <h2 class="text-blueGray-500 text-lg font-bold">
              {login_error_status}
            </h2>
          </div>
        </div>

        <div class="w-full lg:w-6/12 px-4">
          <div class="relative w-full mb-3">
            <label
              class="block uppercase text-blueGray-600 text-xs font-bold mb-2"
              for="grid-last-name"
            />
            <button
              class="mt-auto w-full bg-sky-400 text-white active:bg-sky-500 font-bold uppercase text-xs px-4 py-2 rounded shadow hover:shadow-md outline-none focus:outline-none mr-1 ease-linear transition-all duration-150"
              type="submit"
            >
              Look This Student Data
            </button>
          </div>
        </div>
      </div>
    </form>
  </div>
</div>

<CardLineChart bind:this={CardLineChartComponent} color="light" />
<div class="flex flex-wrap mt-4">
  <div class="w-full xl:w-6/12 mb-4 xl:mb-0 xl:pr-4">
    <CardPieChartEmotion
      bind:this={CardPieChartEmotionComponent}
      color="light"
    />
  </div>
  <div class="w-full xl:w-6/12 xl:pl-4">
    <CardPieChartFocus bind:this={CardPieChartFocusComponent} color="light" />
  </div>
</div>
<!-- <CardPieChartEmotion bind:this={CardPieChartEmotionComponent} color="light" />
<CardPieChartFocus bind:this={CardPieChartFocusComponent} color="light" /> -->
