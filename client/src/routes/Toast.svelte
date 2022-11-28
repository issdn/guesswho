<script lang="ts">
    import { slide } from "svelte/transition";
    import { removeToast } from "../stores";
    const sleep = (time: number) => new Promise(res => setTimeout(res, time));
  
    const types = {
      warning: "bg-red-500",
      success: "bg-green-500"
    };
  
    const btnTypes = {
      warning: "hover:bg-red-400",
      success: "hover:bg-green-400"
    };
  
    export let index: string;
    export let message = "";
    export let visible: boolean;
    export let type: "warning" | "success" = "warning";
  
    const close = () => {
      visible = false;
      sleep(1000).then(() => removeToast(index));
    };
  </script>
  
  {#if visible}
  <div transition:slide class="md:w-96 pointer-events-auto mb-4 font-['Mouse_Memoirs']">
    <div class="{types[type]} flex justify-center items-center p-4 text-white text-2xl text-center rounded-xl">
        <p class="w-full">{message}</p>
      <div class="flex justify-end items-center text-4xl">
        <div on:click={close} class="{btnTypes[type]} cursor-pointer ml-2 w-fit h-fit rounded-md px-2">
          <i class="fa-solid fa-xmark"></i>
        </div>
      </div>
    </div>
  </div>
  {/if}
  