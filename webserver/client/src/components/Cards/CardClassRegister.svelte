<script>
  import { onMount } from "svelte";

  import { link, navigate } from "svelte-routing";
  import CardClassList from "./CardClassList.svelte";

  // LOGIN SYSTEM
  let class_name = "",
    login_error_status = "";
  let promise = Promise.resolve([]);
  let teacher_id = "",
    UserEmail = "",
    UserName = "";
  let cardClassListComponent;

  async function handleSubmit() {
    // promise = submitData();
    if (class_name === "") {
      login_error_status = "Please check yout input again, don't miss it!";
    } else {
      promise = await submitData();
      console.log("Submitted");
      await cardClassListComponent.handleData(teacher_id);
    }
  }
  onMount(() => {
    if (sessionStorage.user_id) {
      teacher_id = sessionStorage.getItem("user_id");
      UserEmail = sessionStorage.getItem("email");
      UserName = sessionStorage.getItem("username");

      // navigate("/", { replace: true });
    } else {
      console.log("No Session");
      navigate("/", { replace: true });
    }
  });

  async function submitData() {
    const res = await fetch(
      "http://iot.petra.ac.id:5000/api/user/teacher/class/register",
      {
        method: "POST",
        headers: {
          "Content-Type": "application/json; charset=UTF-8",
        },
        body: JSON.stringify({
          teacher_id,
          class_name,
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
</script>

<div
  class="relative flex flex-col min-w-0 break-words w-full mb-6 shadow-lg rounded-lg bg-blueGray-100 border-0"
>
  <div class="rounded-t bg-white mb-0 px-6 py-6">
    <div class="text-center flex justify-between">
      <h6 class="text-blueGray-700 text-xl font-bold">Register Class</h6>
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
            <input
              bind:value={class_name}
              id="grid-username"
              type="text"
              class="border-0 px-3 py-3 placeholder-blueGray-300 text-blueGray-600 bg-white rounded text-sm shadow focus:outline-none focus:ring w-full ease-linear transition-all duration-150"
            />
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

<CardClassList bind:this={cardClassListComponent} color="light" />
