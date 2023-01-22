<script>
    import toast, { Toaster } from 'svelte-french-toast';
    import {fade, fly} from "svelte/transition"
    import { onMount } from 'svelte';
    import axios from "axios";
    import bytes from "bytes";

    let isPageLoaded = true;
    

    let url = "";
        $: videoID = url.substring(url.indexOf("?v=") + 3, url.indexOf("&") ? url.indexOf("&") : url.length);
    let md = {};
    let videoFound = false;
    let tn = "";
 

    let showVideoList = false;
    let videoList = ["1","asdfasfasdfsadf","3","4","5"];
    let defaultVideoID = "";

    let showAudioList = false;
    let audioList = ["1","asdfasfasdfsadf","3","4","5"];
    let defaultAudioID = ""

    let server = "http://127.0.0.1:8000/"


    let sponsor = false;
    let timestamp = false;
    let filename = "";

    onMount(() => {
        toast('Welcome!', {icon: '👋'})
    })


    const searchVideo = async (url) => {
        isPageLoaded = false;
        console.log(isPageLoaded)
        const i = url.indexOf("?v=");
        const v = url.substr(i+3);
        console.log(v);
        const res = await axios.get(`${server}get_metadata?v=${v}`);
        console.log(res)
 

        if (res.status == 200) {
        md = res.data
        videoFound = true;
        //care svelte array changes
        videoList = md.formats.filter(x => x.is_video == true);
        audioList = md.formats.filter(x => x.is_video == false);
        tn = `https://i.ytimg.com/vi/${videoID}/mqdefault.jpg`;
        defaultVideoID = videoList.filter(x => x.is_default == true)[0].id
        defaultAudioID = audioList[audioList.length - 1].id
        console.log("success")
        }
        else {
            //if fails {}
        }
        isPageLoaded = true;
      
    }

</script>

<!-- screen box div -->
<div class="flex flex-col justify-center items-center
            h-screen w-screen bg-[#f7f7f7]" >
    <div class="font-serif text-center text-2xl inline-block min-w-min w-1/2 max-w-1xljustify-center "
    >
        EasyRip - The Easiest Way to Rip Youtube Videos 
    </div>
    <!-- main box div -->
    <div class="relative flex flex-col justify-between
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
                             placeholder="URL Here" type="URL" bind:value="{url}" on:input={() => {md = {}; videoFound = false;}}/>
            <input class="btn ml-2"
                            on:click= {() => searchVideo(url)}
                            type="submit" value="Search"/>
        </form>
        
        {#if !isPageLoaded}
            <div transition:fade class="absolute right-[150px] bottom-1/4">
                <div class="text-center">
                <img src="/loading.svg" alt="loading...">
                <span class="text-sm">Looking very hard!!!</span> 
                </div>
            </div>
        {:else if videoFound == true}
        <!-- descriptions and options -->
        <div  transition:fade="{{delay: 500}}" class="flex flex-col h-full items-start content-start p-2">
            <!-- thumnail and description -->
            <div class="flex flex-row w-full h-1/2 justify-between pt-2">
                <div class="w-1/2">
                    <img class="h-full rounded outline outline-4 outline-red-500" src={tn} alt="Thumbnail">
                </div>
                <div class="w-1/2 flex justify-start flex-col pl-4 ">
                    <div class="text-md p-1/2">
                        Author: {md.uploader}
                    </div>
                    <div class="text-md p-1/2">
                        Date Published: {md.upload_date.substring(0,4)}-{md.upload_date.substring(4,6)}-{md.upload_date.substring(6)} 
                    </div>
                    <div class="text-md p-1/2">
                        Duration: {#if md.duration_string.indexOf(":") >= 0} {md.duration_string} minutes {:else} {md.duration_string} seconds {/if}
                    </div>
                    <div class="text-md p-1/2">
                        Likes: {md.like_count}
                    </div>
                    <div class="text-md p-1/2">
                        Views: {md.view_count}
                    </div>
                </div>
            </div>

            <div class="inline overflow-hidden whitespace-nowrap w-full font-bold text-2xl my-2 text-ellipsis">
                {md.title}
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
                    <input type="text" bind:value={filename} maxlength="20" placeholder="default" class="outline rounded-sm pl-1">
                </label>
            </div>


        </div>







        <!-- download buttons -->
        <div  transition:fade="{{delay: 500}}"  class="bottom-0 mb-4 w-full
                    flex flex-row justify-between">
            
            <!-- download audio -->
            <div class="relative flex flex-col justify-start mr-2">
                <a href={`${server}get_video?v=${videoID}&f=${defaultAudioID}`} class="btn">
                    <div class="inline-block">
                        Download Audio
                        <button on:click="{() => showAudioList = !showAudioList}" class="btn p-1 pl-2 pr-2">{#if showAudioList == true} ↑ {:else} ↓ {/if}</button>
                    </div>
                </a>
                {#if showAudioList == true}
                    <div  transition:fly="{{x:-200, duration: 500}}" class="absolute w-fit max-w-[300px] h-fit top-12 outline outline-gray-500 bg-slate-50 rounded-sm pr-0">
                        {#each audioList as audio}
                            <div class="text-xs hover:bg-slate-200">
                                <a href={`${server}get_video?v=${videoID}&f=${audio.id}`}>
                                 audio ({audio.ext}) {#if audio.filesize} ({bytes.format(audio.filesize,  {decimalPlaces: 1})}) {/if}
                                </a>
                            </div>
                        {/each}
                    </div>
                {/if}
            </div>





            <!-- download video -->
            <div class="relative flex flex-col justify-start">
                <a href={`${server}get_video?v=${videoID}&f=${defaultVideoID}`} class="btn">
                    <div class="inline-block">
                        Download Video
                        <button on:click="{() => showVideoList = !showVideoList}" class="btn p-1 pl-2 pr-2"> {#if showVideoList == true} ↑ {:else} ↓ {/if}</button>
                    </div>
                </a>
            {#if showVideoList == true}

                <div transition:fly="{{x:200, duration: 500}}" class="absolute w-fit max-w-[300px] h-fit top-12 outline outline-gray-500 bg-slate-50 rounded-sm pr-0">
                    {#each videoList as video}
                        <div  class="text-xs hover:bg-slate-200">
                            <a href={`${server}get_video?v=${videoID}&f=${video.id}`}>
                            {video.desc}({video.ext}) {#if video.filesize} ({bytes.format(video.filesize,  {decimalPlaces: 1})}) {/if}
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