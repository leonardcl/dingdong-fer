<script>
  import { link } from "svelte-routing";
  import { onMount } from "svelte";

  // core components
  import NotificationDropdown from "components/Dropdowns/NotificationDropdown.svelte";
  import UserDropdown from "components/Dropdowns/UserDropdown.svelte";

  let collapseShow = "hidden";

  let teacher_id = "",
    UserEmail = "",
    UserName = "",
    UserRole = "";

  onMount(() => {
    if (sessionStorage.user_id) {
      teacher_id = sessionStorage.getItem("user_id");
      UserEmail = sessionStorage.getItem("email");
      UserName = sessionStorage.getItem("username");
      UserRole = sessionStorage.getItem("role");

      // navigate("/", { replace: true });
    } else {
      console.log("No Session");
    }
  });

  function toggleCollapseShow(classes) {
    collapseShow = classes;
  }

  export let location;
</script>

<nav
  class="md:left-0 md:block md:fixed md:top-0 md:bottom-0 md:overflow-y-auto md:flex-row md:flex-nowrap md:overflow-hidden shadow-xl bg-white flex flex-wrap items-center justify-between relative md:w-64 z-10 py-4 px-6"
>
  <div
    class="md:flex-col md:items-stretch md:min-h-full md:flex-nowrap px-0 flex flex-wrap items-center justify-between w-full mx-auto"
  >
    <!-- Toggler -->
    <button
      class="cursor-pointer text-black opacity-50 md:hidden px-3 py-1 text-xl leading-none bg-transparent rounded border border-solid border-transparent"
      type="button"
      on:click={() => toggleCollapseShow("bg-white m-2 py-3 px-6")}
    >
      <i class="fas fa-bars" />
    </button>
    <!-- Brand -->
    <a
      use:link
      class="md:block text-left md:pb-2 text-blueGray-600 mr-0 inline-block whitespace-nowrap text-sm uppercase font-bold p-4 px-0"
      href="/"
    >
      Ding Dong
    </a>
    <!-- User -->
    <!-- <ul class="md:hidden items-center flex flex-wrap list-none">
      <li class="inline-block relative">
        <NotificationDropdown />
      </li>
      <li class="inline-block relative">
        <UserDropdown />
      </li>
    </ul> -->
    <!-- Collapse -->
    <div
      class="md:flex md:flex-col md:items-stretch md:opacity-100 md:relative md:mt-4 md:shadow-none shadow absolute top-0 left-0 right-0 z-40 overflow-y-auto overflow-x-hidden h-auto items-center flex-1 rounded {collapseShow}"
    >
      <!-- Collapse header -->
      <div
        class="md:min-w-full md:hidden block pb-4 mb-4 border-b border-solid border-blueGray-200"
      >
        <div class="flex flex-wrap">
          <div class="w-6/12">
            <a
              use:link
              class="md:block text-left md:pb-2 text-blueGray-600 mr-0 inline-block whitespace-nowrap text-sm uppercase font-bold p-4 px-0"
              href="/"
            >
              Ding Dong
            </a>
          </div>
          <div class="w-6/12 flex justify-end">
            <button
              type="button"
              class="cursor-pointer text-black opacity-50 md:hidden px-3 py-1 text-xl leading-none bg-transparent rounded border border-solid border-transparent"
              on:click={() => toggleCollapseShow("hidden")}
            >
              <i class="fas fa-times" />
            </button>
          </div>
        </div>
      </div>
      <!-- Form -->
      <!-- <form class="mt-6 mb-4 md:hidden">
        <div class="mb-3 pt-0">
          <input
            type="text"
            placeholder="Search"
            class="border-0 px-3 py-2 h-12 border border-solid border-blueGray-500 placeholder-blueGray-300 text-blueGray-600 bg-white rounded text-base leading-snug shadow-none outline-none focus:outline-none w-full font-normal"
          />
        </div>
      </form> -->

      <!-- Divider -->
      <!-- <hr class="my-4 md:min-w-full" /> -->
      <!-- Heading -->
      {#if UserRole === "teacher"}
        <h6
          class="md:min-w-full text-blueGray-500 text-xs uppercase font-bold block pt-1 pb-4 no-underline"
        >
          Teacher Pages
        </h6>
        <!-- Navigation -->

        <ul class="md:flex-col md:min-w-full flex flex-col list-none">
          <li class="items-center">
            <a
              use:link
              href="/admin/dashboard"
              class="text-xs uppercase py-3 font-bold block {location.href.indexOf(
                '/admin/dashboard'
              ) !== -1
                ? 'text-blue-500 hover:text-blue-600'
                : 'text-blueGray-700 hover:text-blueGray-500'}"
            >
              <i
                class="fas fa-tv mr-2 text-sm {location.href.indexOf(
                  '/admin/dashboard'
                ) !== -1
                  ? 'opacity-75'
                  : 'text-blueGray-300'}"
              />
              Dashboard
            </a>
          </li>

          <li class="items-center">
            <a
              use:link
              href="/admin/classsetting"
              class="text-xs uppercase py-3 font-bold block {location.href.indexOf(
                '/admin/classsetting'
              ) !== -1
                ? 'text-blue-500 hover:text-blue-600'
                : 'text-blueGray-700 hover:text-blueGray-500'}"
            >
              <i
                class="fas fa-tv mr-2 text-sm {location.href.indexOf(
                  '/admin/classsetting'
                ) !== -1
                  ? 'opacity-75'
                  : 'text-blueGray-300'}"
              />
              Class
            </a>
          </li>

          <li class="items-center">
            <a
              use:link
              href="/admin/schedulesetting"
              class="text-xs uppercase py-3 font-bold block {location.href.indexOf(
                '/admin/schedulesetting'
              ) !== -1
                ? 'text-blue-500 hover:text-blue-600'
                : 'text-blueGray-700 hover:text-blueGray-500'}"
            >
              <i
                class="fas fa-calendar mr-2 text-sm {location.href.indexOf(
                  '/admin/schedulesetting'
                ) !== -1
                  ? 'opacity-75'
                  : 'text-blueGray-300'}"
              />
              Class Schedule
            </a>
          </li>

          <li class="items-center">
            <a
              use:link
              href="/admin/studentsetting"
              class="text-xs uppercase py-3 font-bold block {location.href.indexOf(
                '/admin/studentsetting'
              ) !== -1
                ? 'text-blue-500 hover:text-blue-600'
                : 'text-blueGray-700 hover:text-blueGray-500'}"
            >
              <i
                class="fas fa-user-friends mr-2 text-sm {location.href.indexOf(
                  '/admin/studentsetting'
                ) !== -1
                  ? 'opacity-75'
                  : 'text-blueGray-300'}"
              />
              Student
            </a>
          </li>

          <!-- <li class="items-center">
            <a
              use:link
              href="/admin/settings"
              class="text-xs uppercase py-3 font-bold block {location.href.indexOf(
                '/admin/settings'
              ) !== -1
                ? 'text-blue-500 hover:text-blue-600'
                : 'text-blueGray-700 hover:text-blueGray-500'}"
            >
              <i
                class="fas fa-tools mr-2 text-sm {location.href.indexOf(
                  '/admin/settings'
                ) !== -1
                  ? 'opacity-75'
                  : 'text-blueGray-300'}"
              />
              Settings
            </a>
          </li>

          <li class="items-center">
            <a
              use:link
              href="/admin/tables"
              class="text-xs uppercase py-3 font-bold block {location.href.indexOf(
                '/admin/tables'
              ) !== -1
                ? 'text-blue-500 hover:text-blue-600'
                : 'text-blueGray-700 hover:text-blueGray-500'}"
            >
              <i
                class="fas fa-table mr-2 text-sm {location.href.indexOf(
                  '/admin/tables'
                ) !== -1
                  ? 'opacity-75'
                  : 'text-blueGray-300'}"
              />
              Tables
            </a>
          </li>

          <li class="items-center">
            <a
              use:link
              href="/admin/maps"
              class="text-xs uppercase py-3 font-bold block {location.href.indexOf(
                '/admin/maps'
              ) !== -1
                ? 'text-blue-500 hover:text-blue-600'
                : 'text-blueGray-700 hover:text-blueGray-500'}"
            >
              <i
                class="fas fa-map-marked mr-2 text-sm {location.href.indexOf(
                  '/admin/maps'
                ) !== -1
                  ? 'opacity-75'
                  : 'text-blueGray-300'}"
              />
              Maps
            </a>
          </li> -->
        </ul>
      {/if}
      {#if UserRole === "student"}
        <h6
          class="md:min-w-full text-blueGray-500 text-xs uppercase font-bold block pt-1 pb-4 no-underline"
        >
          Student Pages
        </h6>
        <!-- Navigation -->

        <ul class="md:flex-col md:min-w-full flex flex-col list-none">
          <li class="items-center">
            <a
              use:link
              href="/student/classshow"
              class="text-xs uppercase py-3 font-bold block {location.href.indexOf(
                '/admin/classsetting'
              ) !== -1
                ? 'text-blue-500 hover:text-blue-600'
                : 'text-blueGray-700 hover:text-blueGray-500'}"
            >
              <i
                class="fas fa-tv mr-2 text-sm {location.href.indexOf(
                  '/admin/classsetting'
                ) !== -1
                  ? 'opacity-75'
                  : 'text-blueGray-300'}"
              />
              Class
            </a>
          </li>

          <li class="items-center">
            <a
              use:link
              href="/student/schedulesetting"
              class="text-xs uppercase py-3 font-bold block {location.href.indexOf(
                '/admin/schedulesetting'
              ) !== -1
                ? 'text-blue-500 hover:text-blue-600'
                : 'text-blueGray-700 hover:text-blueGray-500'}"
            >
              <i
                class="fas fa-calendar mr-2 text-sm {location.href.indexOf(
                  '/admin/schedulesetting'
                ) !== -1
                  ? 'opacity-75'
                  : 'text-blueGray-300'}"
              />
              Class Schedule
            </a>
          </li>
        </ul>
      {/if}

      <!-- Divider -->
      <hr class="my-4 md:min-w-full" />
      <!-- Heading -->
      <!-- <h6
        class="md:min-w-full text-blueGray-500 text-xs uppercase font-bold block pt-1 pb-4 no-underline"
      >
        Auth Layout Pages
      </h6> -->
      <!-- Navigation -->

      <!-- <ul class="md:flex-col md:min-w-full flex flex-col list-none md:mb-4">
        <li class="items-center">
          <a
            use:link
            class="text-blueGray-700 hover:text-blueGray-500 text-xs uppercase py-3 font-bold block"
            href="/auth/login"
          >
            <i class="fas fa-fingerprint text-blueGray-300 mr-2 text-sm" />
            Login
          </a>
        </li>

        <li class="items-center">
          <a
            use:link
            class="text-blueGray-700 hover:text-blueGray-500 text-xs uppercase py-3 font-bold block"
            href="/auth/register"
          >
            <i class="fas fa-clipboard-list text-blueGray-300 mr-2 text-sm" />
            Register
          </a>
        </li>
      </ul> -->

      <!-- Divider -->
      <!-- <hr class="my-4 md:min-w-full" /> -->
      <!-- Heading -->
      <!-- <h6
        class="md:min-w-full text-blueGray-500 text-xs uppercase font-bold block pt-1 pb-4 no-underline"
      >
        No Layout Pages
      </h6> -->
      <!-- Navigation -->

      <!-- <ul class="md:flex-col md:min-w-full flex flex-col list-none md:mb-4">
        <li class="items-center">
          <a
            use:link
            class="text-blueGray-700 hover:text-blueGray-500 text-xs uppercase py-3 font-bold block"
            href="/landing"
          >
            <i class="fas fa-newspaper text-blueGray-300 mr-2 text-sm" />
            Landing Page
          </a>
        </li>

        <li class="items-center">
          <a
            use:link
            class="text-blueGray-700 hover:text-blueGray-500 text-xs uppercase py-3 font-bold block"
            href="/profile"
          >
            <i class="fas fa-user-circle text-blueGray-300 mr-2 text-sm" />
            Profile Page
          </a>
        </li>
      </ul> -->

      <!-- Divider -->
      <!-- <hr class="my-4 md:min-w-full" /> -->
      <!-- Heading -->
      <!-- <h6
        class="md:min-w-full text-blueGray-500 text-xs uppercase font-bold block pt-1 pb-4 no-underline"
      >
        Documentation
      </h6> -->
      <!-- Navigation -->
      <!-- <ul class="md:flex-col md:min-w-full flex flex-col list-none md:mb-4">
        <li class="inline-flex">
          <a
            href="https://www.creative-tim.com/learning-lab/tailwind/svelte/colors/notus"
            target="_blank"
            class="text-blueGray-700 hover:text-blueGray-500 text-sm block mb-4 no-underline font-semibold"
          >
            <i class="fas fa-paint-brush mr-2 text-blueGray-300 text-base" />
            Styles
          </a>
        </li>

        <li class="inline-flex">
          <a
            href="https://www.creative-tim.com/learning-lab/tailwind/svelte/alerts/notus"
            target="_blank"
            class="text-blueGray-700 hover:text-blueGray-500 text-sm block mb-4 no-underline font-semibold"
          >
            <i class="fab fa-css3-alt mr-2 text-blueGray-300 text-base" />
            CSS Components
          </a>
        </li>

        <li class="inline-flex">
          <a
            href="https://www.creative-tim.com/learning-lab/tailwind/angular/overview/notus"
            target="_blank"
            class="text-blueGray-700 hover:text-blueGray-500 text-sm block mb-4 no-underline font-semibold"
          >
            <i class="fab fa-angular mr-2 text-blueGray-300 text-base" />
            Angular
          </a>
        </li>

        <li class="inline-flex">
          <a
            href="https://www.creative-tim.com/learning-lab/tailwind/js/overview/notus"
            target="_blank"
            class="text-blueGray-700 hover:text-blueGray-500 text-sm block mb-4 no-underline font-semibold"
          >
            <i class="fab fa-js-square mr-2 text-blueGray-300 text-base" />
            Javascript
          </a>
        </li>

        <li class="inline-flex">
          <a
            href="https://www.creative-tim.com/learning-lab/tailwind/nextjs/overview/notus"
            target="_blank"
            class="text-blueGray-700 hover:text-blueGray-500 text-sm block mb-4 no-underline font-semibold"
          >
            <i class="fab fa-react mr-2 text-blueGray-300 text-base" />
            NextJS
          </a>
        </li>

        <li class="inline-flex">
          <a
            href="https://www.creative-tim.com/learning-lab/tailwind/react/overview/notus"
            target="_blank"
            class="text-blueGray-700 hover:text-blueGray-500 text-sm block mb-4 no-underline font-semibold"
          >
            <i class="fab fa-react mr-2 text-blueGray-300 text-base" />
            React
          </a>
        </li>

        <li class="inline-flex">
          <a
            href="https://www.creative-tim.com/learning-lab/tailwind/svelte/overview/notus"
            target="_blank"
            class="text-blueGray-700 hover:text-blueGray-500 text-sm block mb-4 no-underline font-semibold"
          >
            <i class="fas fa-link mr-2 text-blueGray-300 text-base" />
            Svelte
          </a>
        </li>

        <li class="inline-flex">
          <a
            href="https://www.creative-tim.com/learning-lab/tailwind/vue/overview/notus"
            target="_blank"
            class="text-blueGray-700 hover:text-blueGray-500 text-sm block mb-4 no-underline font-semibold"
          >
            <i class="fab fa-vuejs mr-2 text-blueGray-300 text-base" />
            VueJS
          </a>
        </li>
      </ul> -->
    </div>
  </div>
</nav>
