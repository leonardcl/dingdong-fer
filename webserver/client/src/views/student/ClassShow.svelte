<script>
  // core components
  import CardClassStudent from "components/Cards/CardClassStudent.svelte";
  import CardScheduleList from "components/Cards/CardScheduleList.svelte";
  import CardProfile from "components/Cards/CardProfile.svelte";
  export let location;
</script>

<div class="flex flex-wrap">
  <div class="w-full lg:w-full px-4">
    <CardClassStudent />
  </div>
  <!-- <div class="w-full mb-12 px-4">
    <CardClassList color="light" />
  </div> -->
  <!-- <div class="w-full lg:w-4/12 px-4">
    <CardProfile />
  </div> -->
</div>
