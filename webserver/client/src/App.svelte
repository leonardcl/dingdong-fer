<!-- App.svelte -->
<script>
  import { Router, Route } from "svelte-routing";

  // Admin Layout
  import Admin from "./layouts/Admin.svelte";
  // Student Layout
  import Student from "./layouts/Student.svelte";
  // Auth Layout
  import Auth from "./layouts/Auth.svelte";

  // No Layout Pages
  import Index from "./views/Index.svelte";
  import Landing from "./views/Landing.svelte";
  import Profile from "./views/Profile.svelte";

  export let url = "";
</script>

<!-- <Router url="{url}" basename={'/dingdong'}> -->
<Router url="{url}" basename={'/dingdong'}>
  <!-- admin layout -->
  <Route path="admin/*admin" component="{Admin}" />
  <!-- student layout -->
  <Route path="student/*student" component="{Student}" />                      
  <!-- auth layout -->
  <Route path="auth/*auth" component="{Auth}" />
  <!-- no layout pages -->
  <Route path="/" component="{Index}" />
</Router>
                                                                               