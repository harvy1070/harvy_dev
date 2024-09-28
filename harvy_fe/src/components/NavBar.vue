<template>
    <nav class="navbar">
        <div class="navbar-content">
            <div class="navbar-brand">
                <router-link to="/" class="navbar-item">Developer Kwon</router-link>
            </div>
            <div class="hamburger" @click="toggleMenu">
                <span></span>
                <span></span>
                <span></span>
            </div>
            <div class="navbar-menu" :class="{ 'is-active': isMenuOpen }">
                <router-link to="/" class="navbar-item" :class="{ 'is-active': $route.path === '/' }">Home</router-link>
                <router-link to="/about" class="navbar-item" :class="{ 'is-active': $route.path === '/about' }"
                    >About</router-link
                >
                <router-link
                    to="/project-history"
                    class="navbar-item"
                    :class="{ 'is-active': $route.path === '/project-history' }"
                    >Project History</router-link
                >
                <router-link to="/portfolio" class="navbar-item" :class="{ 'is-active': $route.path === '/portfolio' }"
                    >Portfolio</router-link
                >
                <router-link to="/qna" class="navbar-item" :class="{ 'is-active': $route.path === '/qna' }"
                    >Portfolio Matching</router-link
                >
                <div v-if="isLoggedIn" class="user-menu" @blur="closeDropdown" tabindex="0">
                    <div @click="toggleDropdown" class="user-greeting">
                        <span class="user-name">{{ userName }}</span>
                        <span class="greeting-text">님 반갑습니다.</span>
                    </div>
                    <div v-show="isDropdownOpen" class="dropdown-menu">
                        <a @click="logout" class="dropdown-item">로그아웃</a>
                    </div>
                </div>
                <router-link v-else to="/login" class="navbar-item" :class="{ 'is-active': $route.path === '/login' }"
                    >Login</router-link
                >
            </div>
        </div>
    </nav>
</template>

<script>
import { computed, ref } from 'vue';
import { useStore } from 'vuex';
import { useRouter } from 'vue-router';

export default {
    name: 'NavBar',
    setup() {
        const store = useStore();
        const router = useRouter();
        const isDropdownOpen = ref(false);

        const isLoggedIn = computed(() => store.getters['auth/isAuthenticated']);
        const userName = computed(() => {
            const user = store.getters['auth/currentUser'];
            return user ? user.user_name : '';
        });

        const toggleDropdown = () => {
            isDropdownOpen.value = !isDropdownOpen.value;
        };

        const closeDropdown = () => {
            isDropdownOpen.value = false;
        };

        const logout = async () => {
            await store.dispatch('auth/logout');
            router.push('/login');
        };

        const isMenuOpen = ref(false);

        const toggleMenu = () => {
            isMenuOpen.value = !isMenuOpen.value;
        };

        return {
            isLoggedIn,
            userName,
            logout,
            isDropdownOpen,
            toggleDropdown,
            closeDropdown,
            isMenuOpen,
            toggleMenu,
        };
    },
};
</script>

<style scoped>
.navbar {
    position: fixed;
    top: 0;
    left: 0;
    right: 0;
    background-color: #ffffff;
    box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
    z-index: 1000;
}

.navbar-content {
    display: flex;
    justify-content: space-between;
    align-items: center;
    padding: 1rem 2rem;
    max-width: 1200px;
    margin: 0 auto;
}

.navbar-brand {
    font-size: 1.5rem;
    font-weight: bold;
    color: #346aff;
}

.navbar-menu {
    display: flex;
    gap: 1rem;
}

.navbar-item {
    text-decoration: none;
    color: #333;
    font-weight: 500;
    transition: color 0.3s ease;
}

.navbar-item:hover,
.navbar-item.is-active {
    color: #3498db;
}

.navbar-item.is-active {
    font-weight: 700;
    border-bottom: 2px solid #3498db;
}

.user-menu {
    position: relative;
    cursor: pointer;
}

.user-greeting {
    display: flex;
    align-items: center;
    padding: 0.5rem 1rem;
    border-radius: 4px;
    transition: background-color 0.3s ease;
}

.user-greeting:hover {
    background-color: #f5f5f5;
}

.user-name {
    font-weight: bold;
    color: #3498db;
    margin-right: 0.3rem;
}

.greeting-text {
    font-size: 0.9rem;
    color: #666;
}

.dropdown-menu {
    position: absolute;
    top: 100%;
    right: 0;
    background-color: white;
    border: 1px solid #e0e0e0;
    border-radius: 4px;
    box-shadow: 0 2px 10px rgba(0, 0, 0, 0.1);
    z-index: 1001;
    min-width: 150px;
    margin-top: 0.5rem;
}

.dropdown-item {
    display: block;
    padding: 0.75rem 1rem;
    color: #333;
    text-decoration: none;
    transition: background-color 0.3s ease;
}

.dropdown-item:hover {
    background-color: #f5f5f5;
}

/* 모바일 때문에 햄버거 추가  */
.hamburger {
    display: none;
    flex-direction: column;
    justify-content: space-around;
    width: 2rem;
    height: 2rem;
    cursor: pointer;
}

.hamburger span {
    display: block;
    width: 100%;
    height: 2px;
    background-color: #333;
    transition: all 0.3s linear;
}

@media (max-width: 768px) {
    .navbar-content {
        flex-direction: row;
        justify-content: space-between;
        align-items: center;
    }

    .hamburger {
        display: flex;
    }

    .navbar-menu {
        display: none;
        position: absolute;
        top: 100%;
        left: 0;
        right: 0;
        background-color: #ffffff;
        flex-direction: column;
        width: 100%;
        box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
    }

    .navbar-menu.is-active {
        display: flex;
    }

    .navbar-item {
        padding: 1rem;
        border-top: 1px solid #e0e0e0;
    }

    .user-menu {
        width: 100%;
    }

    .dropdown-menu {
        position: static;
        width: 100%;
        margin-top: 0;
        box-shadow: none;
    }
}
</style>
