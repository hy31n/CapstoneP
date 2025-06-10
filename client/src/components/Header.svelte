<script>
    export let headerName; 

</script>

<style>
  .header-container {
    max-width: 800px;
    margin: 0 auto;
    padding: 40px 20px 0px 0px;
    text-align: left;
  }
  
  .header-logo {
    max-height:130px;
    width: auto;
  }
</style>

<div class="header-container">
        <img src={headerName} alt="Logo" class="header-logo" />
</div>