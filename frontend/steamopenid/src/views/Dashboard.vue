<script setup>
import router from '../router';
import useAuthStore from '../stores/auth.store'
import { DefaultService } from '../client';
import { onMounted, ref } from 'vue';
const usersStore = useAuthStore();
const { logout } = usersStore

const profile = ref({})

async function loadProfile(){
    const data = await DefaultService.getProfileMeGet()
    console.log(data);
    profile.value = data
}
onMounted(loadProfile)
</script>

<template>
    <div class="brand">
        <h2>Hi {{ profile.personaname }}</h2>
    </div>
    <div class="profile">
        <img class="profile-img" :src="profile.avatar" alt="Profile" />
    </div>
    <button style="margin-top: 50px;" @click="logout();router.push('/login')">Logout</button>
</template>

<style scoped>
.profile .profile-img {
width: 40px;
height: 40px;
border-radius: 50%; 
object-fit: cover;
align-items: center;
}
</style>