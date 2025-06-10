<script>
    export let message;

    const className = message.role == 'assistant' ? 'label' : 'yellow basic label';
</script>

<div class="event">
    <div class="{className}" data-text="{message.author}"></div>
    {#if message.isLoading}
        <!-- public 폴더에 있으니까 절대경로로 바로 참조 -->
        <img class="ui image" style="padding: 5px;" src="/assets/images/icons8-loading.gif" alt="loading"/>
    {:else}
        <div class="content">
            {message.text}
        </div>        
    {/if}
</div>
