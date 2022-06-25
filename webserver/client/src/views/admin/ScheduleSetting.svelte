<script>
  // core components
  import CardScheduleRegister from "components/Cards/CardScheduleRegister.svelte";
  import CardScheduleList from "components/Cards/CardScheduleList.svelte";
  import CardProfile from "components/Cards/CardProfile.svelte";
  export let location;
</script>

<div class="flex flex-wrap">
  <div class="w-full lg:w-full px-4">
    <CardScheduleRegister />
  </div>
</div>
