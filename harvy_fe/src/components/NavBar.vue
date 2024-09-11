<template>
    <nav class="navbar">
        <div class="navbar-content">
            <div class="navbar-brand">
                <router-link to="/" class="navbar-item">Developer Kwon</router-link>
            </div>
            <div class="navbar-menu">
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
                    >Q&A</router-link
                >
            </div>
        </div>
    </nav>
</template>

<script>
export default {
    name: 'NavBar',
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

@media (max-width: 768px) {
    .navbar-content {
        flex-direction: column;
        align-items: flex-start;
    }

    .navbar-menu {
        flex-direction: column;
        width: 100%;
        margin-top: 1rem;
    }

    .navbar-item {
        padding: 0.5rem 0;
    }

    .navbar-item.is-active {
        border-bottom: none;
        border-left: 2px solid #3498db;
        padding-left: 0.5rem;
    }
}
</style>
