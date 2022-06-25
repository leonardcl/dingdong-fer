<script>
  // core components
  import CardStudentRegister from "components/Cards/CardStudentRegister.svelte";
  import CardStudentList from "components/Cards/CardStudentList.svelte";
  import CardProfile from "components/Cards/CardProfile.svelte";
  export let location;
</script>

<div class="flex flex-wrap">
  <div class="w-full lg:w-full px-4">
    <CardStudentRegister />
  </div>
  <!-- <div class="w-full mb-12 px-4">
    <CardStudentList color="light" />
  </div> -->
  <!-- <div class="w-full lg:w-4/12 px-4">
    <CardProfile />
  </div> -->
</div>
