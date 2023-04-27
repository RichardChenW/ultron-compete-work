<template>
  <div id="app">
    <data-table></data-table>
  </div>
</template>

<script>
import axios from 'axios';

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
