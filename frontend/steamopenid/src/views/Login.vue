<template>
    <div>
      <button @click="startSteamOpenIDAuth('/login')" :disabled="isLoading">
        <span v-if="isLoading" class="spinner"></span>
        <span v-else>Login with Steam</span>
      </button>
    </div>
  </template>
  
  <style>
  .spinner {
    border: 3px solid rgba(0, 0, 0, 0.3);
    border-top: 3px solid #3498db;
    border-radius: 50%;
    width: 20px;
    height: 20px;
    animation: spin 1s linear infinite;
    display: inline-block;
  }
  
  @keyframes spin {
    0% { transform: rotate(0deg); }
    100% { transform: rotate(360deg); }
  }
  </style>
  
  <script setup>
    import { onMounted } from 'vue';
    import { storeToRefs } from 'pinia';
    import useAuthStore from '../stores/auth.store'
    import router from '../router'


    const usersStore = useAuthStore();
    const {steamOpenIDCallback, startSteamOpenIDAuth} = usersStore
    const { isLoading } = storeToRefs(usersStore);

    onMounted(async () => {
        const urlParams = new URLSearchParams(window.location.search);
        const actionParam = urlParams.get('action');
        
        if (actionParam && actionParam.toLowerCase() === 'callback') {
            const callbackSuccess = await steamOpenIDCallback(urlParams);
            if (callbackSuccess) {
                router.push('/dashboard')
            }
        }
    });
</script>
  