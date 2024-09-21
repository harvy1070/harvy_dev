<template>
    <div class="about-page">
        <div class="header">
            <h1>About Me</h1>
        </div>

        <div class="main-tabs">
            <button
                v-for="tab in ['기본정보', '자격증', '경력', '기술 스택']"
                :key="tab"
                @click="selectMainTab(tab)"
                :class="{ active: selectedMainTab === tab }"
            >
                {{ tab }}
            </button>
        </div>

        <div v-if="selectedMainTab === '기본정보'" class="basic-info">
            <div class="business-card">
                <div class="card-left">
                    <img src="@/assets/profile_image.jpg" alt="Profile Image" class="profile-image" />
                </div>
                <div class="card-right">
                    <h2 class="name">{{ basicInfo.name }}</h2>
                    <p class="title">Developer / Data Analyst</p>

                    <p><i class="fas fa-phone"></i> {{ basicInfo.phone }}</p>
                    <p><i class="fas fa-envelope"></i> {{ basicInfo.email }}</p>
                    <p><i class="fas fa-map-marker-alt"></i> {{ basicInfo.address }}</p>
                </div>
            </div>

            <h3><i class="fas fa-graduation-cap"></i> 학력 정보</h3>
            <div class="education-list">
                <div v-for="edu in basicInfo.education" :key="edu.school" class="education-item">
                    <h4>{{ edu.school }}</h4>
                    <p>{{ edu.major }}</p>
                    <p>{{ edu.period }}</p>
                    <p>{{ edu.status }}</p>
                </div>
            </div>
        </div>

        <div v-if="selectedMainTab === '자격증'" class="certifications">
            <h3><i class="fas fa-certificate"></i> 보유 자격증</h3>
            <div class="grid cert-grid">
                <div class="cert-item" v-for="cert in certifications" :key="cert.name">
                    <h4>{{ cert.name }}</h4>
                    <p>{{ cert.date }}</p>
                    <p>{{ cert.org }}</p>
                </div>
            </div>

            <h3><i class="fas fa-hourglass-half"></i> 취득 준비중인 자격증</h3>
            <div class="grid cert-grid">
                <div class="cert-item" v-for="cert in preparingCertifications" :key="cert.name">
                    <h4>{{ cert.name }}</h4>
                    <p>예정일: {{ cert.expectedDate }}</p>
                    <p>{{ cert.org }}</p>
                </div>
            </div>
        </div>

        <div v-if="selectedMainTab === '경력'" class="work-experience">
            <h3><i class="fas fa-briefcase"></i> 회사 경력</h3>
            <div class="timeline">
                <div class="experience-item" v-for="exp in experiences" :key="exp.company">
                    <div class="timeline-date">
                        <span class="date-circle"></span>
                        {{ exp.period }}
                    </div>
                    <div class="timeline-content">
                        <div class="company-position">
                            <h4 class="company-name">
                                {{ exp.company }}<span class="position">{{ exp.position }}</span>
                            </h4>
                        </div>
                        <div class="company-desc">
                            <p>{{ exp.description }}</p>
                        </div>
                    </div>
                </div>
            </div>
        </div>

        <div v-if="selectedMainTab === '기술 스택'" class="skills">
            <h3><i class="fas fa-code"></i> 기술 스택</h3>
            <div class="skill-tabs">
                <button
                    v-for="category in skills"
                    :key="category.name"
                    @click="selectCategory(category.name)"
                    :class="{ active: selectedCategory === category.name }"
                >
                    {{ category.name }}
                </button>
            </div>
            <div class="skill-content" v-if="selectedCategory">
                <div class="skill-grid">
                    <div class="skill-item" v-for="skill in getSelectedSkills" :key="skill.name">
                        <div class="skill-name">{{ skill.name }}</div>
                        <div class="skill-level">
                            <div class="skill-bar" :style="{ width: skill.level + '%' }"></div>
                        </div>
                    </div>
                </div>
            </div>
        </div>
    </div>
</template>

<script>
export default {
    name: 'AboutPage',
    data() {
        return {
            selectedMainTab: '기본정보',
            selectedCategory: null,
            basicInfo: {
                name: '권승회',
                birthDate: '1992. 01. 27.',
                phone: '010-9364-4402',
                email: 'harvy13@naver.com',
                address: '인천광역시 남동구 하촌로 41 4층',
                education: [
                    {
                        school: '인천정보산업고등학교',
                        degree: '고등학교',
                        period: '2007. 03. - 2010. 03.',
                        major: '전산과',
                        status: '졸업',
                    },
                    {
                        school: '경기공업대학교(과학기술대)',
                        degree: '전문대학',
                        period: '2010. 03. - 2011. 03.',
                        major: 'E비즈니스과',
                        status: '중퇴',
                    },
                    {
                        school: '학점은행제(4년제 학위)',
                        degree: '대학교',
                        period: '2016. 06. - 2022. 02.',
                        major: '컴퓨터공학과',
                        status: '졸업',
                    },
                ],
            },
            certifications: [
                // {
                //     name: '빅데이터분석기사(필기)',
                //     date: '2024. 09. 07.',
                //     org: '한국데이터베이스진흥센터',
                // },
                {
                    name: 'OPIC IL',
                    date: '2024. 03. 31.',
                    org: 'ACTFL',
                },
                {
                    name: 'AICE Associate',
                    date: '2023. 11. 03.',
                    org: 'KT, 한국경제신문',
                },
                {
                    name: '정보처리기사',
                    date: '2022. 11. 25.',
                    org: '한국산업인력공단',
                },
                {
                    name: 'SQLD',
                    date: '2022. 09. 30.',
                    org: '한국데이터베이스진흥센터',
                },
                {
                    name: '전산회계 1급',
                    date: '2011. 07. 11.',
                    org: '한국세무사회',
                },
            ],
            preparingCertifications: [
                {
                    name: '빅데이터분석기사',
                    expectedDate: '2025. 03.',
                    org: '한국데이터산업진흥원',
                },
                {
                    name: 'TEPS 327점 이상',
                    expectedDate: '2025. 01. ~',
                    org: '서울대학교 언어교육원',
                },
                {
                    name: 'OPIc IM 이상 등급',
                    expectedDate: '~ 2024. 12.',
                    org: 'ACTFL',
                },
            ],
            experiences: [
                {
                    company: '클립데이터',
                    position: '사원',
                    period: '2024. 08. 01. ~ 2024. 09. 01.',
                    description: 'Vue.js를 활용한 회사 페이지 개발, Django를 활용한 금융 프로그램 서버 유지보수',
                },
                {
                    company: 'KT Aivle',
                    position: '교육생',
                    period: '2023. 08. 08. ~ 2024. 01. 25.',
                    description: '데이터 전처리, 분석 및 머신/딥 러닝 교육 수료, 전반적 개발 프로세스 경험',
                },
                {
                    company: '협동조합꿈꾸는문화놀이터뜻',
                    position: '주임',
                    period: '2020. 01. 02. ~ 2021. 07. 31.',
                    description:
                        '기획안 작성 및 실행, 제안서 작성 및 실행, 디자인(포스터, 로고 등), 웹 퍼블리싱 작업(CSS)',
                },
                {
                    company: '푸를나이JOBCON남동구청',
                    position: '팀장',
                    period: '2019. 08. 01. ~ 2019. 12. 31.',
                    description: '아티스트(국악, 클래식, 실용음악 등) 인원 관리 및 행사 기획, 웹 사이트 개설',
                },
                {
                    company: '하이윌테크놀로지',
                    position: '사원',
                    period: '2019. 02. 05. ~ 2019. 06. 25.',
                    description: '프론트엔드 개발(JAVA)',
                },
                {
                    company: '한민수시의원선거캠프',
                    position: '사원',
                    period: '2018. 12. 02. ~ 2019. 01. 23.',
                    description: '선거 지역 내 당 인원 데이터 관리 및 전산 작업',
                },
            ],
            skills: [
                {
                    name: '데이터 분석 & AI',
                    items: [
                        { name: 'Python', level: 85 },
                        { name: 'Pandas/Numpy', level: 70 },
                        { name: 'TensorFlow/Pytorch', level: 65 },
                        { name: 'Matplotlib/Seaborn', level: 75 },
                        { name: 'SQL', level: 55 },
                    ],
                },
                {
                    name: '웹 개발',
                    items: [
                        { name: 'HTML/CSS', level: 70 },
                        { name: 'Django', level: 40 },
                        { name: 'Vue.js', level: 20 },
                    ],
                },
                {
                    name: 'DevOps & 툴',
                    items: [
                        { name: 'Docker', level: 20 },
                        { name: 'Git', level: 60 },
                        { name: 'Linux', level: 40 },
                    ],
                },
                {
                    name: 'OA',
                    items: [
                        { name: '한글', level: 90 },
                        { name: 'Excel', level: 90 },
                        { name: 'PowerPoint', level: 90 },
                    ],
                },
                {
                    name: '디자인',
                    items: [
                        { name: 'Photoshop', level: 60 },
                        { name: 'Illustrator', level: 90 },
                    ],
                },
            ],
        };
    },
    computed: {
        getSelectedSkills() {
            if (!this.selectedCategory) return [];
            return this.skills.find((category) => category.name === this.selectedCategory)?.items || [];
        },
    },
    methods: {
        selectMainTab(tab) {
            this.selectedMainTab = tab;
            if (tab === '기술 스택' && this.skills.length > 0) {
                this.selectCategory(this.skills[0].name);
            }
        },
        selectCategory(categoryName) {
            this.selectedCategory = categoryName;
        },
    },
    mounted() {
        this.selectMainTab('기본정보');
    },
};
</script>

<style>
/* 전역 스타일 */
.about-page {
    font-family: 'NanumSquare', sans-serif;
}

html,
body {
    scrollbar-width: none;
    -ms-overflow-style: none;
}

html::-webkit-scrollbar,
body::-webkit-scrollbar {
    display: none;
}
</style>

<style scoped>
/* 레이아웃 */
.about-page {
    max-width: 800px;
    margin: 0 auto;
    padding: 2rem;
    color: #333;
}

.header {
    margin-top: 50px;
    text-align: center;
    margin-bottom: 2rem;
}

/* 타이포그래피 */
h1,
h2,
h3,
h4 {
    color: #2c3e50;
}

h1 {
    font-size: 2.5rem;
    margin-bottom: 1rem;
}

h3 {
    font-size: 1.5rem;
    margin-bottom: 1rem;
    border-bottom: 2px solid #3498db;
    padding-bottom: 0.5rem;
}

h4 {
    color: #3498db;
}

/* 명함 스타일 */
.business-card {
    width: 100%;
    height: 200px;
    display: flex;
    background-color: #ffffff;
    border-radius: 10px;
    box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
    overflow: hidden;
    margin-bottom: 2rem;
}

.card-left {
    flex: 0 0 150px;
    background-color: #3498db;
}

.profile-image {
    width: 100%;
    height: 100%;
    object-fit: cover;
}

.card-right {
    flex: 1;
    padding: 1rem;
    display: flex;
    flex-direction: column;
    justify-content: center;
}

.name {
    margin-top: -3px;
    font-size: 1.4rem;
    color: #2c3e50;
    margin-bottom: 0.25rem;
}

.title {
    font-size: 1rem;
    color: #7f8c8d;
    margin-bottom: 1rem;
}

.card-right p {
    font-size: 0.9rem;
    margin-bottom: 0.25rem;
    display: flex;
    align-items: center;
}

.card-right i {
    margin-right: 0.5rem;
    color: #3498db;
    width: 15px;
}

/* 학력 정보 스타일 */
.education-list {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
}

.education-item {
    background-color: #ffffff;
    padding: 1rem;
    border-radius: 10px;
    box-shadow: 0 4px 6px rgba(0, 0, 0, 0.05);
    transition: all 0.3s ease;
}

.education-item:hover {
    transform: translateY(-5px);
    box-shadow: 0 6px 12px rgba(0, 0, 0, 0.1);
}

.education-item h4 {
    margin-top: 10px;
    color: #3498db;
    font-size: 1rem;
    margin-bottom: 1rem;
    letter-spacing: 0.5px;
    border-bottom: 2px solid #e0e0e0;
    padding-bottom: 0.5rem;
}

.education-item p {
    margin: 0.05rem 0;
    color: #555;
    font-size: 0.95rem;
    line-height: 1.5;
}

.education-item p:nth-child(2) {
    font-weight: 600;
    color: #2c3e50;
}

.education-item p:nth-child(3) {
    color: #7f8c8d;
    font-style: italic;
}

.education-item p:nth-child(4) {
    color: #0ba6b1;
    font-size: 0.9rem;
}

.education-item p:last-child {
    margin-top: 0.1rem;
    color: #3498db;
    font-weight: 600;
}

/* 탭 스타일 */
.main-tabs,
.skill-tabs {
    display: flex;
    justify-content: center;
    margin-bottom: 2rem;
    background-color: #f0f4f8;
    border-radius: 50px;
    padding: 0.5rem;
    box-shadow: 0 2px 10px rgba(0, 0, 0, 0.1);
}

.main-tabs button,
.skill-tabs button {
    padding: 0.75rem 1.5rem;
    margin: 0;
    border: none;
    background-color: transparent;
    border-radius: 50px;
    cursor: pointer;
    transition: all 0.3s ease;
    font-size: 1rem;
    font-family: 'NanumSquare', sans-serif !important;
    font-weight: 600;
    color: #555;
}

.main-tabs button.active,
.skill-tabs button.active {
    background-color: #3498db;
    color: white;
    box-shadow: 0 2px 5px rgba(52, 152, 219, 0.3);
}

/* 그리드 레이아웃 */
.grid,
.skill-grid {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
    gap: 1rem;
}

/* 자격증 아이템 스타일 */
.cert-grid {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
    gap: 1rem;
}

.cert-item {
    background-color: #ffffff;
    padding: 0.5rem 1rem 1rem;
    border-radius: 10px;
    box-shadow: 0 4px 6px rgba(0, 0, 0, 0.05);
    transition: all 0.3s ease;
}

.cert-item:hover {
    transform: translateY(-5px);
    box-shadow: 0 6px 12px rgba(0, 0, 0, 0.1);
}

.cert-item h4 {
    margin-top: 5px;
    color: #3498db;
    font-size: 1rem;
    margin-bottom: 0.5rem;
    letter-spacing: 0.5px;
    border-bottom: 2px solid #e0e0e0;
    padding-bottom: 0.3rem;
}

.cert-item p {
    margin: 0.25rem 0;
    color: #555;
    font-size: 0.9rem;
    line-height: 1.4;
}

.cert-item p:first-of-type {
    color: #7f8c8d;
    font-style: italic;
}

.cert-item p:last-child {
    color: #2c3e50;
    font-weight: 600;
}

/* 경력 타임라인 스타일 */
.work-experience {
    max-width: 800px;
    margin: 0 auto;
}

.timeline {
    position: relative;
    padding: 20px 0;
}

.timeline::before {
    content: '';
    position: absolute;
    top: 0;
    bottom: 0;
    left: 20px;
    width: 2px;
    background: #e0e0e0;
}

.experience-item {
    position: relative;
    margin-bottom: 40px;
    padding-left: 50px;
}

.timeline-date {
    font-weight: 600;
    margin-bottom: 10px;
    color: #3498db;
    position: relative;
}

.date-circle {
    position: absolute;
    left: -35px;
    top: 50%;
    transform: translateY(-50%);
    width: 12px;
    height: 12px;
    background-color: #3498db;
    border-radius: 50%;
    z-index: 1;
}

.timeline-content {
    background: #ffffff;
    padding: 20px;
    border-radius: 8px;
    box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
    transition: all 0.3s ease;
}

.timeline-content:hover {
    transform: translateY(-5px);
    box-shadow: 0 6px 12px rgba(0, 0, 0, 0.15);
}

/* company-name과 position을 인라인으로 표시하기 위한 새로운 스타일 */
.company-position {
    margin-bottom: 10px;
}

.company-name {
    margin: 0;
    color: #2c3e50;
    font-size: 1.2rem;
    display: inline-block;
}

.position {
    margin-left: 10px;
    font-weight: 600;
    color: #3498db;
    font-size: 0.9rem;
}

.company-desc p {
    color: #34495e;
    line-height: 1.6;
    font-size: 0.95rem;
    margin-bottom: 0;
}

/* 기술 스택 스타일 */
.skill-content {
    background-color: #ffffff;
    padding: 2rem;
    border-radius: 12px;
    box-shadow: 0 4px 20px rgba(0, 0, 0, 0.1);
}

.skill-item {
    background-color: #f8f9fa;
    padding: 1rem;
    border-radius: 8px;
    box-shadow: 0 2px 4px rgba(0, 0, 0, 0.05);
    transition: all 0.3s ease;
}

.skill-item:hover {
    transform: translateY(-2px);
    box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
}

.skill-name {
    font-weight: 600;
    margin-bottom: 0.75rem;
    color: #2c3e50;
}

.skill-level {
    background-color: #e0e6ed;
    height: 8px;
    border-radius: 4px;
    overflow: hidden;
}

.skill-bar {
    height: 100%;
    background-color: #3498db;
    border-radius: 4px;
    transition: width 0.5s ease-out;
}

/* 반응형 스타일 */
@media (max-width: 768px) {
    .company-name {
        display: block;
        margin-bottom: 5px;
    }

    .position {
        margin-left: 0;
        display: block;
    }

    .about-page {
        padding: 1rem;
    }

    .business-card {
        flex-direction: column;
    }

    .card-left {
        max-width: 100%;
        height: 200px;
    }

    .card-right {
        padding: 1rem;
    }

    .info-grid {
        grid-template-columns: 1fr;
    }

    .info-item {
        flex-basis: 100%;
    }

    .grid,
    .skill-grid {
        grid-template-columns: 1fr;
    }

    .main-tabs,
    .skill-tabs {
        flex-wrap: wrap;
        border-radius: 12px;
    }

    .main-tabs button,
    .skill-tabs button {
        flex: 1 1 calc(50% - 0.5rem);
        margin: 0.25rem;
        font-size: 0.9rem;
        padding: 0.6rem 1rem;
    }

    .timeline::before {
        left: 15px;
    }

    .experience-item {
        padding-left: 35px;
    }

    .timeline-date {
        margin-left: 10px;
    }

    .date-circle {
        left: -35.5px;
        top: 5px;
        transform: none;
    }

    .timeline-content {
        margin-left: 10px;
    }
    .cert-grid {
        grid-template-columns: 1fr;
    }
}
</style>
