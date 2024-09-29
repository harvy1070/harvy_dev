<template>
    <nav class="navbar">
        <div class="navbar-content">
            <div class="navbar-brand">
                <router-link to="/" class="navbar-item">Developer Kwon</router-link>
            </div>
            <div class="hamburger" @click="toggleMenu" :class="{ 'is-active': isMenuOpen }">
                <span></span>
                <span></span>
                <span></span>
            </div>
            <div class="navbar-menu" :class="{ 'is-active': isMenuOpen }">
                <router-link to="/" class="navbar-item" :class="{ 'is-active': $route.path === '/' }" @click="closeMenu"
                    >Home</router-link
                >
                <router-link
                    to="/about"
                    class="navbar-item"
                    :class="{ 'is-active': $route.path === '/about' }"
                    @click="closeMenu"
                    >About</router-link
                >
                <router-link
                    to="/project-history"
                    class="navbar-item"
                    :class="{ 'is-active': $route.path === '/project-history' }"
                    @click="closeMenu"
                    >Project History</router-link
                >
                <router-link
                    to="/portfolio"
                    class="navbar-item"
                    :class="{ 'is-active': $route.path === '/portfolio' }"
                    @click="closeMenu"
                    >Portfolio</router-link
                >
                <router-link
                    to="/qna"
                    class="navbar-item"
                    :class="{ 'is-active': $route.path === '/qna' }"
                    @click="closeMenu"
                    >PM Chatbot</router-link
                >
                <div v-if="isLoggedIn" class="user-menu">
                    <div @click="toggleDropdown" class="user-greeting">
                        <span class="user-name">{{ userName }}</span>
                        <span class="greeting-text">님 반갑습니다.</span>
                    </div>
                    <div v-show="isDropdownOpen" class="dropdown-menu">
                        <a @click="logout" class="dropdown-item">로그아웃</a>
                    </div>
                </div>
                <router-link
                    v-else
                    to="/login"
                    class="navbar-item"
                    :class="{ 'is-active': $route.path === '/login' }"
                    @click="closeMenu"
                    >Login</router-link
                >
            </div>
        </div>
    </nav>
</template>

<script>
import { computed, ref, onMounted, onUnmounted } from 'vue';
import { useStore } from 'vuex';
import { useRouter } from 'vue-router';

export default {
    name: 'NavBar',
    setup() {
        const store = useStore();
        const router = useRouter();
        const isDropdownOpen = ref(false);
        const isMenuOpen = ref(false);

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

        const toggleMenu = () => {
            isMenuOpen.value = !isMenuOpen.value;
        };

        const closeMenu = () => {
            isMenuOpen.value = false;
        };

        const handleOutsideClick = (event) => {
            const navbar = document.querySelector('.navbar');
            if (navbar && !navbar.contains(event.target)) {
                closeMenu();
            }
        };

        onMounted(() => {
            document.addEventListener('click', handleOutsideClick);
        });

        onUnmounted(() => {
            document.removeEventListener('click', handleOutsideClick);
        });

        return {
            isLoggedIn,
            userName,
            logout,
            isDropdownOpen,
            toggleDropdown,
            closeDropdown,
            isMenuOpen,
            toggleMenu,
            closeMenu,
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
    height: 80px;
}

.navbar-content {
    display: flex;
    justify-content: space-between;
    align-items: center;
    height: 100%;
    padding: 0 2rem;
    max-width: 1200px;
    margin: 0 auto;
}

.navbar-brand {
    font-size: 1.2rem;
    font-weight: bold;
    color: #346aff;
}

.navbar-menu {
    display: none;
}

.hamburger {
    display: flex;
    flex-direction: column;
    justify-content: space-around;
    width: 2rem;
    height: 2rem;
    background: transparent;
    border: none;
    cursor: pointer;
    padding: 0;
}

.hamburger span {
    width: 2rem;
    height: 0.25rem;
    background-color: #333;
    transition: all 0.3s linear;
    position: relative;
    transform-origin: 1px;
}

.hamburger.is-active span:first-child {
    transform: rotate(45deg);
}

.hamburger.is-active span:nth-child(2) {
    opacity: 0;
}

.hamburger.is-active span:nth-child(3) {
    transform: rotate(-45deg);
}

.navbar-item {
    text-decoration: none;
    color: #333;
    font-weight: 500;
    padding: 0.5rem 1rem;
    font-size: 1rem;
}

.navbar-item.is-active {
    color: #3498db;
    font-weight: 700;
}

.user-menu {
    position: relative;
}

.user-greeting {
    display: flex;
    align-items: center;
    cursor: pointer;
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
}

.dropdown-item {
    display: block;
    padding: 0.5rem 1rem;
    color: #333;
    text-decoration: none;
}

@media (max-width: 768px) {
    .navbar-menu.is-active {
        display: flex;
        flex-direction: column;
        position: fixed;
        top: 80px;
        left: 0;
        right: 0;
        bottom: 0;
        background-color: #ffffff;
        padding: 1rem;
    }

    .navbar-item {
        padding: 0.75rem 0;
        border-bottom: 1px solid #e0e0e0;
    }

    .user-menu {
        padding: 0.75rem 0;
        border-bottom: 1px solid #e0e0e0;
    }
}

@media (min-width: 769px) {
    .navbar-content {
        flex-wrap: nowrap;
    }

    .hamburger {
        display: none;
    }

    .navbar-menu {
        display: flex;
        align-items: center;
        justify-content: flex-end;
        flex-grow: 1;
    }

    .navbar-item {
        border-bottom: none;
    }

    .navbar-item.is-active {
        border-bottom: 2px solid #3498db;
    }

    .user-menu {
        margin-left: 1rem;
    }
}
</style>
