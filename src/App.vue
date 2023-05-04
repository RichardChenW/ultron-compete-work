<template>
  <div id="app">
    <data-table></data-table>
  </div>
</template>

<script>
import DataTable from '@/components/DataTable';

export default {
  name: 'App',
  data() {
    return {
      competeData: ""
    }
  },
  components: {
    DataTable
  },
}
</script>

<style></style>
