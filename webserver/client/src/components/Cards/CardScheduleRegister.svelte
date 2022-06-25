<script>
  import { link, navigate } from "svelte-routing";
  import { onMount } from "svelte";
  import CardScheduleList from "./CardScheduleList.svelte";
  import SveltyPicker from "svelty-picker";
  import { parseTwoDigitYear } from "moment";

  let class_name = "",
    login_error_status = "";
  let promise = Promise.resolve([]);
  let teacher_id = "",
    UserEmail = "",
    UserName = "";
  let cardScheduleListComponent;
  let classNames;
  let class_id;

  //Date Picker
  let date = new Date();
  let start_date = "2021-11-11 12:00:00";
  start_date =
    date.getFullYear() +
    "-" +
    String(date.getMonth() + 1).padStart(2, "0") +
    "-" +
    String(date.getDate()).padStart(2, "0") +
    " " +
    String(date.getHours()).padStart(2, "0") +
    ":" +
    String(date.getMinutes()).padStart(2, "0");
  let end_date = "2021-11-11 12:00";
  end_date =
    date.getFullYear() +
    "-" +
    String(date.getMonth() + 1).padStart(2, "0") +
    "-" +
    String(date.getDate()).padStart(2, "0") +
    " " +
    String(date.getHours() + 1).padStart(2, "0") +
    ":" +
    String(date.getMinutes()).padStart(2, "0");
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

  async function handleSubmit() {
    // promise = submitData();
    if (class_id === "") {
      login_error_status = "Please check yout input again, don't miss it!";
    } else {
      promise = await submitData();
      console.log("Submitted");
      await classScheduleListRefresh();
    }
  }

  // Schedule Register
  async function submitData() {
    const res = await fetch(
      "http://iot.petra.ac.id:5000/api/user/teacher/class/schedule/register",
      {
        method: "POST",
        headers: {
          "Content-Type": "application/json; charset=UTF-8",
        },
        body: JSON.stringify({
          class_id,
          start_date,
          end_date,
        }),
      }
    ).then(function (response) {
      console.log(response.status);
      if (response.status != 200) {
        // console.log(response.json().msg);
        login_error_status = "Sorry, please try again!";
      } else {
        login_error_status = "";
      }
      return response.json();
    });
    const json = await res;
    console.log(json);
    if (json.success === "success") {
      console.log("Yay, berhasil");
      login_error_status = "Class Added!";
      // console.log(json.user);
    }
  }

  // Class Selection
  export function handleClassName() {
    promise = getClassName();
  }

  // onMount(getClassName());

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

  async function classScheduleListRefresh(a) {
    console.log(class_id);
    cardScheduleListComponent.handleData(class_id);
  }
</script>

<div
  class="relative flex flex-col min-w-0 break-words w-full mb-6 shadow-lg rounded-lg bg-blueGray-100 border-0"
>
  <div class="rounded-t bg-white mb-0 px-6 py-6">
    <div class="text-center flex justify-between">
      <h6 class="text-blueGray-700 text-xl font-bold">Register Schedule</h6>
    </div>
  </div>
  <div class="flex-auto px-4 lg:px-10 py-10 pt-0">
    <form on:submit|preventDefault={handleSubmit}>
      <h6 class="text-blueGray-400 text-sm mt-3 mb-6 font-bold uppercase">
        Class Information
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
                classScheduleListRefresh("Hello");
              }}
              id="grid-role"
              class="border-0 px-3 py-3 placeholder-blueGray-300 text-blueGray-600 bg-white rounded text-sm shadow focus:outline-none focus:ring w-full ease-linear transition-all duration-150"
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
              Pick Class Start Time
            </label>
            <div>
              <SveltyPicker
                inputClasses="border-0 px-3 py-3 placeholder-blueGray-300 text-blueGray-600 bg-white rounded text-sm shadow focus:outline-none focus:ring w-full ease-linear transition-all duration-150"
                format="yyyy-mm-dd hh:ii"
                bind:value={start_date}
                on:change={() => {
                  console.log("Tanggal berubah");
                  let d1 = new Date(start_date);
                  let d2 = new Date(end_date);

                  if (d2.getTime() < d1.getTime()) {
                    console.log("Ubah berubah");

                    end_date =
                      d1.getFullYear() +
                      "-" +
                      String(d1.getMonth() + 1).padStart(2, "0") +
                      "-" +
                      String(d1.getDate()).padStart(2, "0") +
                      " " +
                      String(d1.getHours() + 1).padStart(2, "0") +
                      ":" +
                      String(d1.getMinutes()).padStart(2, "0");
                  }
                }}
              />
            </div>
          </div>
        </div>

        <div class="w-full lg:w-full px-4">
          <div class="relative w-full mb-3">
            <label
              class="block uppercase text-blueGray-600 text-xs font-bold mb-2"
              for="grid-username"
            >
              Pick Class End Time
            </label>
            <div>
              <SveltyPicker
                inputClasses="border-0 px-3 py-3 placeholder-blueGray-300 text-blueGray-600 bg-white rounded text-sm shadow focus:outline-none focus:ring w-full ease-linear transition-all duration-150"
                format="yyyy-mm-dd hh:ii"
                bind:value={end_date}
              />
            </div>
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
              Add This Class
            </button>
          </div>
        </div>
      </div>
    </form>
  </div>
</div>

<CardScheduleList bind:this={cardScheduleListComponent} color="light" />
