<template>
<SettingsComponent />
</template>
<script setup>
import SettingsComponent from '@/components/SettingsComponent.vue'
</script>
<style scoped>
* {
  box-sizing: border-box;
}

label {
  padding: 12px 12px 12px 0;
  display: inline-block;
}

button[type=submit] {
  background-color: #4CAF50;
  color: white;
  padding: 12px 20px;
  cursor: pointer;
  border-radius: 30px;
}

button[type=submit]:hover {
  background-color: #45a049;
}

input {
  margin: 5px;
  box-shadow: 0 0 15px 4px rgba(0, 0, 0, 0.06);
  padding: 10px;
  border-radius: 30px;
}

#error {
  color: red;
}
</style>
