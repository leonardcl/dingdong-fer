<script>
  // core components
  import { link, navigate } from "svelte-routing";
  // import Select from "svelte-select";
  const github = "../assets/img/github.svg";
  const google = "../assets/img/google.svg";
  export let location;

  let email = "",
    password = "",
    username = "",
    role = "",
    login_error_status = "",
    UserID = "";

  const roles = ["Teacher", "Student"];

  function handleSubmit() {
    if (email === "" || password === "" || username === "" || role === "") {
      login_error_status = "Please check yout input again, don't miss it!";
    } else {
      promise = submitData();
    }
  }

  async function submitData() {
    const res = await fetch("http://iot.petra.ac.id:5000/api/user/register", {
      method: "POST",
      headers: {
        "Content-Type": "application/json; charset=UTF-8",
      },
      body: JSON.stringify({
        email,
        password,
        username,
        role,
      }),
    }).then(function (response) {
      console.log(response.status);
      if (response.status != 200) {
        // console.log(response.json().msg);
        login_error_status =
          "Sorry, please try with different e-mail or username";
        sessionStorage.clear();
      } else {
        login_error_status = "";
      }
      return response.json();
    });
    const json = await res;
    console.log(json);
    if (json.success === "success") {
      console.log("Yay, berhasil");
      // console.log(json.user);
      sessionStorage.setItem("user_id", json.user._id);
      sessionStorage.setItem("username", json.user.username);
      sessionStorage.setItem("email", json.user.email);
      sessionStorage.setItem("role", json.user.role);
      UserID = sessionStorage.getItem("user_id");
      navigate("/", { replace: true });
    }

    // UserID = json.user._id;
  }
</script>

<div class="container mx-auto px-4 h-full">
  <div class="flex content-center items-center justify-center h-full">
    <div class="w-full lg:w-6/12 px-4">
      <div
        class="relative flex flex-col min-w-0 break-words w-full mb-6 shadow-lg rounded-lg bg-blueGray-200 border-0"
      >
        <!-- <div class="rounded-t mb-0 px-6 py-6">
          <div class="text-center mb-3">
            <h6 class="text-blueGray-500 text-sm font-bold">
              Sign up with
            </h6>
          </div>
          <div class="btn-wrapper text-center">
            <button
              class="bg-white active:bg-blueGray-50 text-blueGray-700 font-normal px-4 py-2 rounded outline-none focus:outline-none mr-2 mb-1 uppercase shadow hover:shadow-md inline-flex items-center font-bold text-xs ease-linear transition-all duration-150"
              type="button"
            >
              <img alt="..." class="w-5 mr-1" src="{github}" />
              Github
            </button>
            <button
              class="bg-white active:bg-blueGray-50 text-blueGray-700 font-normal px-4 py-2 rounded outline-none focus:outline-none mr-1 mb-1 uppercase shadow hover:shadow-md inline-flex items-center font-bold text-xs ease-linear transition-all duration-150"
              type="button"
            >
              <img alt="..." class="w-5 mr-1" src="{google}" />
              Google
            </button>
          </div>
          <hr class="mt-6 border-b-1 border-blueGray-300" />
        </div> -->
        <div class="flex-auto px-4 lg:px-10 py-10 pt-0 mt-10">
          <div class="text-blueGray-400 text-center mb-6 font-bold">
            <h2 class="text-blueGray-500 text-lg font-bold">
              Register Your Account
            </h2>
          </div>
          <form on:submit|preventDefault={handleSubmit}>
            <div class="relative w-full mb-3">
              <label
                class="block uppercase text-blueGray-600 text-xs font-bold mb-2"
                for="grid-name"
              >
                Username
              </label>
              <input
                bind:value={username}
                id="grid-name"
                class="border-0 px-3 py-3 placeholder-blueGray-300 text-blueGray-600 bg-white rounded text-sm shadow focus:outline-none focus:ring w-full ease-linear transition-all duration-150"
                placeholder="Name"
              />
            </div>

            <div class="relative w-full mb-3">
              <label
                class="block uppercase text-blueGray-600 text-xs font-bold mb-2"
                for="grid-email"
              >
                Email
              </label>
              <input
                bind:value={email}
                id="grid-email"
                type="email"
                class="border-0 px-3 py-3 placeholder-blueGray-300 text-blueGray-600 bg-white rounded text-sm shadow focus:outline-none focus:ring w-full ease-linear transition-all duration-150"
                placeholder="Email"
              />
            </div>

            <div class="relative w-full mb-3">
              <label
                class="block uppercase text-blueGray-600 text-xs font-bold mb-2"
                for="grid-password"
              >
                Password
              </label>
              <input
                bind:value={password}
                id="grid-password"
                type="password"
                class="border-0 px-3 py-3 placeholder-blueGray-300 text-blueGray-600 bg-white rounded text-sm shadow focus:outline-none focus:ring w-full ease-linear transition-all duration-150"
                placeholder="Password"
              />
            </div>

            <div class="relative w-full mb-3">
              <label
                class="block uppercase text-blueGray-600 text-xs font-bold mb-2"
                for="grid-password"
              >
                Role
              </label>

              <select
                bind:value={role}
                id="grid-role"
                class="border-0 px-3 py-3 placeholder-blueGray-300 text-blueGray-600 bg-white rounded text-sm shadow focus:outline-none focus:ring w-full ease-linear transition-all duration-150"
              >
                <option value="none" selected disabled hidden
                  >Select an Option</option
                >
                <option value="teacher">Teacher</option>
                <option value="student">Student</option>
              </select>
            </div>

            <!-- <div>
              <label class="inline-flex items-center cursor-pointer">
                <input
                  id="customCheckLogin"
                  type="checkbox"
                  class="form-checkbox border-0 rounded text-blueGray-700 ml-1 w-5 h-5 ease-linear transition-all duration-150"
                />
                <span class="ml-2 text-sm font-semibold text-blueGray-600">
                  I agree with the
                  <a
                    href="#pablo"
                    on:click={(e) => e.preventDefault()}
                    class="text-red-500"
                  >
                    Privacy Policy
                  </a>
                </span>
              </label>
            </div> -->
            <div class="text-blueGray-400 text-center mb-6 font-bold">
              <h2 class="text-blueGray-500 text-lg font-bold">
                {login_error_status}
              </h2>
            </div>
            <div class="text-center mt-6">
              <button
                class="bg-sky-800 text-white active:bg-sky-600 text-sm font-bold uppercase px-6 py-3 rounded shadow hover:shadow-lg outline-none focus:outline-none mr-1 mb-1 w-full ease-linear transition-all duration-150"
                type="submit"
              >
                Create Account
              </button>
            </div>
          </form>
        </div>
      </div>
    </div>
  </div>
</div>
