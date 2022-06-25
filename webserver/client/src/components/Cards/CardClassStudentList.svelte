<script>
  // core components
  import TableDropdown from "components/Dropdowns/TableDropdown.svelte";
  import { onMount } from "svelte";
  import { Confirm } from "svelte-confirm";
  // import { Datatable } from "svelte-simple-datatables";

  const settings = {
    sortable: true,
    pagination: true,
    rowsPerPage: 50,
    columnFilter: true,
  };

  const bootstrap = "../assets/img/bootstrap.jpg";
  const classlogo = "../assets/img/class_logo.png";
  const angular = "../assets/img/angular.jpg";
  const sketch = "../assets/img/sketch.jpg";
  const react = "../assets/img/react.jpg";
  const vue = "../assets/img/react.jpg";

  const team1 = "../assets/img/team-1-800x800.jpg";
  const team2 = "../assets/img/team-2-800x800.jpg";
  const team3 = "../assets/img/team-3-800x800.jpg";
  const team4 = "../assets/img/team-4-470x470.png";

  // can be one of light or dark
  export let color = "light";

  let promise = Promise.resolve([]);
  let promise_delete = Promise.resolve([]);
  let user_id = "",
    UserEmail = "",
    UserName = "";
  let classData;

  // function handleSubmit() {
  //   promise = submitData();
  //   console.log("Hellooo");
  // }

  function handleButton(value) {
    console.log(value);
    promise_delete = deleteData(value);
  }

  export function handleData() {
    promise = submitData();
  }

  onMount(async () => {
    if (sessionStorage.user_id) {
      user_id = sessionStorage.getItem("user_id");
      UserEmail = sessionStorage.getItem("email");
      UserName = sessionStorage.getItem("username");

      // navigate("/", { replace: true });
    } else console.log("No Session");

    const res = await fetch(
      "http://iot.petra.ac.id:5000/api/user/student/class",
      {
        method: "POST",
        headers: {
          "Content-Type": "application/json; charset=UTF-8",
        },
        body: JSON.stringify({
          user_id,
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
    console.log(json);
    classData = json.data;
    console.log(classData);
    console.log("classData");

    if (json.success === "success") {
      console.log("Yay, berhasil");
      // console.log(json.user);
    }
  });

  async function submitData() {
    const res = await fetch(
      "http://iot.petra.ac.id:5000/api/user/student/class",
      {
        method: "POST",
        headers: {
          "Content-Type": "application/json; charset=UTF-8",
        },
        body: JSON.stringify({
          user_id,
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
    classData = json.data;
    console.log(classData);
    console.log("classData");

    if (json.success === "success") {
      console.log("Yay, berhasil");
      // console.log(json.user);
    }
  }

  let rows;
  // handleSubmit();
</script>

<div
  class="relative flex flex-col min-w-0 break-words w-full mb-6 shadow-lg rounded {color ===
  'light'
    ? 'bg-white'
    : 'bg-red-800 text-white'}"
>
  <div class="rounded-t mb-0 px-4 py-3 border-0">
    <div class="flex flex-wrap items-center">
      <div class="relative w-full px-4 max-w-full flex-grow flex-1">
        <h3
          class="font-semibold text-lg {color === 'light'
            ? 'text-blueGray-700'
            : 'text-white'}"
        >
          Your Class List
        </h3>
      </div>
    </div>
  </div>
  <div class="block w-full overflow-x-auto">
    <!-- Projects table -->
    <table class="items-center w-full bg-transparent border-collapse">
      <thead>
        <tr>
          <th
            class="px-6 align-middle border border-solid py-3 text-xs uppercase border-l-0 border-r-0 whitespace-nowrap font-semibold text-left {color ===
            'light'
              ? 'bg-blueGray-50 text-blueGray-500 border-blueGray-100'
              : 'bg-red-700 text-red-200 border-red-600'}"
          >
            Class Name
          </th>
        </tr>
      </thead>
      <tbody>
        {#if classData}
          {#each classData as data}
            <tr>
              <th
                class="border-t-0 px-6 align-middle border-l-0 border-r-0 text-xs whitespace-nowrap p-4 text-left flex items-center"
              >
                <img
                  src={classlogo}
                  class="h-12 w-12 bg-white rounded-full border"
                  alt="..."
                />
                <span
                  class="ml-3 font-bold {color === 'light'
                    ? 'btext-blueGray-600'
                    : 'text-white'}"
                >
                  {data.class_name}
                </span>
              </th>
            </tr>
          {/each}
        {/if}
      </tbody>
    </table>
  </div>
</div>
