<script>
    import { headerName } from '../store';
    import Header from '../components/Header.svelte';

    let headerValue;
    headerName.subscribe((data) => {
        headerValue = data;
    })
</script>


<div class="ui">
    <Header headerName={headerValue} />
    <slot />
</div>

