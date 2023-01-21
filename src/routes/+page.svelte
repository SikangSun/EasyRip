<script>
    import toast, { Toaster } from 'svelte-french-toast';
    import { onMount } from 'svelte';
    import axios from 'axios';

    let url = ""
    let server = "http://127.0.0.1:8000"
    let videoFound = true;
    onMount(() => {
        toast.success('Successfully toasted!')
    })

    const downloadVideo = () => {
        console.log("asdf")
    }

    const downloadAudio = () => {

    }
    const searchVideo = async (url) => {
        const i = url.indexOf("?v=");
        const v = url.substr(i+3);
        console.log(v);
        const res = await axios.get(`${server}/get_metadata?v=${v}`);
        console.log(res.data)
    }
</script>

<!-- screen box div -->
<div class="flex flex-col justify-center items-center
            h-screen w-screen bg-[#f7f7f7]" >
    <div class="min-w-min w-1/2 max-w-md flex justify-center"
    >
        EasyRip - The Easiest Way to Rip Youtube Videos 
    </div>
    <!-- main box div -->
    <div class="min-h-max h-1/2 max-h-96
                min-w-fit w-1/2 max-w-md
                relative sm outline outline-gray-500 hover:outline-4 hover:outline-black transition-all
                shadow-[60px_120px_60px_-15px_rgba(255,255,255,0.8)] hover:shadow-[0_35px_60px_-15px_rgba(255,0,0,0.3)] z-10 duration-500
                bg-white rounded p-4 m-3">

        <!-- url search div -->
        <form class="flex flex-row"> 
            <input class="bg-gray-50 border border-gray-300 text-gray-900 text-sm rounded-lg
                            focus:ring-blue-500 focus:border-blue-500 block w-10/12 p-2.5
                            " 
                             placeholder="URL Here" type="URL" bind:value="{url}" />
            <input class="btn ml-2"
                            on:click= {() => searchVideo(url)}
                            type="submit" value="Search"/>
        </form>
        {#if videoFound == true}
        <div class="h-2/3 bg-slate-500 overflow-hidden">
            adsf
        </div>
        {/if}
        <!-- download buttons -->
        <div class="absolute bottom-0 mb-4 w-11/12
                    flex flex-row justify-between">
            <a class="btn cursor-pointer select-none">
                Download Audio
            </a>

            <button on:click={downloadVideo} class="btn ml-2">
                Download Video
                <select >
                    <option disabled selected value> Resolution </option>
                    <option value="volvo">Volvo</option>
                    <option value="saab">Saab</option>
                    <option value="mercedes">Mercedes</option>
                    <option value="audi">Audi</option>
                  </select>
            </button>
        </div>

    </div>    
    
</div>

<Toaster />