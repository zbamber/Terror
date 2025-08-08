<script lang="ts">
 import CalendarIcon from "@lucide/svelte/icons/calendar";
 import {
  DateFormatter,
  type DateValue,
  getLocalTimeZone,
  today,
  CalendarDate
 } from "@internationalized/date";
 import { cn } from "$lib/utils.js";
 import { buttonVariants } from "$lib/components/ui/button/index.js";
 import { Calendar } from "$lib/components/ui/calendar/index.js";
 import * as Popover from "$lib/components/ui/popover/index.js";
 import * as Select from "$lib/components/ui/select/index.js";
 
 const endOfData = new CalendarDate(2017, 12, 31)
 const startOfData = new CalendarDate(1970, 1, 1)

 const years = [];
 for (let year = endOfData.year; year >= startOfData.year; year--) {
   years.push({ value: `${year}`, label:`${year}` });
 }

 const df = new DateFormatter("en-US", {
  dateStyle: "long"
 });

 let {
   value = $bindable(),
    prompt
 } = $props();

 const selectedYear = $derived(value ? `${value.year}` : undefined);

 const valueString = $derived(
  value ? df.format(value.toDate(getLocalTimeZone())) : ""
 );
</script>
 
<Popover.Root>
 <Popover.Trigger
  class={cn(
   buttonVariants({
    variant: "outline",
    class: "w-[280px] justify-start text-left font-normal"
   }),
   !value && "text-muted-foreground"
  )}
 >
  <CalendarIcon class="mr-2 size-4" />
  {value ? df.format(value.toDate(getLocalTimeZone())) : prompt}
 </Popover.Trigger>
 <Popover.Content class="flex w-auto flex-col space-y-2 p-2">
  <Select.Root
   type="single"
   bind:value={
    () => valueString,
    (v) => {
     if (!v) return;
     value = new CalendarDate(Number.parseInt(v), value.month, value.day);
    }
   }
  >
   <Select.Trigger>
    Year
   </Select.Trigger>
   <Select.Content>
    {#each years as year (year.value)}
     <Select.Item value={`${year.value}`}>{year.label}</Select.Item>
    {/each}
   </Select.Content>
  </Select.Root>
  
  <div class="rounded-md border">
   <Calendar type="single" bind:value minValue={startOfData} maxValue={endOfData}/>
  </div>
 </Popover.Content>
</Popover.Root>