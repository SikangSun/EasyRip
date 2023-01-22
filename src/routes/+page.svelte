<script>
    import toast, { Toaster } from 'svelte-french-toast';
    import {fade, fly} from "svelte/transition"
    import { onMount } from 'svelte';
    import axios from 'axios';

    let url = "";
        $: video = url.substring(url.indexOf("?v=") + 3);
    
    let showVideoList = false;
    let videoList = ["1","asdfasfasdfsadf","3","4","5"];

    let showAudioList = false;
    let audioList = ["1","asdfasfasdfsadf","3","4","5"];

    let server = "http://127.0.0.1:8000/"
    let videoFound = true;

    let sponsor = false;
    let timestamp = false;
    onMount(() => {
        toast.success('Successfully toasted!')
    })

    const downloadVideo = async () => {
        // const res = await axios.get(`${server}?v=${video}`, {responseType: 'blob'});
        // console.log("haha")

        // var binaryData = [];
        // binaryData.push(res.data);
        // const href = URL.createObjectURL(new Blob(binaryData, {type: "application/text"}));

        // // create "a" HTML element with href to file & click
        // const link = document.createElement('a');
        // link.href = href;
        // link.setAttribute('download', 'name.mp4'); //or any other extension
        // document.body.appendChild(link);
        // link.click();

        // // clean up "a" element & remove ObjectURL
        // document.body.removeChild(link);
        // URL.revokeObjectURL(href);
    }

    const downloadAudio = async () => {
      
    }
    const searchVideo = async (url) => {
        const i = url.indexOf("?v=");
        const v = url.substr(i+3);
        console.log(v);
        const res = await axios.get(`${server}get_metadata?v=${v}`);
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
    <div class="flex flex-col justify-between
                h-[400px] 
                w-[500px]
                outline outline-gray-500 hover:outline-4 hover:outline-black transition-all
                shadow-[60px_120px_60px_-15px_rgba(255,255,255,0.8)] hover:shadow-[0_35px_60px_-15px_rgba(255,0,0,0.3)] z-10 duration-500
                bg-white rounded p-4 m-3 pb-0">
                
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
        <!-- descriptions and options -->
        <div class="flex flex-col h-full items-start content-start p-2">
            <!-- thumnail and description -->
            <div class="flex flex-row w-full h-1/2 justify-between ">
                <div class="w-1/2">
                    <img class="h-full" src="https://i.ytimg.com/vi/-JSj7N4lH3s/mqdefault.jpg" alt="Thumbnail">
                </div>
                <div class="w-1/2 flex justify-start flex-col pl-2">
                    <div class="text-md p-1">
                        Author: 
                    </div>
                    <div class="text-md p-1">
                        Date Published:
                    </div>
                    <div class="text-md p-1">
                        Duration:
                    </div>
                    <div class="text-md p-1">
                        Likes:
                    </div>
                </div>
            </div>

            <div class="w-full font-bold text-2xl my-2">
                Title: []
            </div>

            <div class="w-full flex flex-row justify-between my-2">
                <div>
                    <label>
                        <input type="checkbox"on:change={() => sponsor = !sponsor}/>
                        Remove Sponsors
                    </label>
                </div>
            
                <div>
                    <label>
                        <input type="checkbox"on:change={() => timestamp = !timestamp}/>
                        Timestamp
                    </label>
                    <input class="outline rounded-sm w-5" type="number" value="00">
                </div>

            </div>


            <div>
                <label >
                    Name my downloaded file: 
                    <input type="text" maxlength="15" placeholder="default" class="outline rounded-sm pl-1">
                </label>
            </div>


        </div>







        <!-- download buttons -->
        <div class="bottom-0 mb-4 w-full
                    flex flex-row justify-between">
            
            <!-- download audio -->
            <div class="relative flex flex-col justify-start mr-2">
                <a href={``} class="btn">
                    <div class="inline-block">
                        Download Audio
                        <button on:click="{() => showAudioList = !showAudioList}" class="btn p-1 pl-2 pr-2">{#if showAudioList == true} ↑ {:else} ↓ {/if}</button>
                    </div>
                </a>
                {#if showAudioList == true}
                    <div  transition:fly="{{x:-200, duration: 500}}" class="absolute w-fit h-fit top-12 outline outline-gray-500 bg-slate-50 rounded-sm pr-0">
                        {#each audioList as audio}
                            <div class="hover:bg-slate-200">
                                <a href="">
                                 {audio}
                                </a>
                            </div>
                        {/each}
                    </div>
                {/if}
            </div>





            <!-- download video -->
            <div class="relative flex flex-col justify-start">
                <a href={``} class="btn">
                    <div class="inline-block">
                        Download Video
                        <button on:click="{() => showVideoList = !showVideoList}" class="btn p-1 pl-2 pr-2"> {#if showVideoList == true} ↑ {:else} ↓ {/if}</button>
                    </div>
                </a>
            {#if showVideoList == true}

                <div transition:fly="{{x:200, duration: 500}}" class="absolute w-fit h-fit top-12 outline outline-gray-500 bg-slate-50 rounded-sm pr-0">
                    {#each videoList as video}
                        <div  class="hover:bg-slate-200">
                            <a href="">
                            {video}
                            </a>
                        </div>
                    {/each}
                </div>
                
            {/if}
            </div>
        </div>
        {/if}
    </div>    
    
</div>

<Toaster />