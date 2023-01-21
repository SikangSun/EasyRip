<script>
    import "../app.css";
    import { fade, fly } from 'svelte/transition';
    
  </script>
  
  <div in:fade>
  <slot />
  </div>