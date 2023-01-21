<script>
    let url = ""

</script>

<!-- screen box div -->
<div class="flex justify-center items-center
            h-screen w-screen">
    <!-- main box div -->
    <div class="min-h-max h-1/2 max-h-96
                min-w-fit w-1/2 max-w-md
                relative sm outline outline-black rounded p-4">

        <!-- url search div -->
        <div class="flex flex-row"> 
            <input class="bg-gray-50 border border-gray-300 text-gray-900 text-sm rounded-lg
                            focus:ring-blue-500 focus:border-blue-500 block w-10/12 p-2.5
                            " 
                             name="email" placeholder="URL Here" type="URL" bind:value="{url}" />
            <button class="btn
                            ml-2"
                            on:click= {() => console.log(url)}> Search</button>
        </div>

        <!-- download buttons -->
        <div class="absolute bottom-0 mb-4 w-11/12
                    flex flex-row justify-between">
            <a class="btn cursor-pointer select-none">
                Download Audio
            </a>

            <button class="btn">
                Download Video
            </button>
        </div>

    </div>    
    
</div>