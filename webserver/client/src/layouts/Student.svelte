<script>
  import { Router, Route } from "svelte-routing";

  // components for this layout
  import AdminNavbar from "components/Navbars/AdminNavbar.svelte";
  import Sidebar from "components/Sidebar/Sidebar.svelte";
  import HeaderStats from "components/Headers/HeaderStats.svelte";
  import FooterAdmin from "components/Footers/FooterAdmin.svelte";

  // pages for this layout
  import Dashboard from "views/student/Dashboard.svelte";
  import Class from "views/student/Class.svelte";
  import ClassShow from "views/student/ClassShow.svelte";
  import Settings from "views/student/Settings.svelte";
  //   import ClassSetting from "views/student/ClassSetting.svelte";
  import ScheduleSetting from "views/student/ScheduleSetting.svelte";
  import StudentSetting from "views/student/StudentSetting.svelte";
  import Tables from "views/student/Tables.svelte";
  import Maps from "views/student/Maps.svelte";

  export let location;
  export let admin = "";
</script>

<div>
  <Sidebar {location} />
  <div class="relative md:ml-64 bg-blueGray-100">
    <AdminNavbar />
    <HeaderStats />
    <div class="px-4 md:px-10 mx-auto w-full -m-24">
      <Router url="student">
        <Route path="classshow" component={ClassShow} />
        <Route path="schedulesetting" component={ScheduleSetting} />           
      </Router>
      <FooterAdmin />
    </div>
  </div>
</div>
