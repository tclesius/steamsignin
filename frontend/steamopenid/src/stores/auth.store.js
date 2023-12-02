import { defineStore } from "pinia"
import { ref } from "vue"
import { OpenAPI } from "../client";
import router from "../router";
import { DefaultService } from "../client";


const useAuthStore = defineStore('auth',() => {
    const isLoading = ref(false)
    OpenAPI.TOKEN = localStorage.getItem('access_token') // needed so the token is available on reload of page too

    async function startSteamOpenIDAuth(returnToPath){
        const params = new URLSearchParams({
            'openid.ns': 'http://specs.openid.net/auth/2.0',
            'openid.mode': 'checkid_setup',
            'openid.return_to': "http://localhost:5173" + returnToPath + "?action=callback", // localhost changes so should be somehow in .env
            'openid.realm': "http://localhost:5173" + returnToPath + "?action=callback", // localhost changes so should be somehow in .env
            'openid.identity': 'http://specs.openid.net/auth/2.0/identifier_select',
            'openid.claimed_id': 'http://specs.openid.net/auth/2.0/identifier_select'
        });
        window.location.href = `https://steamcommunity.com/openid/login?${params.toString()}`; // this redirects the user to Steam
    }
    async function steamOpenIDCallback(urlParams){
       
        if (urlParams && urlParams.get("action") === "callback") {
            isLoading.value = true;
            urlParams.delete("action");
    
            const paramsObject = {};
            for (const [key, value] of urlParams) {
                paramsObject[key] = value;
            }
            const data = await DefaultService.callbackAuthSteamCallbackPost({requestBody: paramsObject})
            if(data.access_token){
                localStorage.setItem('access_token', data.access_token)
                OpenAPI.TOKEN = data.access_token
                isLoading.value = false;
                return true
            }
        }
        return false;
    }
    async function logout(){
        localStorage.removeItem('access_token')
    }

    return { isLoading, startSteamOpenIDAuth, steamOpenIDCallback, logout}
    
})

export default useAuthStore