<script lang="ts">
 import * as AlertDialog from "$lib/components/ui/alert-dialog/index.js";
 import {
  DateFormatter,
  getLocalTimeZone,
  CalendarDate
 } from "@internationalized/date";
 let { 
    open = $bindable(),
    startDate = $bindable(),
    endDate = $bindable(),
    getAttacks,
    calToISO
} = $props();

const df = new DateFormatter("en-GB", {
  dateStyle: "short"
});

const endOfData = new CalendarDate(2017, 12, 31)
const startOfData = new CalendarDate(1970, 1, 1)

const endOfStart = $derived(startDate.add({ years: 2 }));
const startOfEnd = $derived(endDate.subtract({ years: 2 }));

</script>
 
<AlertDialog.Root bind:open>
 <AlertDialog.Content>
  <AlertDialog.Header>
   <AlertDialog.Title>The maximum range is 2 years!</AlertDialog.Title>
   <AlertDialog.Description>
    This is so your computer can render a smooth experience. <br />
    Select either of the suggested ranges or cancel to try again with a new range which is less than 2 years.
   </AlertDialog.Description>
  </AlertDialog.Header>
  <AlertDialog.Footer>
   <AlertDialog.Cancel>Cancel</AlertDialog.Cancel>
    <AlertDialog.Action
    onclick={() => {
        endDate = endOfStart
        getAttacks(calToISO(startDate), calToISO(endOfStart));
        open = false;
        }}>
    {df.format(startDate.toDate(getLocalTimeZone())) + ' to ' + df.format(endOfStart.toDate(getLocalTimeZone()))}
    </AlertDialog.Action>
    <AlertDialog.Action
    onclick={() => {
        startDate = startOfEnd
        getAttacks(calToISO(startOfEnd), calToISO(endDate));
        open = false;
        }}>
    {df.format(startOfEnd.toDate(getLocalTimeZone())) + ' to ' + df.format(endDate.toDate(getLocalTimeZone()))}
    </AlertDialog.Action>
  </AlertDialog.Footer>
 </AlertDialog.Content>
</AlertDialog.Root>