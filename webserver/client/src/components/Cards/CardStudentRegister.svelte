<script>
  import { link, navigate } from "svelte-routing";
  import { onMount } from "svelte";
  import CardStudentList from "./CardStudentList.svelte";
  import SveltyPicker from "svelty-picker";

  let class_name = "",
    login_error_status = "";
  let promise = Promise.resolve([]);
  let teacher_id = "",
    UserEmail = "",
    UserName = "";
  let CardStudentListComponent;
  let classNames;
  let class_id;
  let new_student_id;
  let check_id_status = "";

  //Date Picker
  let start_date = "2021-11-11 12:00:00";
  let end_date = "2021-11-11 12:00:00";
  let checked = 0;

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
    if (checked !== 1) {
      login_error_status = "Please check yout input again, don't miss it!";
    } else {
      promise = await submitData();
      console.log("Submitted");
      await classScheduleListRefresh("HLO");
    }
  }

  // Schedule Register
  async function submitData() {
    let student_id = new_student_id;
    const res = await fetch(
      "http://iot.petra.ac.id:5000/api/user/teacher/class/student/register",
      {
        method: "POST",
        headers: {
          "Content-Type": "application/json; charset=UTF-8",
        },
        body: JSON.stringify({
          class_id,
          student_id,
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
      login_error_status = "Student Added!";
      // console.log(json.user);
    } else {
      login_error_status = "Sorry, please try again! " + json.msg;
    }
  }

  // Check Student ID
  async function checkStudentID() {
    let student_id = new_student_id;
    const res = await fetch("http://iot.petra.ac.id:5000/api/user/id", {
      method: "POST",
      headers: {
        "Content-Type": "application/json; charset=UTF-8",
      },
      body: JSON.stringify({
        student_id,
      }),
    }).then(function (response) {
      console.log(response.status);
      if (response.status != 200) {
        // console.log(response.json().msg);
        check_id_status = "Sorry, please try again! Check the ID!";
      } else {
        check_id_status = "";
      }
      return response.json();
    });
    const json = await res;
    console.log(json);
    if (json.success == "success") {
      console.log("data diberikan");
      return json.data;
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
    CardStudentListComponent.handleData(class_id);
  }

  async function handleCheck(new_id) {
    // promise = submitData();
    resetValue();
    if (new_id) {
      console.log("Checking ID...");
      console.log("ID" + new_id);
      let new_student = await checkStudentID();
      console.log(new_student);
      check_id_status = new_student.username + " Role: " + new_student.role;
      if (new_student.role === "teacher") {
        checked = 0;
        check_id_status =
          new_student.username + " - " + new_student.role + " | Student Only";
      } else {
        checked = 1;
        check_id_status =
          new_student.username +
          " - " +
          new_student.role +
          " | Success" +
          checked;
      }
    } else {
      check_id_status = "Please input student ID";
    }
  }

  function resetValue() {
    // promise = submitData();
    check_id_status = "";
    login_error_status = "";
    checked = 0;
  }
</script>

<div
  class="relative flex flex-col min-w-0 break-words w-full mb-6 shadow-lg rounded-lg bg-blueGray-100 border-0"
>
  <div class="rounded-t bg-white mb-0 px-6 py-6">
    <div class="text-center flex justify-between">
      <h6 class="text-blueGray-700 text-xl font-bold">Register Student</h6>
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
                new_student_id = "";
                resetValue();
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
              Student ID
            </label>
            <input
              bind:value={new_student_id}
              on:change={() => {
                check_id_status = "";
                login_error_status = "";
              }}
              id="grid-username"
              type="number"
              class="border-0 px-3 py-3 placeholder-blueGray-300 text-blueGray-600 bg-white rounded text-sm shadow focus:outline-none focus:ring w-full ease-linear transition-all duration-150"
            />
          </div>
        </div>

        <div class="w-full lg:w-4/12 px-4">
          <div class="relative w-full mb-3">
            <label
              class="block uppercase text-blueGray-600 text-xs font-bold mb-2"
              for="grid-last-name"
            />
            <button
              class="mt-auto w-full bg-lime-600 text-white active:bg-sky-500 font-bold uppercase text-xs px-4 py-2 rounded shadow hover:shadow-md outline-none focus:outline-none mr-1 ease-linear transition-all duration-150"
              type="button"
              on:click={handleCheck(new_student_id)}
            >
              Check User
            </button>
          </div>
        </div>

        <div class="w-full lg:w-8/12 px-4 align-middle">
          <div class="relative w-full mt-2 align-middle">
            <h2 class="text-blueGray-500 text-lg font-bold align-middle">
              Status: {check_id_status}
            </h2>
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
              Add To This Class
            </button>
          </div>
        </div>
      </div>
    </form>
  </div>
</div>

<CardStudentList bind:this={CardStudentListComponent} color="light" />
