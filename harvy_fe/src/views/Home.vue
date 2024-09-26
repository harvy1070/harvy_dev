<template>
    <div class="home">
        <div class="background-shape"></div>
        <div class="content-wrapper">
            <h1 class="main-title">코더가 아닌 생각을 하는 개발자가 되겠습니다.</h1>
            <div class="hero-section">
                <div class="profile-image-container">
                    <img src="@/assets/profile_image.jpg" alt="Profile Image" class="profile-image" />
                </div>
                <div class="hero-content">
                    <!-- <h2 class="name">권승회</h2> -->
                    <p class="title">생각하는 개발자 권승회</p>
                    <p class="description">
                        기획 회사에서의 2년간의 기획 경험을 바탕으로,<br />
                        단순한 코더가 아닌 문제 해결에 강한 개발자가 되기 위해 노력하고 있습니다.<br /><br />
                        KT Aivle에서 데이터 분석과 AI 개발 프로젝트를 경험하였으며,<br />
                        Kaggle 대회에 지속적으로 참여하며 AI 개발 역량을 강화하고 있습니다.<br /><br />
                        또한, 백엔드 개발에도 열정을 가지고 있으며,<br />
                        Django 프레임워크를 활용해 설계하고 구현하는 연습을 하고 있습니다.<br />
                        그리고 RESTful API 개발, 데이터베이스 관리, 사용자 인증 및 권한 부여 등의<br />
                        작업을 통해 안정적인 백엔드 시스템을 구축하기 위해 노력하고 있습니다.
                    </p>
                    <router-link to="/about" class="cta-button">View About Me</router-link>
                </div>
            </div>
        </div>
    </div>
</template>

<script>
export default {
    name: 'HomePage',
};
</script>

<style scoped>
.home {
    height: 98vh; /* 변경: min-height에서 height로 변경 */
    display: flex;
    justify-content: center;
    align-items: center;
    background-color: #f0f4f8;
    position: relative;
    overflow: hidden;
}

.background-shape {
    position: absolute;
    top: -50%;
    left: -50%;
    width: 200%;
    height: 200%;
    background: linear-gradient(45deg, #3498db, #8e44ad);
    animation: rotate 20s linear infinite;
    z-index: 1;
}

@keyframes rotate {
    from {
        transform: rotate(0deg);
    }
    to {
        transform: rotate(360deg);
    }
}

.content-wrapper {
    /* margin-left: 100px; */
    background-color: rgba(255, 255, 255, 0.9);
    padding: 2rem; /* 변경: 패딩 줄임 */
    border-radius: 20px;
    box-shadow: 0 10px 30px rgba(0, 0, 0, 0.1);
    z-index: 2;
    max-width: 800px;
    width: 90%;
    max-height: 90vh; /* 추가: 최대 높이 설정 */
    overflow-y: auto; /* 추가: 내용이 넘칠 경우 스크롤 */
}

.main-title {
    font-size: 2rem; /* 변경: 글자 크기 줄임 */
    color: #3498db;
    margin-bottom: 1.5rem; /* 변경: 마진 줄임 */
    text-align: center;
    font-weight: 700;
}

.hero-section {
    display: flex;
    align-items: center;
    gap: 2rem; /* 변경: 갭 줄임 */
}

.profile-image {
    width: 210px; /* 변경: 이미지 크기 줄임 */
    height: 230px; /* 변경: 이미지 크기 줄임 */
    border-radius: 20%;
    object-fit: cover;
    border: 5px solid #fff;
    box-shadow: 0 5px 15px rgba(0, 0, 0, 0.1);
    transition: transform 0.3s ease;
}

.name {
    font-size: 1.5rem; /* 변경: 글자 크기 줄임 */
    color: #2c3e50;
    margin-bottom: 0.5rem;
    font-weight: 700;
}

.title {
    font-size: 1.3rem; /* 변경: 글자 크기 줄임 */
    color: #3498db;
    margin-bottom: 0.8rem; /* 변경: 마진 줄임 */
    font-weight: 600;
}

.description {
    font-size: 0.9rem; /* 변경: 글자 크기 줄임 */
    color: #34495e;
    margin-bottom: 1.2rem; /* 변경: 마진 줄임 */
    line-height: 1.5;
}

.cta-button {
    margin-top: 10px;
    display: inline-block;
    padding: 0.6rem 1.2rem; /* 변경: 패딩 줄임 */
    background-color: #3498db;
    color: white;
    text-decoration: none;
    border-radius: 30px;
    font-weight: 600;
    transition: all 0.3s ease;
    box-shadow: 0 4px 6px rgba(50, 50, 93, 0.11), 0 1px 3px rgba(0, 0, 0, 0.08);
}

@media (max-width: 768px) {
    .hero-section {
        flex-direction: column;
        text-align: center;
    }

    .profile-image {
        width: 120px; /* 변경: 모바일에서 이미지 크기 더 줄임 */
        height: 120px; /* 변경: 모바일에서 이미지 크기 더 줄임 */
    }

    .name {
        font-size: 1.8rem; /* 변경: 모바일에서 글자 크기 줄임 */
    }

    .content-wrapper {
        padding: 1.5rem; /* 변경: 모바일에서 패딩 줄임 */
    }
}
</style>
